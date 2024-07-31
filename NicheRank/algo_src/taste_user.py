
import os
from typing import List, Tuple, Dict

import json_parsing
import music_dataclass as md

"""
    insert a spotify listening history json file and store, then output top songs, top artists etc

"""

default_recently_played = "idk" #! change this to config data!

class User_Taste():


    """
        Loads and handles an individuals spotify taste
    
    """

    def __init__(self, spotify_history_file:str) -> None:
        # history_location: string of where spotify json file is
        self.spotify_history_file = spotify_history_file 
        self.artist = []
        self.songs_metrics = None

        pass

    def process_user_history(self, song_history: List[md.Song])->None:
        # TODO process and store a users favorite artists based on time listened  
        pass        
        # sort this list with merge sort?
        # put this list into a heap?

    def get_favorite_artists(self, n=None):
        # Return n favorite artists
        if (self.artists_metrics is None):
            return None
        
        # get all
        n = self.unique_artists_listened() if n is None else n
        
        pass

    def get_favorite_songs(self, n=None):
        # Return n Favorite songs
        if (self.songs_metrics is None):
            return None

        n = self.unique_songs_listened() if n is None else n


        pass 

    def unique_artists_listened(self)->int:
        # total artists youve listened to 
        pass

    def unique_songs_listened(self)->int:
        # total unique songs youve listened to
        pass