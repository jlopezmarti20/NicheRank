import os 
import sys
import json
from typing import List, Tuple, Dict, Union

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../NicheRank/algo_src')))

import music_dataclass as md
from sorting import Local_StatSort
from file_management import parse_spotify_history_json


def create_dummy_artiststats(listens) -> List[md.Artist_Stat]:
    return [md.Artist_Stat(artist=md.Artist(name=str(i), uri=str(i)),
                           total_s=listen, 
                           total_songs=listen, 
                           weighted_listens=listen) 
            for i,(listen) in enumerate(listens)]

def create_dummy_songstats(listens):
    return [md.Song_Stat(song=md.Song(name=str(i),uri=str(i)), 
                         total_listens=listen, weighted_listens=listen) 
            for i, (listen) in enumerate(listens)]

def basic_songstat_merge_test(listen_times, target_times):
    print("Songstat merge testing")
    song_stats = create_dummy_songstats(listen_times)
    merged_songstats = Local_StatSort.merge_sort(song_stats)

    for song_stat in merged_songstats:
        print(f"{song_stat.song.uri} pop: {song_stat.popularity}")
    
def basic_artiststat_merge_test(listen_times, target_times):
    print("Artiststat testing")
    artist_Stats = create_dummy_artiststats(listen_times)
    merged_artiststats = Local_StatSort.merge_sort(artist_Stats)

    for artist_stat in merged_artiststats:
        print(f"{artist_stat.artist.uri} pop: {artist_stat.popularity}")
    
        

def TEST_1_STATSORT():
    # test basics of sorting
    listens_1 = [323232, 454, 65, 10, 4]
    expected_1 = [4, 10, 65, 454, 323232]
    basic_artiststat_merge_test(listens_1, expected_1)
    basic_songstat_merge_test(listens_1, expected_1)
    # hash_merge_test(input_1, expected_1)

    # now test if they properly merge when sorting
    input_2 = [50, 4, 5, 6, 56, 1]
    expected_2 = [1, 4, 5, 6, 50, 56]

    basic_artiststat_merge_test(input_2, expected_2)
    basic_songstat_merge_test(input_2, expected_2)
    # hash_merge_test(input_2, expected_2)


def TEST_2_QUICKSORT(): 
    # test edge cases (empty uri)
    history = "/home/mattyb/Desktop/summer_class_2024/DSA/Projects/NicheRank/NicheRank/algo_src/example_user_history/user_rand_173217_50.json"
    songs = parse_spotify_history_json(history)
    sorted = Local_StatSort.quick_sort(songs)


def all_tests():

    pass


if __name__ == "__main__":

    TEST_2_QUICKSORT()