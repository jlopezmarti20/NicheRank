
import os
from typing import List, Tuple, Dict

import json_parsing
import music_dataclass as md

"""
    insert a spotify listening history json file and store, then output top songs, top artists etc

"""

default_recently_played = "idk" #! change this to config data!

class User_Taste():


    """
        Loads and handles an individuals spotify taste
    
    """

    def __init__(self, spotify_history_file:str) -> None:
        # history_location: string of where spotify json file is
        self.spotify_history_file = spotify_history_file 
        self.artist = []
        self.songs_metrics = None

        pass

    def process_user_history(self, song_history: List[md.Song])->None:
        # TODO process and store a users favorite artists based on time listened  
        pass        
        # sort this list with merge sort?
        # put this list into a heap?

    def get_favorite_artists(self, n=None):
        # Return n favorite artists
        if (self.artists_metrics is None):
            return None
        
        # get all
        n = self.unique_artists_listened() if n is None else n
        
        pass

    def get_favorite_songs(self, n=None):
        # Return n Favorite songs
        if (self.songs_metrics is None):
            return None

        n = self.unique_songs_listened() if n is None else n


        pass 

    def unique_artists_listened(self)->int:
        # total artists youve listened to 
        pass

    def unique_songs_listened(self)->int:
        # total unique songs youve listened to
        pass

class SongSorter():

    """
        Input list of md.Songs, output tuple of (md.Song, freq) of of that song

        #TODO add different comparison methods to use!
    """


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
        sorted_list:List[Tuple[int, str]] = SongSorter._merge_sort(tuple_songs)

        return [(uri_song_map[uri], freq) for (freq, uri) in sorted_list]

    def basic_merge_sort(songs: List[md.Song]) -> List[Tuple[md.Song, int]]:
        # uri: song mapping
        uri_song_map = {song.uri: song for song in songs}

        tuple_list = [(1, song.uri) for song in songs] # tuples of uri to song

        sorted_list: List[Tuple[int, str]] = SongSorter._merge_sort(tuple_list)
        
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
            comparison = SongSorter._tuple_song_compare(left[l], right[r])
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
        sorted_left = SongSorter._merge_sort(left_songs)
        sorted_right = SongSorter._merge_sort(right_songs)

        return SongSorter._merge(sorted_left, sorted_right) 


def create_songs_from_uris(uris):
    return [md.Song(name="", uri=uri) for uri in uris]

def basic_merge_test(given_uris, target_uris):
    songs = create_songs_from_uris(given_uris)
    merged_songs = SongSorter.basic_merge_sort(songs)

    for song, freq in merged_songs:
        print(f"{song.uri}: freq {freq}")
    
    assert(len(merged_songs) == len(target_uris))
    
def hash_merge_test(given_uris, target_uris):
    songs = create_songs_from_uris(given_uris)
    merged_songs = SongSorter.hash_merge_sort(songs)

    for song, freq in merged_songs:
        print(f"{song.uri}: freq {freq}")
    
    assert(len(merged_songs) == len(target_uris))

def basic_merge_sort_testing():
    # test song sorting
    input_1 = ["323232", "454", "65", "10", "4"]
    expected_1 = ["4", "10", "65", "454", "323232"]
    basic_merge_test(input_1, expected_1)
    hash_merge_test(input_1, expected_1)

    # now test if they properly merge when sorting
    input_2 = ["50", "4", "5", "4", "6", "56", "1", "50"]
    expected_2 = ["1", "56", "4", "5", "6", "50"]

    basic_merge_test(input_2, expected_2)
    hash_merge_test(input_2, expected_2)



if __name__ == "__main__":
    basic_merge_sort_testing()