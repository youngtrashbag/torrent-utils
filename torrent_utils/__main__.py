r"""
Torrent Utils

Usage:
    torrent_utils [--version] [--help] <command>  [<args>...]

Options:
    -h --help       Show help this menu
    --version       Show the current version

Commands:
    index       create and manage torrent index files
    magnet      create and manage magnet-link files
"""
import sys
from docopt import docopt

from torrent_utils.backend import Backend
from torrent_utils.torrent import Torrent

VERSION = 'v0.0.1'


def main():
    args = docopt(__doc__, version=VERSION, options_first=True)
    command = args['<command>']
    argv = [command] + args['<args>']

    if command == 'index':
        from torrent_utils.commands import index
        sys.exit(index.main(argv))
    if command == 'magnet':
        from torrent_utils.commands import magnet
        sys.exit(magnet.main(argv))
    else:
        print(f'"{command}" is not a valid command, please use --help to see a list of commands')
        sys.exit()

    qtorrent_url = 'http://localhost:8084'

    backend = Backend(qtorrent_url)

    if backend.authorize('admin', 'basedpiracy332'):
        print('auth success')
    else:
        print('auth fail')

    torrent_list = []
    for t in backend.torrent_list():
        torrent_list.append(Torrent.from_json(t))
    print('nice')


if __name__ == '__main__':
    main()
