from typing import List, Tuple, Dict, Union, Any

import music_dataclass as md

"""
    Sorting Class for taking either Songs or Song Stats and sorting them by a given metric

"""

class Sorter():

    def merge_sort(list: List[Tuple[str, float]]):
        if len(list) == 1:
            return list
        mid = len(list) // 2 
        left = list[:mid]
        right = list[mid:]
        sorted_left = Sorter.merge_sort(left)
        sorted_right = Sorter.merge_sort(right)

        return Sorter.merge_fast(sorted_left, sorted_right) 

    def quicksort(list: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        return Sorter._quicksort(list, 0, len(list) - 1)

    def _quicksort(list: List[Tuple[str, float]], l, r)-> None:
        if (l >= r):
            return

        piv = Sorter._pivot(list, l, r)

        Sorter._quicksort(list, l, piv - 1)
        Sorter._quicksort(list, piv + 1, r)

    def _pivot(stats_list: List[Tuple[str, float]], l, r) -> int:
        piv = r
        
        i = l
        j = r - 1

        while (i < j):

            while ( i < r and Sorter.compare(stats_list[i], stats_list[piv]) == -1):
                # keep moving i right while i greater then piv
                i += 1

            while (j >= l and Sorter.compare(stats_list[j], stats_list[piv]) == 1):
                # keep going left while j is smaller then piv
                j -= 1
            if (i < j):
                Sorter._swap(stats_list, i, j)

        # swap i and pivot?
        Sorter._swap(stats_list, i, piv)

        return i # i is the new pivot

    def _swap(list, i, j):
        a = list[i]
        list[i] = list[j]
        list[j] = a     
    
    def merge_fast(left: List[Tuple[str, float]], right: List[Tuple[str, float]]):

        """
            This merge method is faster as it uses a preallocated list that never needs to be expanded.
        """

        l = 0
        r = 0
        i = 0

        size = len(left) + len(right)
        sorted = [None] * size

        while(l < len(left)) and (r < len(right)):
            comparison = Sorter.compare(left[l], right[r])
            if comparison == 0:
                # combine 2 and add to both 
                # THESE SHOULD REALLY BE CLASSES not dataclasses lololol FUCKKK
                sorted[i] = left[l] + right[r]
                del sorted[-1]
                r += 1
                l += 1
                i += 1

            elif comparison == -1 :
                # left is larger, so add left
                sorted[i] = left[l]
                i += 1
                l += 1

            elif comparison == 1:
                # right is larger, so add right 
                sorted[i] = right[r]
                i += 1
                r += 1
        
        while(l < len(left)):
            sorted[i] = left[l]
            i += 1       
            l += 1

        while(r < len(right)):
            sorted[i] = right[r]
            i += 1
            r += 1

        return sorted        

    # behavior
    def merge_slow(left: List, right: List) -> List[Union[md.Song_Stat, md.Artist_Stat]]:
            
            """
                This merge method is slow as it appends to the list continuously, possibly resizing it in O(N) time.
            """

            l = 0
            r = 0
            sorted = []

            while(l < len(left)) and (r < len(right)):
                comparison = Sorter.compare(left[l], right[r])
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
    

    def compare(l: Tuple[str, float], r: Tuple[str, float]):
        """
            l and r are (uri, pop_float)
            returns -1 if l is larger score, 1 if r is larger score, and 0 if they have the same uri
        """

        if l[0] == r[0]:
            # they have equal IDs!
            return 0
        
        l_score = l[1]
        r_score = r[1]

        if (l_score < r_score):
            return 1
        elif (l_score > r_score):
            return -1
        
        elif (l_score == r_score):
            # use alphabetical order?
            if (l[0] > r[0]):
                return -1
            else:
                return 1
    
class StatSorter(Sorter):
    
    @staticmethod
    def merge_sort_stats(stats_list: List[Union[md.Song_Stat, md.Artist_Stat]]) -> List[Union[md.Song_Stat, md.Artist_Stat]]:
        stats_as_tuple = [(stat.get_uri(), stat.popularity) for stat in stats_list]
        sorted_tuple = Sorter.merge_sort(stats_as_tuple)
        music_list = StatSorter.recreate_music_list(sorted_tuple, stats_list)
        return music_list
    @staticmethod
    def quicksort_stats(stats_list:List[Union[md.Song_Stat, md.Artist_Stat]]):
        """
            Quicksort should be faster then mergesort, as we dont need to keep constructing lists over and 
            over again. However, to avoid deletions and array creation, we will need to fuse all repeats as the
            very last process in O(N) time.
        """
        stats_as_tuple = [(stat.get_uri(), stat.popularity) for stat in stats_list]
        
        Sorter.quicksort(stats_as_tuple) #? O(NLog(N))
        music_list = StatSorter.recreate_music_list(stats_as_tuple, stats_list)
        return music_list

    @staticmethod    
    def recreate_music_list(sorted_list, stats_list: List[Union[md.Song_Stat, md.Artist_Stat]])-> List[Union[md.Song_Stat, md.Artist_Stat]]:
        uri_map = {stat.get_uri(): stat for stat in stats_list}
        new_list = [(None, None)] * len(sorted_list)
        for i in range(len(sorted_list)):
            cur_uri = sorted_list[i][0]
            new_list[i] = uri_map[cur_uri]

        return new_list

class GlobalSorter(Sorter):

    @staticmethod
    def merge_sort_stats(stats_list: List[Union[md.Song_Stat, md.Artist_Stat]], global_music_dict) -> List[Union[md.Song_Stat, md.Artist_Stat]]:

        stats_as_tuple = []
        for stat in stats_list:
            uri = stat.get_uri()
            if uri in global_music_dict:
                popularity = global_music_dict[uri].popularity
            else:
                popularity = 0
            stats_as_tuple.append((uri, popularity))

        sorted_tuple = Sorter.merge_sort(stats_as_tuple)
        music_list = GlobalSorter.recreate_music_list(sorted_tuple, stats_list)
        return music_list
    
    @staticmethod
    def quicksort_stats(stats_list:List[Union[md.Song_Stat, md.Artist_Stat]], global_music_dict):
        """
            Quicksort should be faster then mergesort, as we dont need to keep constructing lists over and 
            over again. However, to avoid deletions and array creation, we will need to fuse all repeats as the
            very last process in O(N) time.
        """
        stats_as_tuple = []
        for stat in stats_list:
            uri = stat.get_uri()
            if uri in global_music_dict:
                popularity = global_music_dict[uri].popularity
            else:
                popularity = 0
            stats_as_tuple.append((uri, popularity))
        
        Sorter.quicksort(stats_as_tuple) #? O(NLog(N))
        music_list = GlobalSorter.recreate_music_list(stats_as_tuple, stats_list)
        return music_list

    @staticmethod    
    def recreate_music_list(sorted_list, stats_list)-> List[Union[md.Song_Stat, md.Artist_Stat]]:
        stats_map = {stat.get_uri(): stat for stat in stats_list}

        new_list = [None] * len(sorted_list)
        for i in range(len(sorted_list)):
            cur_uri = sorted_list[i][0]
            new_list[i] = stats_map[cur_uri]
        
        return new_list


""" BADDD lets delete this pleaseee"""

class Local_StatSort():
    
    """
        Stat sort sorts descending by which Stats most listened to   
    """


    def merge_sort(stats_list:List[Union[md.Song_Stat, md.Artist_Stat]]):
        # remember must be stats!!
        # convert to tuples
        return Local_StatSort._merge_sort_stats(stats_list)
    
    def quick_sort(stats_list:List[Union[md.Song_Stat, md.Artist_Stat]]):
        """
            Quicksort should be faster then mergesort, as we dont need to keep constructing lists over and 
            over again. However, to avoid deletions and array creation, we will need to fuse all repeats as the
            very last process in O(N) time.
        """
        Local_StatSort._quicksort_stats(stats_list, 0, len(stats_list) - 1) #? O(NLog(N))
        # now that we have sorted this list, there may be repeats, so we must merge this in O(N).
        # TODO fuse together repeats in list. The list should be sorted, so this step should be simple.
        new_list = Local_StatSort._fuse(stats_list)
        return new_list

    def _quicksort_stats(stats_list: List[Union[md.Artist_Stat, md.Song_Stat]], l, r)-> None:
        if (l >= r):
            return

        piv = Local_StatSort._pivot(stats_list, l, r)

        Local_StatSort._quicksort_stats(stats_list, l, piv - 1)
        Local_StatSort._quicksort_stats(stats_list, piv + 1, r)

    def _pivot(stats_list: List[Union[md.Artist_Stat, md.Song_Stat]], l, r) -> int:
        piv = r
        
        i = l
        j = r - 1

        while (i < j):

            while ( i < r and Local_StatSort._compare_obj(stats_list[i], stats_list[piv]) == -1):
                # keep moving i right while i greater then piv
                i += 1

            while (j >= l and Local_StatSort._compare_obj(stats_list[j], stats_list[piv]) == 1):
                # keep going left while j is smaller then piv
                j -= 1
            if (i < j):
                Local_StatSort._swap(stats_list, i, j)

        # swap i and pivot?
        Local_StatSort._swap(stats_list, i, piv)

        return i # i is the new pivot

    def _fuse(list):
        # fusing takes an already sorted list and merges into a new on. 
        new_list = [None] * len(list)
        # TODO make this
        return list

    def _swap(list, i, j):
        a = list[i]
        list[i] = list[j]
        list[j] = a     

    # behavior
    def _slow_merge_stats(left: List, right: List) -> List[Union[md.Song_Stat, md.Artist_Stat]]:
            
            """
                This merge method is slow as it appends to the list continuously, possibly resizing it in O(N) time.
            """

            l = 0
            r = 0
            sorted = []

            while(l < len(left)) and (r < len(right)):
                comparison = Local_StatSort._compare_obj(left[l], right[r])
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
    
    def _fast_merge_stats(left: List, right: List) -> List[Union[md.Song_Stat, md.Artist_Stat]]:

        """
            This merge method is faster as it uses a preallocated list that never needs to be expanded.
        """

        l = 0
        r = 0
        i = 0

        size = len(left) + len(right)
        sorted = [None] * size

        while(l < len(left)) and (r < len(right)):
            comparison = Local_StatSort._compare_obj(left[l], right[r])
            if comparison == 0:
                # combine 2 and add to both 
                # THESE SHOULD REALLY BE CLASSES not dataclasses lololol FUCKKK
                sorted[i] = left[l] + right[r]
                del sorted[-1]
                r += 1
                l += 1
                i += 1

            elif comparison == -1 :
                # left is larger, so add left
                sorted[i] = left[l]
                i += 1
                l += 1

            elif comparison == 1:
                # right is larger, so add right 
                sorted[i] = right[r]
                i += 1
                r += 1
        
        while(l < len(left)):
            sorted[i] = left[l]
            i += 1       
            l += 1

        while(r < len(right)):
            sorted[i] = right[r]
            i += 1
            r += 1

        return sorted

    def _merge_sort_stats(stats_list:List[Union[md.Artist_Stat, md.Song_Stat]]):
        if len(stats_list) == 1:
            return stats_list
        
        mid = len(stats_list) // 2
        left_songs = stats_list[:mid]
        right_songs = stats_list[mid:]
        sorted_left = Local_StatSort._merge_sort_stats(left_songs)
        sorted_right = Local_StatSort._merge_sort_stats(right_songs)

        return Local_StatSort._fast_merge_stats(sorted_left, sorted_right) 

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


class Global_StatSort():

    """
        Popularity sort sorts decending by seeing which Stats more popular in Global Taste
    """

    def merge_sort(stats_list:List[Union[md.Artist_Stat, md.Song_Stat]], music_map) -> List[Union[md.Artist_Stat, md.Song_Stat]]:
        return Global_StatSort._merge_sort_stats(stats_list, music_map)

    def quick_sort(stats_list:List[Union[md.Song_Stat, md.Artist_Stat]], music_map):
        """
            Quicksort should be faster then mergesort, as we dont need to keep constructing lists over and 
            over again. However, to avoid deletions and array creation, we will need to fuse all repeats as the
            very last process in O(N) time.
        """
        Global_StatSort._quicksort_stats(stats_list, 0, len(stats_list) - 1, music_map) #? O(NLog(N))
        # now that we have sorted this list, there may be repeats, so we must merge this in O(N).
        # TODO fuse together repeats in list. The list should be sorted, so this step should be simple.
        new_list = Local_StatSort._fuse(stats_list)
        return new_list

    def _quicksort_stats(stats_list: List[Union[md.Artist_Stat, md.Song_Stat]], l, r, music_map):
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

    def _fuse(list):
        # fusing takes an already sorted list and merges into a new on. 
        new_list = [None] * len(list)
        # TODO make this
        return list

    def _swap(list, i, j):
        a = list[i]
        list[i] = list[j]
        list[j] = a     


    def _merge_sort_stats(stats_list:List[Union[md.Artist_Stat, md.Song_Stat]], music_map):
        
        if len(stats_list) == 1:
            return stats_list
        
        mid = len(stats_list) // 2
        left_songs = stats_list[:mid]
        right_songs = stats_list[mid:]
        sorted_left = Global_StatSort._merge_sort_stats(left_songs, music_map)
        sorted_right = Global_StatSort._merge_sort_stats(right_songs, music_map)

        return Global_StatSort._merge_stats(sorted_left, sorted_right, music_map) 
        
    def _merge_stats(left: List, right: List, music_map) -> List[Union[md.Song_Stat, md.Artist_Stat]]:
            
            l = 0
            r = 0
            sorted = []

            while(l < len(left)) and (r < len(right)):
                
                comparison = Global_StatSort.global_compare(l, r, music_map)
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
    
    def _fast_merge_stats(left: List, right: List, music_map) -> List[Union[md.Song_Stat, md.Artist_Stat]]:

        """
            This merge method is faster as it uses a preallocated list that never needs to be expanded.
        """

        l = 0
        r = 0
        i = 0

        size = len(left) + len(right)
        sorted = [None] * size

        while(l < len(left)) and (r < len(right)):
            comparison = Global_StatSort.global_compare(left[l], right[r], music_map)
            if comparison == 0:
                # combine 2 and add to both 
                # THESE SHOULD REALLY BE CLASSES not dataclasses lololol FUCKKK
                sorted[i] = left[l] + right[r]
                del sorted[-1]
                r += 1
                l += 1
                i += 1

            elif comparison == -1 :
                # left is larger, so add left
                sorted[i] = left[l]
                i += 1
                l += 1

            elif comparison == 1:
                # right is larger, so add right 
                sorted[i] = right[r]
                i += 1
                r += 1
        
        while(l < len(left)):
            sorted[i] = left[l]
            i += 1
            l += 1

        while(r < len(right)):
            sorted[i] = right[r]
            i += 1
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

