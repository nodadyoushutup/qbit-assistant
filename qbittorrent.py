from time import sleep
from vulcan_utils.logger import Logger
from qbittorrentapi import Client, LoginFailed, TrackerStatus
from collections import defaultdict
from pyarr import RadarrAPI
from radarr import Radarr
from collections import defaultdict


logger = Logger(__name__)

ALLOWED_EXT_VIDEO = ["mkv", "mp4", "avi", "mov", "wmv", "m4v", "mpeg", "mpg"]
ALLOWED_EXT_SUBTITLE = ["srt", "sub", "idx", "ass"]
ALLOWED_EXT_AUDIO = ["mp3", "flac", "aac", "ogg", "wav"]
ALLOWED_EXT_IMAGE = ["jpg", "jpeg", "png"]
ALLOWED_EXT_DOCUMENT = ["nfo", "txt", "pdf"]

ALLOWED_EXT = (
    ALLOWED_EXT_VIDEO + 
    ALLOWED_EXT_SUBTITLE + 
    ALLOWED_EXT_AUDIO +
    ALLOWED_EXT_IMAGE + 
    ALLOWED_EXT_DOCUMENT
)
counts = defaultdict(int)  # Initialize counts with defaultdict

# radarr = Radarr()

class Qbittorrent():
    def __init__(self) -> None:
        conn_info = dict(
            host="192.168.1.100",
            port=10095,
            username="admin",
            password="",
        )
        self.client = Client(**conn_info)
        self.radarr = None

        try:
            self.client.auth_log_in()
        except LoginFailed as e:
            logger.error(e)


        logger.info(f"Caching {self.client.torrents_count()} torrents...")
        self.torrents = self.client.torrents_info()
        logger.info("Caching completed")

        logger.info("Searching for torrents with errored tracker status")



    def pause(self, torrent):
        tags = ["issue"]
        torrent.add_tags(tags=tags)
        torrent.pause()
        logger.info(f"{torrent.name} tagged with {tags} and paused")

    def tag_orphan(self, torrent):
        tags = ["orphan"]
        torrent.add_tags(tags=tags)
        logger.warning(f"{torrent.name} tagged with {tags}")

    def refresh_untag(self, torrent):
        tags = ["issue"]
        torrent.remove_tags(tags=tags)
        logger.warning(f"{torrent.name} untagged with {tags}")

    def refresh(self, torrent, attempts=1, delay=1, attempt=1):
        logger.info(f"Attempt {attempt} to refresh {torrent.name}")
        torrent.pause()
        torrent.reannounce()
        sleep(delay)
        torrent.start()
        for tracker in torrent.trackers:
            if "http" in tracker.url and tracker.status == 2:
                logger.critical(f"{torrent.name} is now working on tracker {tracker.url}")
                self.refresh_untag(torrent)
                return True
        if attempt < attempts:
            return self.refresh(torrent, attempts, delay, attempt + 1)
        logger.info(f"{torrent.name} is still not working after max attempts")
        return False

    def tag(torrent):
        for file in torrent.files:
            movie = self.radarr.tag_movie(file.name)
            if not movie:
                return self.tag_orphan(torrent)
            return False

    # for torrent in torrents:
    #     working = False
    #     for tracker in torrent.trackers:
    #         if "http" in tracker.url:
    #             if tracker.status == 2:
    #                 working = True
    #                 break
    #             elif tracker.status == 4:
    #                 if not refresh(torrent):
    #                     pause(torrent)
    #                     logger.debug(tracker.msg)
    #                     tag(torrent)


    def recategorize_bad_ext(self):
        for torrent in self.torrents:
            for file in torrent.files:
                ext = file.name.split(".")[-1].lower()
                if ext not in ALLOWED_EXT:
                    counts[ext] += 1  # Increment count for this extension
                    logger.info(f"Scanning {file.name}")
                    torrent.set_category(category="issue")
                    torrent.pause()
                    break  # Move to the next torrent as soon as a bad file is found
        print(counts)
