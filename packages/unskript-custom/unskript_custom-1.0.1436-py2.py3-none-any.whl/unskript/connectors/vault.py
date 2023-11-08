##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Any
import hvac
from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.vault import VaultSchema

class VaultConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            vaultCredential = VaultSchema(**data)
        except ValidationError as e:
            raise e

        client = hvac.Client(url=vaultCredential.url, verify=vaultCredential.verify_ssl)

        if vaultCredential.token:
            client.token = vaultCredential.token.get_secret_value()
        
        # Check if authentication is successful
        if not client.is_authenticated():
            raise ValueError("Failed to authenticate with Vault.")

        return client
