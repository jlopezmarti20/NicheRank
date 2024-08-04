from typing import Dict, List
from dataclasses import dataclass

import music as md
from sorting import StatSorter, GlobalSorter

"""
    Metrics store information about a users listening history, 
    retrieved from the HistoryAnalyzer class.

"""

@dataclass
class Artist_Metrics:
    favorites: List[str]
    most_popular: List[str]
    num_listened: int # number of artists listened to 

@dataclass
class Song_Metrics:
    favorites: List[str]
    most_popular: List[str]
    num_listened: int

@dataclass
class User_Metrics:
    # data to be returned after analyzing
    artist_metrics: Artist_Metrics
    song_metrics: Song_Metrics
    pop_score: float # val from 0 to 100 of how popular this persons taste is+


"""
    The HistoryAnalyzer class analyzes the history of the 
    a history list of songs. It outputs a User Metric when
    analyze history is called.
"""

class HistoryAnalyzer():

    def __init__(self, history: List[md.Song], database: Dict[str, md.Artist_Stat]) -> None:
        # sorting is q for quick, m for merge
        self.song_history = history

        self.user_artist_stats: List[md.Artist_Stat] = md.Stats_Extractor.extract_artist_stats_from_songs(history)
        self.user_song_stats: List[md.Song_Stat] = md.Stats_Extractor.extract_song_stats_from_songs(history)

        self.g_artists_map: Dict[str, md.Artist_Stat] = database["artist_stats"]
        self.g_songs_map: Dict[str, md.Song_Stat] = database["song_stats"]

    def analyze_history(self, sorting="q") -> User_Metrics:

        """
            Returns user metrics from the given history of that user.
        """

        artist_metrics = self.calculate_artist_metrics(sorting)
        song_metrics = self.calculate_song_metrics(sorting)
        pop_score = self.calculate_mainstream_score()        
        cur_metric = User_Metrics(artist_metrics=artist_metrics, song_metrics=song_metrics, pop_score=pop_score)

        return cur_metric
    
    def calculate_artist_metrics(self, sorting) -> Artist_Metrics:
        # Artist Metrics
        num_shown = 10 if 10 > len(self.user_artist_stats) else len(self.user_artist_stats)
        
        if sorting == "q":
            favorite_artists: List[md.Artist_Stat] = StatSorter.quicksort_stats(self.user_artist_stats)
            popular_artists: List[md.Artist_Stat] = GlobalSorter.quicksort_stats(self.user_artist_stats, self.g_artists_map)
        elif sorting == "m":
            favorite_artists: List[md.Artist_Stat] = StatSorter.merge_sort_stats(self.user_artist_stats)
            popular_artists: List[md.Artist_Stat] = GlobalSorter.merge_sort_stats(self.user_artist_stats, self.g_artists_map)  
        
        fav_10 = favorite_artists[:num_shown]
        pop_10 = popular_artists[:num_shown]
        fav_10 = [stat.artist.name for stat in fav_10]
        pop_10 = [stat.artist.name for stat in pop_10]
        artist_metrics = Artist_Metrics(favorites=fav_10,most_popular=pop_10,num_listened=len(favorite_artists) )
        return artist_metrics
    
    def calculate_song_metrics(self, sorting) -> Song_Metrics:

        # get song metrics
        if sorting == "q":

            favorite_songs: List[md.Song_Stat] = StatSorter.quicksort_stats(self.user_song_stats)
            popular_songs: List[md.Song_Stat] = GlobalSorter.quicksort_stats(self.user_song_stats, self.g_songs_map)  
        elif sorting == "m":
            favorite_songs: List[md.Song_Stat] = StatSorter.merge_sort_stats(self.user_song_stats)
            popular_songs: List[md.Song_Stat] = GlobalSorter.merge_sort_stats(self.user_song_stats, self.g_songs_map)   
        num_shown = 10 if 10 > len(self.user_song_stats) else len(self.user_song_stats)
        pop_10 = popular_songs[:num_shown]
        fav_10 = favorite_songs[:num_shown]
        pop_10 = [stat.song.name for stat in pop_10]
        fav_10 = [stat.song.name for stat in fav_10]
        song_met = Song_Metrics(favorites=fav_10, most_popular=pop_10, num_listened=len(favorite_songs))
        
        return song_met
 
    def calculate_mainstream_score(self) -> float:

        # use calculate_percentile
        return self.calculate_percentile()


    def calculate_percentile(self) -> float:

        """
            Calculates what percentile of listening popularity a users artists stats are at.
        
        """
        # first, lets normalize all the artists
        min_global = min(artist.popularity for uri, artist in self.g_artists_map.items())
        max_global = max(artist.popularity for uri, artist in self.g_artists_map.items()) 
        
        normalized_artist_stats = {uri: (artist_stat.popularity - min_global)*100/(max_global - min_global) for uri, artist_stat in self.g_artists_map.items()}
        sum_pop_artists = 0
        total_songs_listened = 0

        for artist_stat in self.user_artist_stats:
            if artist_stat.get_uri() in normalized_artist_stats:
                artist_global_weight = normalized_artist_stats[artist_stat.get_uri()]
            else:
                artist_global_weight = 1
            
            total_songs_listened += artist_stat.total_listens
            sum_pop_artists += artist_stat.total_listens * artist_global_weight

        avg_artist_pop = sum_pop_artists/total_songs_listened

        # now lets find the percentile of this! 
        global_AS_list = [artist_stat for uri, artist_stat in self.g_artists_map.items()]

        # sorts by most to least popular
        top_artists: List[md.Artist_Stat] = StatSorter.merge_sort_stats(global_AS_list)

        j = 1
        for (artist_stat) in reversed(top_artists):
            # 0 is least popular artist
            if artist_stat.popularity > avg_artist_pop:
                # we found where this artists placement is 
                break

            j += 1

        
        percentile = j/len(top_artists)
        return percentile
