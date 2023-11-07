"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
from ebx.constants.api import API_PREFIX, OAUTH_PATH, BASE_URL, API_SECRETS_PATH
import urllib.parse
from os import getenv
from ebx.peristence.local_filesystem import LocalFilePersistence
from ebx.peristence.abstact_persistence import AbstractPersistence

class ClientConfig():
    """Configuration for the Earth Blox API client."""
    def __init__(self) -> None:
        self.base_url = BASE_URL
        self.api_prefix = API_PREFIX
        self.oauth_path = OAUTH_PATH 
        self.persistence_driver = LocalFilePersistence(path=API_SECRETS_PATH)

        if getenv("EBX_API_EMULATOR_HOST") is not None:
            emulator_host = getenv("EBX_API_EMULATOR_HOST")
            self.base_url = emulator_host
        
        if getenv("EBX_API_PREFIX_PATH") is not None:
            self.api_prefix = getenv("EBX_API_PREFIX_PATH")

    def get_api_base_url(self):
        return urllib.parse.urljoin(self.base_url, self.api_prefix)
    
    def get_oauth_url(self):
        if getenv("EBX_API_AUTH_EMULATOR") is not None:
           return getenv("EBX_API_AUTH_EMULATOR")  
        return urllib.parse.urljoin(self.base_url, self.oauth_path)
    
    def get_persistence_driver(self) -> AbstractPersistence:
        return self.persistence_driver
    

class ServiceClientConfig(ClientConfig):
    """Configuration for the Earth Blox API client."""
    def __init__(self) -> None:
        super().__init__()
        self.api_prefix = ""
        self.base_url = BASE_URL
        if getenv("EBX_API_CLIENT_REGISTRATION") is not None:
            emulator_host = getenv("EBX_API_CLIENT_REGISTRATION")
            self.base_url = emulator_host 