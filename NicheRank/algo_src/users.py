from typing import Dict, List, Tuple

from file_management import deserialize_database
from sorting import Local_StatSort
import music_dataclass as md

"""
    This class is for creating listening histories to mimic a spotify API pull. 

    Users have 3 taste modes: high, medium, and low
"""

class Generate_History():

    def __init__(self, database_path) -> None:
        # database is what music database we are pulling from
        self.database = deserialize_database(database_path)

        artist_stats = [artist for uid, artist in self.database["artist_stats"]]
        song_stats = [song for uid, song in self.database["song_stats"]]

        self.song_stats_list:List[md.Song_Stat] = Local_StatSort.quick_sort(song_stats)
        self.artist_stats_list:List[md.Artist_Stat] = Local_StatSort.quick_sort(artist_stats) 


    def greedy_generate_history(self, size:int, pop_level="med"):
        """
            This method uses a greedy algorithm for playlist generation
            pop_level: low, med, or high. This reflects the listening habits of the user
            size: number of songs in playlist
        """

        # lets first have a map which maps each URI to a popularity score
        pop_map: Dict[str, float] = {uri: songstat.popularity for uri, songstat in self.database["song_stats"].items()}
        
        # all values are normalized to be between 0 and 100
        pop_map: Dict[str, float] = Generate_History.normalize_popularity(pop_level)
        pop_list: List[Tuple[str, float]] = [(uri, pop) for uri, pop in pop_map.items()]

    def generate_bins(normed_list: List[Tuple[str, float]]):
        # lets generate 3 bins based on the percentiles. first we have to sort stats tho...
        Generate_History.quick_sort(normed_list)

    
    def normalize_popularity(pop_map: Dict[str, float]):
        min = min(pop for _, pop in pop_map)
        max = max(pop for _, pop in pop_map)
        return {uri: (pop - min)*100/(max-min) for uri, pop in pop_map.items()}


    def quick_sort(song_list: List[Tuple[str, float]]):
        """
            Quicksort should be faster then mergesort, as we dont need to keep constructing lists over and 
            over again. However, to avoid deletions and array creation, we will need to fuse all repeats as the
            very last process in O(N) time.
        """
        Generate_History._quicksort_stats(song_list, 0, len(song_list) - 1) #? O(NLog(N))
        # now that we have sorted this list, there may be repeats, so we must merge this in O(N).
        return song_list

    def _quicksort_helper(stats_list: [md.Artist_Stat, md.Song_Stat], l, r, music_map):
        if (l >= r):
            return

        piv = Global_StatSort._pivot(stats_list, l, r, music_map)

        Global_StatSort._quicksort_stats(stats_list, l, piv - 1, music_map)
        Global_StatSort._quicksort_stats(stats_list, piv + 1, r, music_map)
        

    def _pivot(stats_list: List[Union[md.Artist_Stat, md.Song_Stat]], l, r, music_map) -> int:
        piv = r
        
        i = l
        j = r - 1

        while (i < j):

            while ( i < r and Global_StatSort.global_compare(stats_list[i], stats_list[piv], music_map) == -1):
                # keep moving i right while i greater then piv
                i += 1

            while (j >= l and Global_StatSort.global_compare(stats_list[j], stats_list[piv], music_map) == 1):
                # keep going left while j is smaller then piv
                j -= 1
            if (i < j):
                Global_StatSort._swap(stats_list, i, j)

        # swap i and pivot?
        Global_StatSort._swap(stats_list, i, piv)

        return i # i is the new pivot
