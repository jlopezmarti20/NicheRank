from typing import List, Tuple, Dict, Union
from typing import Any

import music_dataclass as md
import NicheRank.algo_src.popularity as pop_rank

"""
    Sorting Class for taking either Songs or Song Stats and sorting them by a given metric

"""


def merge_stats(left: List, right: List):
        
        l = 0
        r = 0
        sorted = []

        while(l < len(left)) and (r < len(right)):
            comparison = compare_obj(left[l], right[r])
            if comparison == 0:
                # combine 2 and add to both 
                # THESE SHOULD REALLY BE CLASSES not dataclasses lololol FUCKKK
                sorted.append((left[l] + right[r]))
                r += 1
                l += 1
            elif comparison == -1 :
                # left is larger, so add right
                sorted.append(right[r])
                r += 1

            elif comparison == 1:
                # right is larger, so add left 
                sorted.append(left[l])
        return sorted

def merge_sort_stats(stats_list:List[Union[md.Artist_Stat, md.Song_Stat]], scoring_method):
    if len(stats_list) == 1:
        return stats_list
    
    mid = len(stats_list) // 2
    left_songs = stats_list[:mid]
    right_songs = stats_list[mid:]
    sorted_left = merge_sort_stats(left_songs)
    sorted_right = merge_sort_stats(right_songs)

    return merge_stats(sorted_left, sorted_right, scoring_method) 

def compare_obj(l, r):
    # compares 2 artist_stats or song_stats

    # -1 if left is larger, 1 if right is larger, 0 if they are the same artist

    if isinstance(l, md.Artist_Stat):
        # both are artist stats
        if l.artist.uri == r.artist.uri:
            return 0

    elif isinstance(l, md.Song_Stat):
        # is both are same song stats
        if l.song.uri == r.song.uri:
            return 0

    if l.artist.uri == r.artist.uri:
        # these are the same artist stats
        return 0
    
    left_pop = l.popularity()
    right_pop = r.popularity()

    if (left_pop < right_pop):
        return 1
    else:
        return -1
