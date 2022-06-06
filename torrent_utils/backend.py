"""
Backend for qBittorrent requests
"""

from dataclasses import dataclass
from typing import List

import requests

from torrent_utils.exceptions import FailedAuthorizeError
from torrent_utils.torrent import Torrent


@dataclass
class Credentials:
    """Credentials for the qBittorrent Client"""

    URL: str
    """URL to qBittorrent Web Interface (e.g. http://192.168.1.1:8080)"""
    username: str
    """username for the web interface"""
    password: str
    """password for the web interface"""


class Backend:
    """
    Fetches info from qBittorrent Web API
    """

    def __init__(self, credentials: Credentials):
        """
        :param credentials: Credentials object
        """
        self.url = f'{credentials.URL}/api/v2'
        self.session = requests.Session()

        if not self._authorize(credentials.username, credentials.password):
            raise FailedAuthorizeError('Could not authorize in qBittorrent Web API')

    def _authorize(self, username: str, password: str) -> bool:
        """
        Authorizes this client in qBittorrent Web Interface
        :param username: username of the user
        :param password: password of the user
        :return: True if success, False if fail
        """
        data = f'username={username}&password={password}'
        self.session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        response = self.session.post(f'{self.url}/auth/login', data)
        self.session.headers.pop('Content-Type')

        if response.text == 'Ok.':
            return True
        return False

    def torrent_list(self) -> List:
        """
        Fetches all torrents
        **Note**: the objects in the list are not Torrent objects
        :return: List of objects as provided by qBittorrent
        """
        response = self.session.get(f'{self.url}/torrents/info')
        return response.json()

    def add_torrent(self, torrent: Torrent) -> bool:
        """
        Will add a torrent to the client
        :param torrent: Torrent instance
        :return: True if success, False if fail
        """
        data = {
            'urls': (None, torrent.magnet_uri),
            'savepath': (None, str(torrent.save_path)),
            'category': (None, torrent.category or None),
            'tags': (None, ','.join(torrent.tags) or None),
        }

        response = self.session.post(f'{self.url}/torrents/add', files=data)
        if response.text == 'Ok.':
            return True
        return False
