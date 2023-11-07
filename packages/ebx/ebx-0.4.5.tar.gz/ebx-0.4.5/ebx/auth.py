"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
from ebx.models.auth_token import AuthToken
from os import getenv
import httpx
import datetime
import datetime
from ebx.config import ClientConfig
import base64
from abc import ABC
from ebx.constants.api import API_TOKEN_FILE

class AbstractAuthentication(ABC):
    """Abstract class for authentication."""
    def __init__(self, config: ClientConfig):
        self.auth_token = None
        self.config = config

    def has_expired(self) -> bool:
        return self.auth_token is None or self.auth_token.expires is None or self.auth_token.expires < datetime.datetime.now(tz=datetime.timezone.utc)
    
    def refresh(self) -> None:
        pass

    def id(self):
        return id(self)
    
    def get_headers(self):
        return {}


class EnvAuthentication(AbstractAuthentication):
    """Authentication using the EBX_API_TOKEN environment variable."""
    def __init__(self, config: ClientConfig) -> None:
        self.auth_token = getenv("EBX_API_TOKEN")
        self.config = config

    def has_expired(self) -> bool:
        return False
    
    def refresh(self) -> None:
        self.auth_token = getenv("EBX_API_TOKEN")
        return self
    
    def setToken(self, token: str) -> None:
        self.auth_token = token
        return self
    
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.auth_token}",
        }
    
class BasicAuth(AbstractAuthentication):
    """Authentication using a username and password."""
    def __init__(self, config: ClientConfig, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self.config = config

    def has_expired(self) -> bool:
        return False
    
    def refresh(self) -> None:
        raise NotImplementedError("BasicAuth does not support refresh")
        return self
    
    def get_headers(self):
        base64string = base64.b64encode(f"{self.email}:{self.password}".encode('utf-8')).decode('utf-8')
        return {
            "Authorization": f"Basic {base64string}",
        }

class OAuthAuthentication(AbstractAuthentication):
    """Authentication using OAuth."""
    def __init__(self, config: ClientConfig, client_id: str = None, client_secret: str = None):
        self.config = config
        self.client_id = client_id
        self.client_secret = client_secret
        if self.client_id is None:
            self.client_id = getenv("EBX_CLIENT_ID")
        if self.client_secret is None:
            self.client_secret = getenv("EBX_CLIENT_SECRET")
        self.auth_token = None

        if self.client_secret is None:
            raise ValueError("No client secret provided")
        if self.client_id is None:
            raise ValueError("No client id provided")
        
        self.load_saved_credentials()

    def refresh(self) -> None:
        """Creates a new token for the client.
            Returns:
            AuthToken: The new token.
        """
        request_data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = httpx.post(self.config.get_oauth_url(), json=request_data, headers=headers)
        if res.status_code == 200:
            responseJson = res.json()
            expires = datetime.datetime.fromisoformat(responseJson["expires"]).replace(tzinfo=datetime.timezone.utc)
            self.auth_token = AuthToken(token=responseJson["token"], expires=expires)
            self.save_credentials()
            return self
        else:
            res.raise_for_status()
        
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.auth_token.token}",
        }
    
    def get_token_filename(self):
        return self.client_id+"_"+API_TOKEN_FILE
    
    def load_saved_credentials(self):
        if AuthToken.saved_token_exists(self.config, self.get_token_filename()):
            self.auth_token = AuthToken.load(self.config, self.get_token_filename())
        return self
    
    def save_credentials(self):
        self.auth_token.save(self.config, self.get_token_filename())
        return self

