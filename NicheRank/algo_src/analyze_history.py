from typing import Dict, List
from dataclasses import dataclass

import music_dataclass as md
from sorting import StatSorter, GlobalSorter

"""
    THIS IS THE MOST IMPORTANT CLASS!!! Takes your listening history 
    and outputs metrics based on it 

"""

@dataclass
class Artist_Metrics:
    favorites: List[md.Artist_Stat]
    most_popular: List[md.Artist_Stat]
    num_listened: int # number of artists listened to 

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

    def __init__(self, history: List[md.Song], database: Dict[str, md.Artist_Stat], sorting="q") -> None:
        # sorting is q for quick, m for merge
        if sorting not in ["m", "q"]:
            return None
        
        self.sorting = sorting
        self.song_history = history

        self.user_artist_stats: List[md.Artist_Stat] = md.Stats_Extractor.extract_artist_stats_from_songs(history)
        self.user_song_stats: List[md.Song_Stat] = md.Stats_Extractor.extract_song_stats_from_songs(history)

        self.g_artists_map: Dict[str, md.Artist_Stat] = database["artist_stats"]
        self.g_songs_map: Dict[str, md.Song_Stat] = database["song_stats"]

    def analyze_history(self) -> User_Metrics:

        artist_metrics = self.calculate_artist_metrics()
        song_metrics = self.calculate_song_metrics()
        time_listened_s = sum(artist_stat.total_s for artist_stat in self.user_artist_stats)
        pop_score = self.calculate_mainstream_score()        
        cur_metric = User_Metrics(artist_metrics=artist_metrics, song_metrics=song_metrics, time_listened_s=time_listened_s, pop_score=pop_score)

        return cur_metric
    
    def calculate_artist_metrics(self) -> Artist_Metrics:
        # Artist Metrics
        if self.sorting == "q":
            favorite_artists: List[md.Artist_Stat] = StatSorter.quicksort_stats(self.user_artist_stats)
            popular_artists: List[md.Artist_Stat] = GlobalSorter.quicksort_stats(self.user_artist_stats, self.g_artists_map)
        elif self.sorting == "m":
            favorite_artists: List[md.Artist_Stat] = StatSorter.merge_sort_stats(self.user_artist_stats)
            popular_artists: List[md.Artist_Stat] = GlobalSorter.merge_sort_stats(self.user_artist_stats, self.g_artists_map)  
        artist_metrics = Artist_Metrics(favorites=favorite_artists,most_popular=popular_artists,num_listened=len(favorite_artists) )
        return artist_metrics
    
    def calculate_song_metrics(self) -> Song_Metrics:

        # get song metrics
        if self.sorting == "q":

            favorite_songs: List[md.Song_Stat] = StatSorter.quicksort_stats(self.user_song_stats)
            popular_songs: List[md.Song_Stat] = GlobalSorter.quicksort_stats(self.user_song_stats, self.g_songs_map)  
        elif self.sorting == "m":
            favorite_songs: List[md.Song_Stat] = StatSorter.merge_sort_stats(self.user_song_stats)
            popular_songs: List[md.Song_Stat] = GlobalSorter.merge_sort_stats(self.user_song_stats, self.g_songs_map)   
        
        song_met = Song_Metrics(favorites=favorite_songs, most_popular=popular_songs, num_listened=len(favorite_songs))
        
        return song_met
 
    def calculate_mainstream_score(self):

        # use calculate_percentile
        return self.calculate_percentile()


    def calculate_percentile(self):

        """
            Calculates what percentile of listening popularity a users artists stats are at.
        
        """

        sum_pop_artists = 0

        for artist in self.user_artist_stats:
            if artist.get_uri() in self.g_artists_map:

                artist_global_weight = self.g_artists_map[artist.get_uri()].popularity
            else:
                artist_global_weight = 0
            

            sum_pop_artists += artist.total_songs * artist_global_weight

        avg_artist_pop = sum_pop_artists/len(self.user_artist_stats)

        # now lets find the percentile of this! 
        global_AS_list = [artist_stat for uri, artist_stat in self.g_artists_map.items()]

        # sorts by most to least popular
        top_artists: List[md.Artist_Stat] = StatSorter.merge_sort_stats(global_AS_list)

        j = 0
        for (artist_stat) in reversed(top_artists):
            j += 1
            if artist_stat.popularity > avg_artist_pop:
                # we found where this artists placement is 
                break

        
        percentile = j/len(top_artists)
        return percentile