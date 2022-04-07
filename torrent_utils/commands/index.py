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
from docopt import docopt
from pathlib import Path

from torrent_utils.backend import Backend
from torrent_utils.torrent import Torrent


def main(argv=None):
    kwargs = docopt(__doc__, argv=argv)

    url = kwargs.pop('--url')
    username = kwargs.pop('--username')
    password = kwargs.pop('--password')
    file_path = kwargs.pop('--file')

    if os.path.exists(Path(file_path)):
        raise RuntimeError('Cannot overwrite file')

    backend = Backend(url)

    if not backend.authorize(username, password):
        raise RuntimeError('Could not authorize in qBittorrent Web API')

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


if __name__ == '__main__':
    main()
