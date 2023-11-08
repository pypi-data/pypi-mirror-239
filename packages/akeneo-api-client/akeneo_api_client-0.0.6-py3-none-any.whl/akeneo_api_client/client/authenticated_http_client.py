from requests.models import Response

from akeneo_api_client.api.request.json_serializable import JsonSerializable


class AuthenticatedHttpClient:

    def __init__(self, http_client, authentication, authentication_api):
        self.http_client = http_client
        self.authentication = authentication
        self.authentication_api = authentication_api

    def send_request(self, method: str, uri: str, headers: dict = {}, body: JsonSerializable = None) -> Response:
        if self.authentication.access_token == "":
            tokens = self.authentication_api.authenticate_by_password(
                self.authentication.username,
                self.authentication.password,
                self.authentication.client_id,
                self.authentication.secret
            )

            self.authentication.access_token = tokens["access_token"]
            self.authentication.refresh_token = tokens["refresh_token"]

        headers["Authorization"] = "Bearer " + self.authentication.access_token
        return self.http_client.send_request(method, uri, headers, body)