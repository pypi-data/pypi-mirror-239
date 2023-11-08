##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class VaultSchema(BaseModel):
    url: str = Field(
        title='Vault URL',
        description='URL for the Vault instance.'
    )
    token: Optional[SecretStr] = Field(
        '',
        title='Token',
        description='Token value to authenticate requests to Vault.'
    )
    verify_ssl: bool = Field(
        False,
        title='Verify SSL',
        description='Flag to decide if SSL verification should be enforced for Vault connection.'
    )
