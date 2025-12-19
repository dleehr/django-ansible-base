import logging
import time

import requests

from ansible_base.resource_registry.resource_server import get_resource_server_config, get_service_token

logger = logging.getLogger('ansible_base.workload_identity.client')

from django.conf import settings


class WorkloadIdentityClient:

    header_name = "X-ANSIBLE-SERVICE-AUTH"
    _jwt_timeout = None
    _jwt = None

    def __init__(self, service_url: str, jwt_user_id=None, jwt_expiration=60) -> None:
        self.service_url = service_url
        self.jwt_user_id = jwt_user_id
        self.jwt_expiration = jwt_expiration
        self._jwt = None
        self._jwt_timeout = None

    @property
    def jwt(self):
        if self._jwt is None or self._jwt_timeout is None or time.time() >= self._jwt_timeout:
            self.refresh_jwt()
        return self._jwt

    def refresh_jwt(self):
        # Add a buffer to the token timeout to account for slower requests.
        self._jwt_timeout = time.time() + (self.jwt_expiration - 2)
        # user id is likely None, we should set this
        self._jwt = get_service_token(self.jwt_user_id, expiration=self.jwt_expiration)

    def create_workload_identity_token(self, data: dict):
        # make a request to /workload_identity_tokens
        url = f"{self.service_url}/api/gateway/v1/workload_identity_tokens/"
        response = requests.post(
            url=url,
            data=data,
            headers={self.header_name: self.jwt},
        )
        response.raise_for_status()
        # If we succeeded, JWT will be in jwt
        return response.json()
