"""
Create a json file that contains an array of relevant data for each torrent

Works only with qBittorrent WebUI running
"""

import os
import json
import argparse
from pathlib import Path

from torrent_utils.backend import Backend
from torrent_utils.torrent import Torrent


def create_magnet(t: Torrent):
    magnet_path = t.content_path / 'magnet'
    if not os.path.isdir(t.content_path):
        magnet_path = t.content_path.parent / f'magnet_{t.hash}'

    with open(magnet_path, mode='w', encoding='UTF-8') as magnet:
        magnet.write(t.toJSON())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outfile',
                        help='path to the newly created index file',
                        required=True)
    parser.add_argument('--save-magnet',
                        help='add this flag to create magnet files belonging to the torrents',
                        action='store_true')
    args = parser.parse_args()

    if os.path.exists(Path(args.outfile)):
        raise RuntimeError('Cannot overwrite file')

    backend = Backend('http://localhost:8084')

    if not backend.authorize('admin', 'basedpiracy332'):
        raise RuntimeError('Could not authorize in qBittorrent Web API')

    torrents = []
    for t in backend.torrent_list():
        torrent = Torrent.from_json(t)
        torrents.append(torrent)

        if args.save_magnet:
            create_magnet(t)

    with open(Path(args.outfile), mode='w', encoding='UTF-8') as index_file:
        index_file.write(
            json.dumps(
                [t.__dict__ for t in torrents]
            )
        )


if __name__ == '__main__':
    main()
