r"""
This mode is used to copy subtitle files into the same directory of the video file.
The subtitle file will be renamed to the movie file, but the extension will be changed,
that way your media indexer will detect them automatically.

Usage:
    torrent_utils subtitle <action> --directory=DIRECTORY [<args>...]

Options:
    -d DIRECTORY --directory=DIRECTORY      directory where the video file is in (will recursively search for subtitle files)

Actions:
    copy            copies the subtitle file and renames it to the video file, with the correct extension
"""
import os
import shutil
import sys
from pathlib import Path

from docopt import docopt

# NOTE: there might be other extensions,
# please open a Pull Request if you notice that any extension may be missing
VIDEO_EXTENSIONS = [
    'mp4',
    'mov',
    'avi',
    'm4a',
]

SUBTITLE_EXTENSIONS = [
    'sub',
    'srt',
    'vtt',
    'ass',
    'ssa',
    'idx',
]


def copy(directory: Path):
    for dir_name, sub_dir, file_list in os.walk(directory):
        for file in file_list:
            extension = os.path.basename(file).split('.')[-1]

            if extension in VIDEO_EXTENSIONS:
                video_file = Path(dir_name) / file
            elif extension in SUBTITLE_EXTENSIONS:
                subtitle_file = Path(dir_name) / file
                try:
                    video_file
                except NameError:
                    continue

                new_subtitle_file = video_file.with_suffix(f'.{extension}')
                try:
                    shutil.copy(subtitle_file, new_subtitle_file)
                    print(f'Copied subtitle file "{subtitle_file}" to "{new_subtitle_file}".')
                except shutil.SameFileError:
                    print(f'Could not copy file "{subtitle_file}". Subtitle file"{new_subtitle_file}" already exists.')


def main(argv=None):
    kwargs = docopt(__doc__, argv=argv)

    action = kwargs['<action>']

    directory = Path(kwargs.pop('--directory'))

    if action == 'copy':
        copy(directory)
    else:
        print(f'"{action}" is not a valid action')
        sys.exit()
