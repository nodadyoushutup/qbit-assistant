import pickle
from typing import Any, Literal
from pyarr.radarr import RadarrAPI
from pyarr.types import JsonArray, JsonObject
from vulcan_utils.logger import Logger

logger = Logger(__name__)

class Radarr(RadarrAPI):
    def get_movie(self, id_: int | None = None, tmdb: bool = False) -> list[dict[str, Any]] | dict[str, Any]:
        logger.info(f"Retrieving movie(s) from Radarr")
        movies = super().get_movie(id_, tmdb)
        logger.info(f"Movies successfully retrieved from Radarr")
        return movies
    
    def get_movie_cache(self):
        logger.info(f"Retrieving movies from Radarr cache")
        with open('movies_cache.pkl', 'rb') as file:
            movies = pickle.load(file)
            logger.info(f"Movies retrieved from Radarr cache")
            return movies
        
    def add_movie_cache(self):
        logger.info(f"Caching movies from Radarr")
        with open('movies_cache.pkl', 'wb') as file:
            pickle.dump(self.get_movie(), file)
            logger.info(f"Movies successfully saved to Radarr cache")

    def add_movie(self, movie: JsonObject[str],
        root_dir: str,
        quality_profile_id: int,
        monitored: bool = True,
        search_for_movie: bool = True,
        monitor: Literal['movieOnly'] | Literal['movieAndCollections'] | Literal['none'] = "movieOnly",
        minimum_availability: Literal['announced'] | Literal['inCinemas'] | Literal['released'] = "announced", tags: JsonArray[int] = ...
    ) -> JsonObject[str]:
        if movie:
            title = movie.get("title")
            logger.info(f"Successfully added {title} to {root_dir}")
            return super().add_movie(  
                movie, 
                root_dir, 
                quality_profile_id, 
                monitored, 
                search_for_movie, 
                monitor, 
                minimum_availability, 
                tags
            )
    
    def _get_new_root_dir(self, movie):
        root_dirs = {
            "/media/movies/mainstream/": "/media/movie_hardlink/mainstream",
            "/media/movies/underground/": "/media/movie_hardlink/underground",
            "/media/movies/short/": "/media/movie_hardlink/short",
            "/media/movies/pre1960/": "/media/movie_hardlink/pre1960",
            "/media/movies/temp/": "/media/movie_hardlink/temp",
        }
        return root_dirs.get(movie.get("rootFolderPath"))
    
    def migrate_movies(self, movies):
        total = len(movies)
        count = 0
        for movie in movies:
            imdbId = movie.get("imdbId")
            tmdbId = movie.get("tmdbId")
            print(tmdbId, imdbId)
            root_dir = self._get_new_root_dir(movie)
            title = movie.get('title')
            if tmdbId:
                term = f"tmdb:{tmdbId}"
            elif imdbId:
                term = f"tmdb:{imdbId}"
            else:
                logger.warning(f"{title} has no TMDB or IMDB information")
                continue
            existing = self.get_movie(id_=tmdbId, tmdb=True)
            if existing:
                logger.warning(f"{tmdbId} {title} already exists in library")
                continue
            result = self.lookup_movie(term=term)
            if result:
                result = result[0]
            count += 1
            if count / 100 == 0:
                logger.warning(f"({count}/{total})")
            self.add_movie(
                movie=result,
                root_dir=root_dir,
                quality_profile_id=1,
                monitored=True,
                search_for_movie=False,
                monitor="movieOnly",
                minimum_availability="announced",
                tags=[]
            )
