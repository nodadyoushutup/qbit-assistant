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


radarr_truenas = Radarr(host_url="http://192.168.0.100:9878", api_key="aec86fd08b3c49c9b8cef09de11b7102")


print(radarr_truenas)
# # with open('movies_cache.pkl', 'wb') as file:
# #     pickle.dump(radarr_truenas.get_movies(), file)

# def load_cached_movies():
#     with open('movies_cache.pkl', 'rb') as file:
#         cached_movies = pickle.load(file)
#     return cached_movies

# cached_movies = load_cached_movies()

# radarr_k3s = Radarr(hostname="http://192.168.0.200:30078", api_key="d9bac69600744fc6900565db46c1c87e")
# existing_roots = radarr_k3s.client.get_root_folder()

# def new_root_dir(existing_movie, existing_roots):
#     root_dirs = {
#         "/media/movies/mainstream/": "/media/movie_hardlink/mainstream",
#         "/media/movies/underground/": "/media/movie_hardlink/underground",
#         "/media/movies/short/": "/media/movie_hardlink/short",
#         "/media/movies/pre1960/": "/media/movie_hardlink/pre1960",
#         "/media/movies/temp/": "/media/movie_hardlink/temp",
#     }
#     new_root_path = root_dirs.get(existing_movie.get("rootFolderPath"))
#     matching_roots = [root['id'] for root in existing_roots if root['path'] == new_root_path]
#     id = matching_roots[0] if matching_roots else None
#     try:
#         return int(id)
#     except:
#         return None



# for movie in cached_movies:
#     imdbId = movie.get("imdbId")
#     tmdbId = movie.get("tmdbId")
#     root_dir = new_root_dir(movie, existing_roots)
        

#     if tmdbId:
#         term = f"tmdb:{tmdbId}"
#     elif imdbId:
#         term = f"tmdb:{imdbId}"
#     else:
#         logger.warning(f"{movie.title} has no TMDB or IMDB information")
#         continue
#     result = radarr_k3s.client.lookup_movie(term=term)
#     # logger.debug(result)
#     radarr_k3s.client.add_movie(
#         movie=result,
#         root_dir="/media/movie_hardlink/mainstream",
#         quality_profile_id=7,
#         monitored=True,
#         search_for_movie=False,
#         monitor="movieOnly",
#         minimum_availability="announced",
#         tags=[]
#     )
#     break

# download_clients = radarr_truenas.client.get_download_client()
# for download_client in download_clients:
#     try:
#         radarr_k3s.client.get_download_client(id_=download_client.get("id"))
#         radarr_k3s.client.upd_download_client(id_=download_client.get("id"), data=download_client)
#     except PyarrResourceNotFound as e:
#         # logger.error(e)
#         logger.info("Adding Download Client")
#         del download_client["id"]
#         download_client["fields"][5]["value"] = "S#nvhs89vher"
#         print(download_client)

#         radarr_k3s.client.add_download_client(data=download_client)
        
#     print(download_client.get("id"))
#     else:
#         radarr_k3s.client.add_download_client(data=download_client)


# print(var[0])