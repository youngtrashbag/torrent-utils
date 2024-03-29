# Torrent Utils

## **IMPORTANT INFO**

**NO LONGER DEVELOPED ON GITHUB**

You can find the new repository on [codeberg.org](https://codeberg.org/goonli/torrent-utils)


## Usage

The credentials to your qBittorrent Client will be read from your environment.
- `source .credentials.env`

### `index`

#### `create`

`python -m torrent_utils index create --file=index.json`

Creates and file with metadata about your torrents
that are available in your qBittorrent client

#### `load`

`python -m torrent_utils index load --file=index.json`

Adds torrents from index.json to your qBittorrent client

### `magnet`

#### `create`

`python -m torrent_utils magnet create --directory=/media/movies`

Will create a file containing the magnet link to the torrent.
Also searches for Torrents in subdirectories

If `content_path` is a directory, magnet will be stored in it

Example:
If `content_path` is `/media/movies/american_psycho/` the Filepath will be:
`/media/movies/american_psycho/magnet`

But if `content_path` is `/media/movies/american_psycho.mp4` the Filepath will be:
`/media/movies/american_psycho.mp4.magnet`

#### `load`

`python -m torrent_utils magnet load --directory=/media/movies`

Will search subdirectories for magnet files, loads magnet files in similar way as described in *`create`*

#### `check`

`python -m torrent_utils magnet check --directory=/media/movies --verbose`

Checks if immediate Subirectories (`/media/movies/*/`) if they contain a `magnet` file.
Will print out those directories, which do **not** contain a `magnet` file.

Option `--verbose` or `-v` print a message for every directory scanned.

### `subtitle`

#### `copy`

`python -m torrent_utils subtitle copy --directory=/media/movies/eternal_sunshine_of_the_spotless_mind/`

Will recursively search subdirectories for subtitle files, and copy them to where the video file is located.

Supported file extensions:

- `.sub`
- `.srt`
- `.vtt`
- `.ass`
- `.ssa`
- `.idx`
