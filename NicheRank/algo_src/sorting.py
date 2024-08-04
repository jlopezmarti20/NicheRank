from typing import List, Tuple, Dict, Union, Any

import music as md

"""
    Sorting class takes a list of (str,float) Tuples and sorts them by ascending order
    using either quicksort or mergesort.
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
            This merge method is faster as it uses a preallocated list that never needs to be expanded. O(N)
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
    def merge_slow(left: List, right: List) -> List[md.Stat]:
            
            """
                This merge method is slow as it appends to the list continuously, possibly resizing it in O(N) time.
                HOWEVER, because it uses a append operation which can require resizing, it becomes O(N^2).
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
    
"""
    The StatSorter takes in a list of Artist Stats or Song Stats and sorts them
    by whatever popularity metric they use, with either merge or quicksort.
"""

class StatSorter(Sorter):
    
    @staticmethod
    def merge_sort_stats(stats_list: List[md.Stat]) -> List[md.Stat]:
        """
            Quicksorts a list of either ArtistStats or SongStats
        """
        stats_as_tuple = [(stat.get_uri(), stat.popularity) for stat in stats_list]
        sorted_tuple = Sorter.merge_sort(stats_as_tuple)
        music_list = StatSorter.recreate_music_list(sorted_tuple, stats_list)
        return music_list
    @staticmethod
    def quicksort_stats(stats_list:List[md.Stat]):
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
    def recreate_music_list(sorted_list, stats_list: List[md.Stat])-> List[md.Stat]:
        uri_map = {stat.get_uri(): stat for stat in stats_list}
        new_list = [(None, None)] * len(sorted_list)
        for i in range(len(sorted_list)):
            cur_uri = sorted_list[i][0]
            new_list[i] = uri_map[cur_uri]

        return new_list

"""
    GlobalSorter takes a song_history and a stats database and sorts them based on
    the popularity of the stats database.
"""

class GlobalSorter(Sorter):

    @staticmethod
    def merge_sort_stats(stats_list: List[md.Stat], global_music_dict) -> List[md.Stat]:
        # Merge Sort Stats runs merge sort with the global_music_dict in O(NLogN), HOWEVER
        # its main slowdown occurs when it keeps recreating the list in the merge operation. 
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
    def quicksort_stats(stats_list:List[md.Stat], global_music_dict):
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
    def recreate_music_list(sorted_list, stats_list)-> List[md.Stat]:
        # from the sorted tuple list, recreates the stats list using a hashmap O(LenSortedList)
        stats_map = {stat.get_uri(): stat for stat in stats_list}

        new_list = [None] * len(sorted_list)
        for i in range(len(sorted_list)):
            cur_uri = sorted_list[i][0]
            new_list[i] = stats_map[cur_uri]
        
        return new_list

