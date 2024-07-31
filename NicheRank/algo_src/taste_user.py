
import os
from typing import List, Tuple, Dict

import music_dataclass as md
from extraction import Stats_Extractor
from sorting import Stat_Sorter

# we need an extractor class to extract stats from just songs

# storage and loading of users taste
class User_Taste():

    """
        Loads and handles an individuals spotify taste
    
    """

    def __init__(self, song_history:List[md.Song]) -> None:
        # song history is a list of a users listening history
        self.favorite_artists_list:List[md.Song] = []
        self.favorite_songs_list: List[md.Song] = []
        self._setup_sorted_stats(song_history)
        
        # get sumation of these 2 metrics
        self.total_songs_listened = sum(artist_stat.total_songs for artist_stat in self.favorite_artists_list)
        self.total_seconds_listened = sum(artist_stat.total_s for artist_stat in self.favorite_artists_list)
        
        pass

    def _setup_sorted_stats(self, song_history:List[md.Song]):
        artist_stats_dict = {}
        song_stats_dict = {}
        Stats_Extractor.extract_artiststats(song_history, artist_stats_dict, type="artist")
        Stats_Extractor.extract_songstats(song_history, song_stats_dict, type="song")
        self.fav_artists_list = Stat_Sorter.merge_sort([artist_stat for uri, artist_stat in artist_stats_dict.items()])
        self.fav_songs_list = Stat_Sorter.merge_sort([song_stat for uri, song_stat in song_stats_dict.items()])

    def get_fav_AS(self, n=None)-> List[md.Artist_Stat]:
        # Return n Favorite Artists (As stats)
        n = len(self.fav_artists_list) if n is None else n
        return self.fav_artists_list[-n:]

    def get_fav_SS(self, n=None) -> List[md.Song_Stat]:
        # Return n Favorite Songs(As stats)
        n = len(self.fav_songs_list) if n is None else n
        return self.fav_songs_list[:n]

    def get_A_stat(self, index) -> md.Artist_Stat:
        return self.fav_artists_list[index]

    def get_S_stat(self, index) -> md.Song_Stat:
        return self.fav_songs_list[index]