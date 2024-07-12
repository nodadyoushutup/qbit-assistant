from time import sleep
from vulcan_utils.logger import Logger
from qbittorrentapi import Client, LoginFailed, TrackerStatus
from collections import defaultdict
from collections import defaultdict
from qbittorrent import Qbittorrent
from pyarr.exceptions import PyarrResourceNotFound
import pickle
from radarr import Radarr

logger = Logger(__name__)

# qbittorrent = Qbittorrent()
# qbittorrent.recategorize_bad_ext()


radarr_truenas = Radarr(host_url="http://192.168.1.100:9878", api_key="")
radarr_k3s = Radarr(host_url="http://192.168.1.200:30078", api_key="")
cached_movies = radarr_truenas.get_movie()
radarr_k3s.migrate_movies(cached_movies)
