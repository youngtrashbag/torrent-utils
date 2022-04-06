"""
Providing datastructures for torrent
"""
import json
from typing import List
from pathlib import Path


class Torrent:
    """
    Stores relevant info of a torrent
    """
    def __init__(self, hash: str, magnet_uri: str, content_path: Path, name: str, category: str, tags: List[str]):
        self.hash = hash
        """The hash is intended as a unique identifier"""
        self.magnet_uri = magnet_uri
        """Can be used to add the torrent to a client"""
        self.content_path = content_path
        """Path to the directory/file downloaded"""
        self.name = name
        """Display name of the torrent"""
        self.category = category
        """Category of torrent"""
        self.tags = tags
        """List of tags"""

    @classmethod
    def from_json(cls, json_obj) -> 'Torrent':
        """
        Load from
        :param json_obj: object that has been parsed with ``json.loads()``
        :return: Torrent
        """
        return Torrent(
            hash=json_obj.get('hash'),
            magnet_uri=json_obj.get('magnet_uri'),
            content_path=Path(json_obj.get('content_path')),
            name=json_obj.get('name'),
            category=json_obj.get('category'),
            tags=json_obj.get('tags').split(',')
        )

    def to_json(self) -> str:
        return json.dumps(self)
