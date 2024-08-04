from NicheRank.algo_src.file_utils import json_to_music_dict
from NicheRank.algo_src.music import * 
import random
import os
import json
from typing import List

"""
    This script generates 3 user example song histories and adds them to their json file

    user 1: Extremely popular playlist, listens to all the music that is big
    user 2: listens to some popular songs, but mainly medium artists
    user 3: most of their songs are unheard of. Either extremely small or has artists that are not on the list.

"""

def convert_to_spotify_response(songs: List[Song]):
    # converts a song into a dictionary that is similar to a spotify song request

    response = {
        "total": len(songs),
        "items": []
    }

    for song in songs:

        artists_list = [{
                "name": artist.name,
                "uri" : artist.uri
            } for artist in song.artists]

        track_dict = {
            "track": {
                "artists": artists_list,
                "duration_ms": song.duration_s*1000,
                "name": song.name,
                "uri": song.uri
            }
        }
        response["items"].append(track_dict)

    return response

def gen_random_user(json_songs_file, save_location, N=100_000):
    # generate N songs
    songs_dict = json_to_music_dict(json_songs_file)
    database_uris:str = [uri for uri, song_stat in songs_dict.items()]
    
    save_name = f"user_rand_{len(database_uris)}_{N}.json"
    songs: List[Song] = []

    for i in range(N):
        rand_idx = int(random.random() * len(database_uris))
        songs.append(songs_dict[database_uris[rand_idx]].song)

    spotify_json_response = convert_to_spotify_response(songs)
    with open(os.path.join(save_location, save_name), 'w') as f:
        json.dump(spotify_json_response, f)

def generate_histories(json_songs, save_location):
    history_lengths = [10, 50, 1000, 100_000, 300_000]
    for len in history_lengths:
        gen_random_user(json_songs, save_location, len)

if __name__ == "__main__":
    json_songs_file = "/home/mattyb/Desktop/summer_class_2024/DSA/Projects/NicheRank/NicheRank/algo_src/playlist_stats/song_stats_10000.json"
    save_location = "/home/mattyb/Desktop/summer_class_2024/DSA/Projects/NicheRank/NicheRank/algo_src/example_user_history"
    generate_histories(json_songs_file, save_location)