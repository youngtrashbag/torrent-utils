r"""
Usage:
    torrent_utils magnet <action> --url=URL --username=USERNAME --password=PASSWORD --directory=DIRECTORY [<args>...]

Options:
    --url=URL                               URL to the qBittorrent WebUI
    --username=username                     Username for WebUI
    --password=password                     Password for WebUI
    -d DIRECTORY --directory=DIRECTORY      directory where the torrents are

Actions:
    create          creates a ``magnet`` file containing the magnet URI for each torrent
    load            loads the magnet files and add torrents from index file to client
"""
import os
import sys
from pathlib import Path
from typing import List
from docopt import docopt

from torrent_utils.backend import Backend
from torrent_utils.torrent import Torrent


def create_magnet(t: Torrent) -> Path:
    """
    Creates a magnet file containing the magnet link for a torrent
    :param t: Torrent instance
    :return: Path to the magnet file
    """
    magnet_path = t.content_path / 'magnet'
    if not os.path.isdir(t.content_path):
        magnet_path = t.content_path.parent / f'{os.path.basename(t.content_path)}.magnet'

    with open(magnet_path, mode='w', encoding='UTF-8') as magnet:
        magnet.write(t.magnet_uri)

    return magnet_path


def create(backend: Backend, directory: Path) -> List[Path]:
    """
    Creates a magnet file for each torrent in the directory

    (Note: magnets for torrents in subdirectories of *directory* will be added as well)
    :param backend:
    :param directory: The directory, which contains the torrents
    :return: List of magnet-file Paths
    """
    path_list = []

    for t in backend.torrent_list():
        torrent = Torrent.from_json(t)

        if directory.parent in torrent.save_path.parents:
            magnet_path = create_magnet(torrent)
            print(f'Created "{magnet_path}"')
            path_list.append(magnet_path)

    return path_list


def load(backend: Backend, directory: Path):
    pass


def main(argv=None):
    kwargs = docopt(__doc__, argv=argv)

    action = kwargs['<action>']

    url = kwargs.pop('--url')
    username = kwargs.pop('--username')
    password = kwargs.pop('--password')
    directory = Path(kwargs.pop('--directory'))

    backend = Backend(url, username, password)

    if action == 'create':
        create(backend, directory)
    elif action == 'load':
        load(backend, directory)
    else:
        print(f'"{action}" is not a valid action')
        sys.exit()


if __name__ == '__main__':
    main()
