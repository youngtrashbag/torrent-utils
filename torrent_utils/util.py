import os

from torrent_utils.backend import Credentials
from torrent_utils.exceptions import NoCredentialsError

ENV_VARS = {
    'url': 'qbittorrent.url',
    'username': 'qbittorrent.username',
    'password': 'qbittorrent.password',
}


def get_credentials() -> Credentials:
    try:
        credentials = Credentials(
            URL=os.environ[ENV_VARS['url']],
            username=os.environ[ENV_VARS['username']],
            password=os.environ[ENV_VARS['password']],
        )
    except KeyError as e:
        raise NoCredentialsError(f'Could not find {e} in environment variables')

    return credentials
