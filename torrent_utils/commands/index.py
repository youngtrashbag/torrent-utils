r"""
Usage:
    torrent_utils index <action> --url=URL --username=USERNAME --password=PASSWORD --file=FILE [<args>...]

Options:
    --url=URL               URL to the qBittorrent WebUI
    --username=username     Username for WebUI
    --password=password     Password for WebUI
    -f FILE --file=FILE     path to index file

Actions:
    create                  creates an index file
    load                    load and add torrents from index file to client
"""

import os
import json
import sys

from docopt import docopt
from pathlib import Path

from torrent_utils.backend import Backend
from torrent_utils.torrent import Torrent


def create_index(backend: Backend, file_path: Path):
    if os.path.exists(file_path):
        raise FileExistsError('Cannot overwrite file')

    torrents = []
    for t in backend.torrent_list():
        torrent = Torrent.from_json(t)
        torrents.append(torrent)

    with open(Path(file_path), mode='w', encoding='UTF-8') as index_file:
        index_file.write(
            json.dumps(
                [t.__dict__ for t in torrents],
                indent=4
            )
        )


def main(argv=None):
    kwargs = docopt(__doc__, argv=argv)

    action = kwargs['<action>']

    url = kwargs.pop('--url')
    username = kwargs.pop('--username')
    password = kwargs.pop('--password')
    file_path = Path(kwargs.pop('--file'))

    backend = Backend(url)
    if not backend.authorize(username, password):
        raise RuntimeError('Could not authorize in qBittorrent Web API')

    if action == 'create':
        create_index(backend, file_path)
    elif action == 'load':
        pass
    else:
        print(f'"{action}" is not a valid action')
        sys.exit()


if __name__ == '__main__':
    main()
