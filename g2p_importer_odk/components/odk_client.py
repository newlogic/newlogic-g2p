# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.

import requests

SSL_VERIFY = True


class ODKClient:
    def __init__(self, url, email, password):
        self.base_url = url.split("/v1/")[0]
        self.url = url
        self.email = email
        self.password = password

        self.header_token = None
        self.session = requests.Session()

    def _get_odk_login_token(self):
        url = f"{self.base_url}/v1/sessions"
        response = requests.post(
            url,
            json={"email": self.email, "password": self.password},
            verify=SSL_VERIFY,
        )
        response.raise_for_status()
        data = response.json()

        token = data["token"]
        return {"Authorization": f"Bearer {token}"}

    def get_header_token(self):
        if self.header_token is None:
            self.header_token = self._get_odk_login_token()
        return self.header_token

    def get_responses(self, skip=0, top=100):
        url = f"{self.url}/Submissions"
        params = {"$top": top, "$skip": skip, "$count": "true", "$expand": "*"}

        response = requests.get(
            url, headers=self.get_header_token(), params=params, verify=SSL_VERIFY
        )
        response.raise_for_status()
        data = response.json()
        return data

    def count(self):
        url = f"{self.url}/Submissions"
        params = {"$top": 0, "$count": "true"}
        response = requests.get(
            url, headers=self.get_header_token(), params=params, verify=SSL_VERIFY
        )
        response.raise_for_status()
        data = response.json()
        return data["@odata.count"]
