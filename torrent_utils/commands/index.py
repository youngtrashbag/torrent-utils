r"""
Usage:
    torrent_utils index <action> --file=FILE [<args>...]

Options:
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

from torrent_utils import util
from torrent_utils.backend import Backend
from torrent_utils.torrent import Torrent


def create_index(backend: Backend, file_path: Path):
    if os.path.exists(file_path):
        print(f'Overwriting file "{file_path}"')

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

    print(f'Wrote index to "{file_path}"')


def load_index(backend: Backend, file_path: Path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'"{file_path}" not found')

    torrents = []
    with open(Path(file_path), mode='r', encoding='UTF-8') as index_file:
        indexed_torrents = json.loads(index_file.read())
        for t in indexed_torrents:
            torrents.append(Torrent.from_json(t))

    for t in torrents:
        if backend.add_torrent(t):
            print(f'Successfully added "{t.name}" to client')
        else:
            print(f'Failed to add "{t.name}" to client')


def main(argv=None):
    kwargs = docopt(__doc__, argv=argv)

    action = kwargs['<action>']
    file_path = Path(kwargs.pop('--file'))

    credentials = util.get_credentials()
    backend = Backend(credentials)

    if action == 'create':
        create_index(backend, file_path)
    elif action == 'load':
        load_index(backend, file_path)
    else:
        print(f'"{action}" is not a valid action')
        sys.exit()


if __name__ == '__main__':
    main()
