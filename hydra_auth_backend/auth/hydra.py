import json

import requests

from hydra_auth_backend.auth import settings


class Hydra(object):
    def __init__(self, api_key=None, access_token=None):
        self._access_token = None
        if not api_key:
            self.api_key = settings.HYDRA_API_KEY
        else:
            self.api_key = api_key

        if access_token:
            self.access_token = access_token

        self._default_headers = {
            "x-hydra-api-key": settings.HYDRA_API_KEY,
            "content-type": "application/json"
        }

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, token):
        self._access_token = token

    def headers(self, custom_headers=None):
        if not custom_headers:
            custom_headers = {}
        heads = self._default_headers.copy()
        heads.update(custom_headers)

        if self.access_token and 'x-hydra-access-token' not in heads:
            heads['x-hydra-access-token'] = self.access_token
        return heads


    def post(self, url, *args, **kwargs):
        kwargs['headers'] = self.headers(kwargs.pop('headers', {}))
        return requests.post("%s/%s" % (settings.HYDRA_URL, url), *args,
                             **kwargs)

    def get(self, url, *args, **kwargs):
        kwargs['headers'] = self.headers(kwargs.pop('headers', {}))
        return requests.get("%s/%s" % (settings.HYDRA_URL, url), *args, **kwargs)

    def put(self, url, *args, **kwargs):
        kwargs['headers'] = self.headers(kwargs.pop('headers', {}))
        return requests.put("%s/%s" % (settings.HYDRA_URL, url), *args, **kwargs)

    def authenticate(self, username, password):
        response = self.post('auth', json.dumps(
            {"user": {"username": username, "password": password}}))

        if not response.ok:
            return False

        auth_token = response.json()['token']
        access = self.post('access', json.dumps({'auth_token': auth_token}))

        if not access.ok:
            return False

        self.access_token = access.json()['token']
        return True

    def account(self, hid="me"):
        return self.get("accounts/%s" % hid).json()

    def profile(self, hid="me"):
        return self.get("profiles/%s" % hid).json()
