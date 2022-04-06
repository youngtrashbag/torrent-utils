from .backend import Backend
from .torrent import Torrent

qtorrent_url = 'http://localhost:8084'

backend = Backend(qtorrent_url)

if backend.authorize('admin', 'admin'):
    print('auth success')
else:
    print('auth fail')

torrent_list = []
for t in backend.torrent_list():
    torrent_list.append(Torrent.from_json(t))
print('nice')
