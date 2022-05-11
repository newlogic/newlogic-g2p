#
# Copyright (c) 2022 Newlogic.
#
# This file is part of newlogic-g2p-erp.
# See https://github.com/newlogic/newlogic-g2p-erp/ for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.#

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
        params = {"$top": top, "$skip": skip, "$count": "true"}

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
