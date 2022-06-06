"""
Providing datastructures for torrent
"""
from pathlib import Path
from typing import List, Dict, TypeVar

T = TypeVar('T', bound='Torrent')


class Torrent:
    """
    Stores relevant info of a torrent
    """

    def __init__(self, hash: str, magnet_uri: str,
                 save_path: Path, content_path: Path,
                 name: str, category: str, tags: List[str]):
        self.hash = hash
        """The hash is intended as a unique identifier"""
        self.magnet_uri = magnet_uri
        """Can be used to add the Torrent to a client"""
        self.save_path = save_path
        """Path of the Torrents save directory"""
        self.content_path = content_path
        """Path that points directly to the torrent itself"""
        self.name = name
        """Display name of the Torrent"""
        self.category = category
        """Category of Torrent"""
        self.tags = tags
        """List of tags"""

    @classmethod
    def from_json(cls, json_obj) -> T:
        """
        Load from
        :param json_obj: object that has been parsed with ``json.loads()``
        :return: Torrent
        """
        if tags := json_obj.get('tags'):
            if isinstance(tags, str):
                tags = json_obj.get('tags').split(',')
            else:
                tags = json_obj.get('tags')
        return Torrent(
            hash=json_obj.get('hash'),
            magnet_uri=json_obj.get('magnet_uri'),
            save_path=Path(json_obj.get('save_path')),
            content_path=Path(json_obj.get('content_path')),
            name=json_obj.get('name'),
            category=json_obj.get('category'),
            tags=tags
        )

    @property
    def __dict__(self) -> Dict:
        return {
            'hash': self.hash,
            'magnet_uri': self.magnet_uri,
            'save_path': str(self.save_path),
            'content_path': str(self.content_path),
            'name': self.name,
            'category': self.category,
            'tags': self.tags,
        }
