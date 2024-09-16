import json
import requests
from src.tools.common import _try_get_env_var


class BearerAuth():
    def __init__(self):
        self.url = _try_get_env_var("PING_FED_URL")
        self.client_id = _try_get_env_var("KGW_CLIENT_ID")
        self.client_secret = _try_get_env_var("KGW_CLIENT_SECRET")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        response = requests.post(self.url, headers=headers, data=data)

        if not response.ok:
            raise Exception(f"Error: {response.status_code}, {response.text}")

        dict_of_response_text = json.loads(response.text)

        self.bearer_token = dict_of_response_text.get("access_token")
