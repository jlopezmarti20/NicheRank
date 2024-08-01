from ..file_management import json_to_music_dict
from ..sorting import Local_Sort

"""
    This script generates 3 user example song histories and adds them to their json file

    user 1: Extremely popular playlist, listens to all the music that is big
    user 2: listens to some popular songs, but mainly medium artists
    user 3: most of their songs are unheard of. Either extremely small or has artists that are not on the list.

"""

json_music_file = "/home/mattyb/Desktop/summer_class_2024/DSA/Projects/NicheRank/NicheRank/algo_src/playlist_stats/song_stats_10000.json"

def gen_user1():
    
    songs_dict = json_to_music_dict(json_music_file)
    

    pass

def gen_user2():
    
    pass

def gen_user3():


def generate_histories():

    gen_user1()
    gen_user2()
    gen_user3()

if __name__ == "__main__":

    generate_histories()