from typing import List, Tuple, Dict, Union, Any
import music_dataclass as md
"""
    Sorting Class for taking either Songs or Song Stats and sorting them by a given metric

"""

class Local_Sort():
    
    """
        Stat sort sorts descending by which Stats most listened to   
    """

    def merge_sort(stats_list:List[Union[md.Song_Stat, md.Artist_Stat]]):
        return Local_Sort._merge_sort_stats(stats_list)
    
    def heap_sort(stats_list:List[Union[md.Song_Stat, md.Artist_Stat]]):
        # TODO

        pass

    # behavior
    def _merge_stats(left: List, right: List) -> List[Union[md.Song_Stat, md.Artist_Stat]]:
            
            l = 0
            r = 0
            sorted = []

            while(l < len(left)) and (r < len(right)):
                comparison = Local_Sort.compare_obj(left[l], right[r])
                if comparison == 0:
                    # combine 2 and add to both 
                    # THESE SHOULD REALLY BE CLASSES not dataclasses lololol FUCKKK
                    sorted.append((left[l] + right[r]))
                    r += 1
                    l += 1

                elif comparison == -1 :
                    # left is larger, so add left
                    sorted.append(left[l])
                    l += 1

                elif comparison == 1:
                    # right is larger, so add right 
                    sorted.append(right[r])
                    r += 1
            
            while(l < len(left)):
                sorted.append(left[l])
                l += 1

            while(r < len(right)):
                sorted.append(right[r])
                r += 1

            return sorted

    def _merge_sort_stats(stats_list:List[Union[md.Artist_Stat, md.Song_Stat]]):
        if len(stats_list) == 1:
            return stats_list
        
        mid = len(stats_list) // 2
        left_songs = stats_list[:mid]
        right_songs = stats_list[mid:]
        sorted_left = Local_Sort._merge_sort_stats(left_songs)
        sorted_right = Local_Sort._merge_sort_stats(right_songs)

        return Local_Sort._merge_stats(sorted_left, sorted_right) 

    def _compare_obj(l, r):
        # compares 2 artist_stats or song_stats

        # -1 if left is larger, 1 if right is larger, 0 if they are the same artist

        if l == r:
            # both are equal to each other!
            return 0
        
        left_pop = l.popularity
        right_pop = r.popularity

        if (left_pop < right_pop):
            return 1
        elif (left_pop > right_pop):
            return -1
        
        elif (left_pop == right_pop):
            # use alphabetical order?
            if (l.get_uri() > l.get_uri()):
                return -1
            else:
                return 1


class Popularity_Sort():

    """
        Popularity sort sorts decending by seeing which Stats more popular in Global Taste
    """

    def merge_sort(stats_list:List[Union[md.Artist_Stat, md.Song_Stat]], music_map):
        return Popularity_Sort._merge_sort_stats(stats_list, music_map)

    def _merge_sort_stats(stats_list:List[Union[md.Artist_Stat, md.Song_Stat]], music_map):
        
        if len(stats_list) == 1:
            return stats_list
        
        mid = len(stats_list) // 2
        left_songs = stats_list[:mid]
        right_songs = stats_list[mid:]
        sorted_left = Popularity_Sort._merge_sort_stats(left_songs, music_map)
        sorted_right = Popularity_Sort._merge_sort_stats(right_songs, music_map)

        return Popularity_Sort._merge_stats(sorted_left, sorted_right, music_map) 
        
    def _merge_stats(left: List, right: List, music_map) -> List[Union[md.Song_Stat, md.Artist_Stat]]:
            
            l = 0
            r = 0
            sorted = []

            while(l < len(left)) and (r < len(right)):
                
                comparison = Popularity_Sort.global_compare(l, r, music_map)
                if comparison == 0:
                    # combine 2 and add to both 
                    # THESE SHOULD REALLY BE CLASSES not dataclasses lololol FUCKKK
                    sorted.append((left[l] + right[r]))
                    r += 1
                    l += 1
                elif comparison == -1 :
                    # left is larger, so add left
                    sorted.append(left[l])
                    l += 1

                elif comparison == 1:
                    # right is larger, so add right 
                    sorted.append(right[r])
                    r += 1
            
            while(l < len(left)):
                sorted.append(left[l])
                l += 1

            while(r < len(right)):
                sorted.append(right[r])
                r += 1

            return sorted
    
    def global_compare(l, r, music_map):
        # -1 if left is more popular, 1 if right is more popular, 0 if they are the same artist

        if l == r:
            # both are equal to each other!
            return 0

        global_l = music_map[l.get_uri()]
        global_r = music_map[r.get_uri()]


        if global_l is None or global_r is None:
            # one of the 2 are not on the ranking board, so one on board automatically wins
            if (global_l is None) and (global_r is None):
                if (l.get_uri() > r.get_uri()):
                    return -1
                else:
                    return 1
            elif global_l is None:
                return 1
            elif (global_r is None):
                return -1
  
        l_global_pop = global_l.popularity
        r_global_pop = global_r.popularity
        
        if (l_global_pop < r_global_pop):
            return 1
        elif (l_global_pop > r_global_pop):
            return -1
        
        elif (l_global_pop == r_global_pop):
            # use alphabetical order?
            if (l.get_uri() > l.get_uri()):
                return -1
            else:
                return 1

