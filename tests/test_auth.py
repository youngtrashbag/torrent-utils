import pytest
import requests
from urllib.parse import urlparse

from torrent_utils import backend
from . import constants


class MockRequests:
    def _torrent_info(self):
        res = requests.Response()
        setattr(res, 'json', lambda _: constants.TORRENTS_INFO_DICT)
        return res

    def get(self, url, *args, **kwargs):
        {
            '/api/v2/torrents/info': self._torrent_info
        }[urlparse(url).path]()

    def _auth_login(self, *args, **kwargs):
        data = args[0]

        if data != f'username={constants.USERNAME}&password={constants.PASSWORD}':
            pytest.fail()

        res = requests.Response()
        setattr(res, 'text', 'Ok.')

    def post(self, url, *args, **kwargs):
        {
            '/api/v2/auth/login': self._auth_login
        }[urlparse(url).path](*args, **kwargs)

    @property
    def headers(self):
        return {}


@pytest.fixture
def mock_requests(monkeypatch):
    # mock_req = MockRequests()

    # setattr(requests, 'get', mock_req.get)
    # setattr(requests, 'post', mock_req.post)
    setattr(requests, 'Session', MockRequests)


def test_credentials(mock_requests):
    # act
    creds = backend.Credentials(
        URL=constants.URL,
        username=constants.USERNAME,
        password=constants.PASSWORD
    )

    # assert

    backend.Backend(creds)


