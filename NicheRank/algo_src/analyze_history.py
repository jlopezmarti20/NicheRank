from typing import Dict, List
from dataclasses import dataclass

import music_dataclass as md
from sorting import Local_Sort, Global_Sort
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

def print_metric(metric):
    if isinstance(metric, User_Metrics):
        print(f"pop_score: {metric.pop_score}, time_listened: {metric.time_listened_s} seconds")
        print("artist metrics:")
        print_metric(metric.artist_metrics)
        print("song metrics:")
        print_metric(metric.artist_metrics)
            
    elif isinstance(metric, Song_Metrics):
        print(f"    num songs listened: {metric.num_listened}")
        num_songs = len(metric.most_popular)
        print(f"    unique songs listend: {num_songs}")
        print(f"    most popular songs:")
        most_pop_songs = metric.most_popular[:10] if num_songs >= 10 else metric.most_popular[:num_songs]
        print(f"    most favorite songs: ")
        fav_songs = metric.favorites[:10] if num_songs >= 10 else metric.most_popular[:num_songs]

    elif isinstance(metric, Artist_Metrics):
        print(f"    num artists listened: {metric.num_listened}")
        num_artists = len(metric.most_popular)
        print(f"    unique songs listend: {num_artists}")
        print(f"    most popular songs:")
        most_pop_artists = metric.most_popular[:10] if num_artists >= 10 else metric.most_popular[:num_artists]
        print(f"    most favorite songs: ")
        fav_artists = metric.favorites[:10] if num_artists >= 10 else metric.most_popular[:num_artists]

def calculate_percentile(user_AS:List[md.Artist_Stat], global_AS_map: Dict[str: md.Artist_Stat]):

        sum_pop_artists = 0

        for artist in user_AS:
            artist_global_weight = global_AS_map[artist.get_uri()]
            
            if artist_global_weight == None:
                # if the artists isnt on the list, they must not be popular
                artist_global_weight = 0

            sum_pop_artists += artist.total_songs * artist_global_weight

        avg_artist_pop = sum_pop_artists/len(user_AS)

        # now lets find the percentile of this! 
        global_AS_list = [artist_stat for uri, artist in global_AS_map.items()]
        top_artists: List[md.Artist_Stat] = Local_Sort.merge_sort(global_AS_list)

        j = 0
        for (artist_stat) in top_artists:
            j += 1
            if artist_stat.popularity > avg_artist_pop:
                # we found where this artists placement is 
                break

        percentile = j/len(top_artists)
        return percentile

# Behavior Class
class Mainstream_Engine():

    def __init__(self, history: List[md.Song], global_artists_stat_map: Dict[str, md.Artist_Stat], global_song_stat_map: Dict[str, md.Song_Stat]) -> None:
        self.song_history = history
        self.history_artist_stats: List[md.Artist_Stat] = Stats_Extractor.extract_artist_stats_from_songs(history)
        self.history_song_stats: List[md.Song_Stat] = Stats_Extractor.extract_song_stats_from_songs(history)

        self.g_artists_map = global_artists_stat_map
        self.g_song_map = global_song_stat_map
        

    def analyze_history(self) -> User_Metrics:

        artist_metrics = self.calculate_artist_metrics()
        song_metrics = self.calculate_song_metrics()
        time_listened_s = sum(artist_stat.total_s for artist_stat in self.history_artist_stats)
        pop_score = self.calculate_mainstream_score()        
        cur_metric = User_Metrics(artist_metrics=artist_metrics, song_metrics=song_metrics, time_listened_s=time_listened_s, pop_score=pop_score)

        return cur_metric
    
    def calculate_artist_metrics(self) -> Artist_Metrics:
        # Artist Metrics
        favorite_artists: List[md.Artist_Stat] = Local_Sort.merge_sort(self.history_artist_stats)
        popular_artists: List[md.Artist_Stat] = Global_Sort.merge_sort(self.history_artist_stats, self.g_artists_map)
        artist_metrics = Artist_Metrics(favorites=favorite_artists,most_popular=popular_artists,num_listened=len(favorite_artists) )
        return artist_metrics
    
    def calculate_song_metrics(self) -> Song_Metrics:

        # get song metrics
        favorite_songs: List[md.Song_Stat] = Local_Sort.merge_sort(self.history_song_stats)
        popular_songs: List[md.Song_Stat] = Global_Sort.merge_sort(self.history_song_stats, self.g_song_map)  
        song_met = Song_Metrics(favorites=favorite_songs, most_popular=popular_songs, num_listened=len(favorite_songs))
        
        return song_met
 
    def calculate_mainstream_score(self):

        # use calculate_percentile
        return

    def grouping_based_allignment():

        """
            Sections into n groups that represent "popularity tiers" and then
            gives popularity score based off that tier
        """

        pass
