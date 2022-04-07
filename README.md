# Torrent Utils

Manage your Torrents in the qBittorrent client *easily*.

## Usage

### `index`

#### `create`

`python -m torrent_utils index create --file=index.json`

Creates and file with metadata about your torrents
that are available in your qBittorrent client

#### `load`

`python -m torrent_utils index load --file=index.json`

Adds torrents from index.json to your qBittorrent client
