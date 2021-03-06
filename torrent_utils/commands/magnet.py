r"""
Usage:
    torrent_utils magnet <action> --directory=DIRECTORY [--verbose] [<args>...]

Options:
    -d DIRECTORY --directory=DIRECTORY      directory where the torrents are
    -v --verbose                            verbose output

Actions:
    create          creates a ``magnet`` file containing the magnet URI for each torrent
    load            loads the magnet files and add torrents from index file to client
    check           checks with subdirectories of directory, if a magnet file is in its folders
"""
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

from docopt import docopt

from torrent_utils import util
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


@dataclass
class MagnetFile:
    """Provides data for torrent to be loaded via magnet file"""
    magnet_uri: str
    save_path: Path
    category = None
    tags = []


def load(backend: Backend, directory: Path, verbose: bool = False):
    for dir_name, sub_dir, file_list in os.walk(directory):
        for file in file_list:
            if os.path.basename(file).split('.')[-1] == 'magnet':
                magnet_path = Path(dir_name) / file
                save_path = Path(dir_name).parent
                magnet_uri = open(magnet_path, mode='r', encoding='UTF-8').read()

                # creating a object with only required attributes
                magnet_file = MagnetFile(magnet_uri=magnet_uri, save_path=save_path)
                success = backend.add_torrent(magnet_file)
                if not success:
                    print(f'Failed to add "{magnet_path}" to client')
                elif success and verbose:
                    print(f'Successfully added "{magnet_path}" to client')


def check(directory: Path, verbose: bool = False):
    for f in os.scandir(directory):
        if f.is_dir():
            magnet_file_path = Path(f.path) / 'magnet'
            if not magnet_file_path.exists():
                print(f'Magnet NOT found in dir {f.path}')
            elif magnet_file_path.exists() and verbose:
                print(f'Magnet file found in dir {f.path}')


def main(argv=None):
    kwargs = docopt(__doc__, argv=argv)

    action = kwargs['<action>']
    directory = Path(kwargs.pop('--directory'))

    if action == 'check':
        check(directory, verbose=kwargs.pop('--verbose', False))
        sys.exit()

    credentials = util.get_credentials()
    backend = Backend(credentials)

    if action == 'create':
        create(backend, directory)
    elif action == 'load':
        load(backend, directory, verbose=kwargs.pop('--verbose', False))
    else:
        print(f'"{action}" is not a valid action')
        sys.exit()


if __name__ == '__main__':
    main()
