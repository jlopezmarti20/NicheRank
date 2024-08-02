from typing import Dict, List, Tuple
import random

from file_management import deserialize_database
from sorting import Sorter
import music_dataclass as md

"""
    This class is for creating listening histories to mimic a spotify API pull. 

    Users have 3 taste modes: high, medium, and low
"""

class Generate_History():

    def __init__(self, database_path) -> None:
        # database is what music database we are pulling from
        database = deserialize_database(database_path)
        self.database_artist_stats = database["artist_stats"]
        self.database_song_stats = database["song_stats"]

    def graph_generate_history(self, size:int, pop_level="med"):
        """
            Generate a user play history based off a graph method
        """
        
        pass

    def greedy_generate_history(self, size:int, pop_level="med"):
        """
            This method uses a greedy algorithm for playlist generation
            pop_level: low, med, or high. This reflects the listening habits of the user
            size: number of songs in playlist
        """

        # grap a bunch of songs, and then choose the one of nth popularity 

        i = 0
        num_choices = 5
        while (i < size):
            choices = [None] * num_choices
            for j in range(num_choices):
                choices[j] = random.randint(0, len(self.database_song_stats))
            
            # we now want the small, medium, or large 
                
            # choose the smallest, medium or large value by using a heap 

    def generate_bins(normed_list: List[Tuple[str, float]]):
        # todo: maybe make however many bins we want?
        # lets generate 3 bins based on the percentiles. first we have to sort stats tho...
        sorted_list: List[Tuple[str, int]] = Sorter.quicksort(normed_list)
        n = len(sorted_list)
        low_bin = sorted_list[2*n//3:]
        med_bin = sorted_list[n//3:2*n//3]
        high_bin = sorted_list[0:n//3]

        return low_bin, med_bin, high_bin

    
    def normalize_popularity(pop_map: Dict[str, float]):
        min = min(pop for _, pop in pop_map)
        max = max(pop for _, pop in pop_map)
        return {uri: (pop - min)*100/(max-min) for uri, pop in pop_map.items()}
