"""
Backend for qBittorrent requests
"""

import requests
import json
from typing import List
from .torrent import Torrent


class NotAuthorizedError(Exception):
    pass


class Backend:
    """
    Fetches info from qBittorrent Web API
    """
    def __init__(self, url: str):
        """
        :param url: URL to qBittorrent Web Interface (e.g. http://192.168.1.1:8080)
        """
        self.authorized = False
        self.url = f'{url}/api/v2'
        self.session = requests.Session()
        self.session.headers.update({'Content-type': 'application/x-www-form-urlencoded'})

    def authorize(self, username: str, password: str) -> bool:
        """
        Authorizes this client in qBittorrent Web Interface
        :param username: username of the user
        :param password: password of the user
        :return: True if success, False if fail
        """
        data = f'username={username}&password={password}'
        response = self.session.post(f'{self.url}/auth/login', data)

        if response.text == 'Ok.':
            self.authorized = True
        else:
            self.authorized = False

        return self.authorized

    def torrent_list(self) -> List:
        """
        Fetches all torrents
        :return: List of Torrent objects as provided by qBittorrent
        """
        if not self.authorized:
            raise NotAuthorizedError

        response = self.session.get(f'{self.url}/torrents/info')
        return response.json()
