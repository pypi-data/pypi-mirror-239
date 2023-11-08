##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Any
from pydantic import ValidationError
from keycloak import KeycloakAdmin

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.keycloak import KeycloakSchema


class KeycloakConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            keycloakCredential = KeycloakSchema(**data)
        except ValidationError as e:
            raise e
        
        username = keycloakCredential.username if keycloakCredential.username else None
        password = keycloakCredential.password.get_secret_value() if keycloakCredential.password else None
        client_secret = keycloakCredential.client_secret.get_secret_value() if keycloakCredential.client_secret else None
        client_id = keycloakCredential.client_id if keycloakCredential.client_id else None
        verify = keycloakCredential.verify if keycloakCredential.verify else True

        try:
            # username and password authentication
            if username and password:
                keycloakClient = KeycloakAdmin(
                    server_url=keycloakCredential.server_url,
                    username=username,
                    password=password,
                    realm_name=keycloakCredential.realm,
                    verify=verify
                )
            # client_id and client_secret authentication
            elif client_id and client_secret:
                keycloakClient = KeycloakAdmin(
                    server_url=keycloakCredential.server_url,
                    client_id=client_id,
                    client_secret_key=client_secret,
                    realm_name=keycloakCredential.realm,
                    verify=verify
                )
            else:
                raise ValueError("Either username/password or client_id/client_secret must be provided for authentication.")

        except Exception as e:
            raise e

        return keycloakClient
