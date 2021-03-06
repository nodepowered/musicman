"""
Hi im logman. I take care of logging history of played tracks. I also help
remembering queued songs in case of restart BUT NOT YET SO COOL YOUR JETS.
"""

import datetime
import pymongo
import atexit

from pymongo.errors import OperationFailure, ServerSelectionTimeoutError


class Logman():

    def __init__(self, mongodb_uri):
        self.connection = pymongo.MongoClient(mongodb_uri)
        self.db = self.connection.get_default_database()
        self.musichistory = self.db['musichistory']
        atexit.register(self._disconnect)

    def _disconnect(self):
        self.connection.close()

    def log_song(self, entry):
        """Use this to log a song to play history."""

        song = {
            'playedAt': datetime.datetime.now(),
            'title': entry.title,
            'url': entry.url
        }
        
        if hasattr(entry.meta, 'author'):
            song.requestedBy = str(entry.meta['author'].id)

        try:
            self.musichistory.insert(song)

        except (OperationFailure, ServerSelectionTimeoutError):
            print("[Logman] \"im hev trouble comunicating with mongodb. "
                  "Cud be wrong login info or bad uri :<\"")
