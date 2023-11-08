##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class KeycloakSchema(BaseModel):
    server_url: str = Field(
        title='Keycloak Server URL',
        description='Base URL of the Keycloak instance'
    )
    realm: str = Field(
        title='Keycloak Realm',
        description='Name of the realm for authentication'
    )
    client_id: Optional[str] = Field(
        default=None,
        title='Client ID',
        description='Client ID for authentication'
    )
    username: Optional[str] = Field(
        default=None,
        title='Username',
        description='Username for client-based authentication'
    )
    password: Optional[SecretStr] = Field(
        default=None,
        title='Password',
        description='Password for client-based authentication'
    )
    client_secret: Optional[SecretStr] = Field(
        default=None,
        title='Client Secret',
        description='Client Secret for client-based authentication'
    )
    verify: Optional[bool] = Field(
        default=True,
        title='SSL Verification',
        description='Boolean to decide if SSL certificate verification should be performed'
    )
