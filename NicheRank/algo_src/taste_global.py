from typing import Any
from typing import List

import NicheRank.algo_src.music_dataclass as md 
from NicheRank.algo_src.sorting import Stat_Sorter
"""
    Global Taste takes in the million playlists database and 
    generates a global taste ranking according to a chosen PopularityMetric scoring class.

    This is what we will compare to the individual user to get their nicheness score 

"""

# Behavior and Storage? 
class Global_Taste():

    def __init__(self, song_stats: List[md.Song_Stat], artist_stats: List[md.Artist_Stat]) -> None:
        # sort song_stats and artist stats by popularity
        self.song_stats = Stat_Sorter(song_stats)
        self.artist_stats = Stat_Sorter(artist_stats)


    def __getattribute__(self, name: str) -> Any:
        pass