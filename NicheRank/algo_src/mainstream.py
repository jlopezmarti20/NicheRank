from typing import Dict, List
from dataclasses import dataclass

import taste_user as ut
import music_dataclass as md
from sorting import Local_Sort, Popularity_Sort
from extraction import Stats_Extractor

"""
    THIS IS THE MOST IMPORTANT CLASS!!! Takes your listening history 
    and outputs metrics based on it 

    TODO: create mainstream calcualtor function

"""

@dataclass
class Artist_Metrics:
    favorites: List[md.Artist_Stat]
    most_popular: List[md.Artist_Stat]
    num_listened: int

@dataclass
class Song_Metrics:
    favorites: List[md.Song_Stat]
    most_popular: List[md.Song_Stat]
    num_listened: int

@dataclass
class User_Metrics:
    # data to be returned after analyzing
    artist_metrics: Artist_Metrics
    song_metrics: Song_Metrics
    pop_score: float # val from 0 to 100 of how popular this persons taste is+
    time_listened_s: float


# Behavior Class
class Mainstream_Engine():

    def analyze_history(history: List[md.Song], global_AS_map=None, global_SS_map=None) -> User_Metrics:

        # list artists ordered by listening metric descending

        artist_history_stats: List[md.Artist_Stat] = Stats_Extractor.history_AS_extract(history) 
        favorite_artists: List[md.Artist_Stat] = Local_Sort.merge_sort(artist_history_stats)

        if global_AS_map is not None:
            popular_artists: List[md.Artist_Stat] = Popularity_Sort.merge_sort(artist_history_stats, global_AS_map)
            least_popular_artists = popular_artists.reverse()

        # get song metrics
        song_history_stats: List[md.Song_Stat] = Stats_Extractor.history_SS_extract(history)
        favorite_songs: List[md.Song_Stat] = Local_Sort.merge_sort(song_history_stats)

        if global_SS_map is not None:
            popular_songs = Popularity_Sort.merge_sort(song_history_stats, global_SS_map)  

        time_listened_s = sum(artist_stat.total_s for artist_stat in artist_history_stats)
        pop_score = Mainstream_Engine.calculate_mainstream_score()


    def calculate_mainstream_score(history: List[md.Song], global_AS_map: Dict[str, md.Artist_Stat]) -> float:
        # Finds your mainstream score based off of your artists listening history

        pass

    def list_allignment_MS(fav_AS_sorted: List[md.Artist_Stat], popularity_sorted) -> float:
        # compares 2 lists sorted by favorite vs popularity to see how well they are alligned.
        pass

    def global_map_allignment_MS(fav_AS_sorted: List[md.Artist_Stat], AS_global_map, total_listens) -> float:
        # calculates based off how much you listen to an artist
        total_global_songs = sum( artist.total_songs for uri, artist in AS_global_map.items()) 
        
        score = 0
        for i, (artist_stat) in enumerate(fav_AS_sorted):
            # smaller i is, more popular artist is 
            pass