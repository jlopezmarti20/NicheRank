from typing import List, Tuple, Dict
from typing import Any

import music_dataclass as md
import NicheRank.algo_src.popularity as pop_rank

"""
    Sorting Class for taking either Songs or Song Stats and sorting them by a given metric

"""



class Sort_Records():

    """

    """

    def __call__(self, records_list) -> Any:
        if isinstance(records_list[0], md.Artist_Stat):
            # perform an artists sort

        elif isinstance(records_list[0], md.Song_Stat):
            # perform a song records sort
    
    def sort_artists_records():

        pass

    def sort_song_records():

        pass


class Sort_Artists_Records():

    """
        Sorts Artist Stats according to some metric!
    
    """

    def __init__(self) -> None:
        pass


    def stats_sort(self, artist_stats_records: List[md.Artist_Stat], 
                   scoring_method:pop_rank.Artist_Scorer,
                   sorting_type = "merge")->List[md.Artist_Stat]:
        
        # sorts artist stats by a given scoring method. Lets do a basic merge sort.
        if sorting_type == "merge":
            return Sort_Artists._merge_sort(artist_stats_records, scoring_method)

        else:
            return None

    def _merge(left: List[md.Artist_Stat], right: List[md.Artist_Stat], scoring_method:pop_rank.Artist_Scorer):
        l = 0
        r = 0
        sorted = []

        while(l < len(left)) and (r < len(right)):
            comparison = Sort_Artists._compare(left[l], right[r], scoring_method)
            if comparison == 0:
                # combine 2 and add to both 
                sorted.append((left[l][0] + right[r][0], left[l][1]))
                r += 1
                l += 1
            elif comparison == -1 :
                # left is larger, so add right
                sorted.append(right[r])
                r += 1

            elif comparison == 1:
                # right is larger, so add left 
                sorted.append(left[l])
                l += 1

        while (l < len(left)):
            sorted.append(left[l])
            l += 1

        while(r < len(right)):
            sorted.append(right[r])
            r += 1 

        return sorted

    def _merge_sort(artist_stats:List[md.Artist_Stat], scoring_method:pop_rank.Artist_Scorer) -> List[Tuple[int, str]]:
        if len(artist_stats) == 1:
            return artist_stats
        
        mid = len(artist_stats) // 2
        left_songs = artist_stats[:mid]
        right_songs = artist_stats[mid:]
        sorted_left = Sort_Artists._merge_sort(left_songs)
        sorted_right = Sort_Artists._merge_sort(right_songs)

        return Sort_Artists._merge(sorted_left, sorted_right, scoring_method) 

    def _compare(l:md.Artist_Stat, r: md.Artist_Stat, scoring_method:pop_rank.Artist_Scorer):
        # compares 2 artist records

        # -1 if left is larger, 1 if right is larger, 0 if they are the same artist

        if l.artist.uri == r.artist.uri:
            # these are the same artist stats
            return 0
        
        left_pop = scoring_method(l)
        right_pop = scoring_method(r)

        if (left_pop < right_pop):
            return 1
        else:
            return -1


        


class Sort_Songs():

    """
        Input list of md.Songs, output tuple of (md.Song, freq) of of that song
    """

    def songs_sort():
        pass


    def frequency_sort(self, songs:List[md.Song]) -> List[md.Song_Stat]:
        # sorts list of songs by frequency, returns List[md.Song_Stat]
        pass

    def hash_merge_sort(songs: List[md.Song]) -> List[Tuple[md.Song, int]]:
        """
            This sorting algorithm generates a hashmap for song_uri to number of repeats, and then 
            does a sort by number of keys  
        """
        uri_song_map = {song.uri: song for song in songs}
        song_freq = {}
        for song in songs:
            if song.uri not in song_freq:
                song_freq[song.uri] = 0
            song_freq[song.uri] += 1

        tuple_songs:List[Tuple[int, str]] = [(freq, uri) for uri, freq in song_freq.items()]
        sorted_list:List[Tuple[int, str]] = Song_Sorter._merge_sort(tuple_songs)

        return [(uri_song_map[uri], freq) for (freq, uri) in sorted_list]

    def basic_merge_sort(songs: List[md.Song]) -> List[Tuple[md.Song, int]]:
        # uri: song mapping
        uri_song_map = {song.uri: song for song in songs}

        tuple_list = [(1, song.uri) for song in songs] # tuples of uri to song

        sorted_list: List[Tuple[int, str]] = Song_Sorter._merge_sort(tuple_list)
        
        # change sorted list back to (md.song, freq) 
        return [(uri_song_map[uri], freq) for (freq, uri) in sorted_list]


    # =================== PRIVATE METHODS ===================

    def _tuple_song_compare(l_tup: Tuple[int, str], r_tup:Tuple[int, str]):
        # -1 if left is larger, 1 if right is larger, 0 if equal

        if l_tup[1] == r_tup[1]:
            return 0

        if l_tup[0] > r_tup[0]:
            return -1
        elif l_tup[0] < r_tup[0]:
            return 1
        else:
            if l_tup[1] > r_tup[1]:
                return -1
            else:
                return 1

    def _merge(left:List[Tuple[int, str]], right: List[Tuple[int, str]]):
        l = 0
        r = 0
        sorted = []

        while(l < len(left)) and (r < len(right)):
            comparison = Song_Sorter._tuple_song_compare(left[l], right[r])
            if comparison == 0:
                # combine 2 and add to both 
                sorted.append((left[l][0] + right[r][0], left[l][1]))
                r += 1
                l += 1
            elif comparison == -1 :
                # left is larger, so add right
                sorted.append(right[r])
                r += 1

            elif comparison == 1:
                # right is larger, so add left 
                sorted.append(left[l])
                l += 1

        while (l < len(left)):
            sorted.append(left[l])
            l += 1

        while(r < len(right)):
            sorted.append(right[r])
            r += 1 

        return sorted

    def _merge_sort(songs: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
        if len(songs) == 1:
            return songs
        
        mid = len(songs) // 2
        left_songs = songs[:mid]
        right_songs = songs[mid:]
        sorted_left = Song_Sorter._merge_sort(left_songs)
        sorted_right = Song_Sorter._merge_sort(right_songs)

        return Song_Sorter._merge(sorted_left, sorted_right) 

