import json
from typing import List, Tuple, Dict, Union
import os
from dataclasses import asdict
from tqdm import tqdm
import sys
import os
import sys

import music as md

"""
    Methods for creating or reading json information and database files.
"""


def deserialize_database(stats_json_path) -> Dict[Dict[str, md.Artist_Stat], Dict[str, md.Song_Stat]]:
    # converts Database_json into Database Dict with artist_stats: and song_stats:
    with open(stats_json_path, 'r') as f:
        json_data = json.load(f)

    artists_dict = {uri: md.convert_dict_to_music(artist) for uri, artist in json_data["artist_stats"].items()}
    songs_dict = {uri: md.convert_dict_to_music(song_stat) for uri, song_stat in json_data["song_stats"].items()}
    return {"artist_stats": artists_dict,
            "song_stats": songs_dict}

class CustomJSONEncoder(json.JSONEncoder):
    # encodes a music object into a dictionary
    def default(self, obj):
        if isinstance(obj, (md.Artist_Stat, md.Song_Stat, md.Artist, md.Song)):
            return md.convert_music_to_dict(obj)
        return super().default(obj)

def parse_spotify_history_json(response)->List[md.Song]:
    """
        parse spotify history json into a list  of song stats 
        see https://developer.spotify.com/documentation/web-api/reference/get-recently-played 
        for more on responses
        return: List[md.Song]
    """
    if isinstance(response, str):
        # response is a file location  
        with open(response, "r") as f:
            response_json = json.load(f)
    elif isinstance(response, dict):
        response_json = response
    else:
        print("WRONG RESPONSE TYPE GIVEN")
        return None
        
    recently_played: List[md.Song] = [] # list of song dataclasses
    for play_history in response_json["items"]:
        # organizes json object into more easily parsable list of song dataclasses

        track = play_history["track"]
        artists = track["artists"]
        # process as list of artist names? 
        artists_list: List[md.Artist] = []
        for artist in artists:
            artists_list.append(md.Artist(name=artist["name"], uri=artist["uri"]))
        song = md.Song(name=track["name"],uri=track["uri"], artists=artists_list, duration_s=track["duration_ms"] / 60)
        recently_played.append(song) 

    return recently_played

def create_spotify_response(songs: List[md.Song]) -> dict:
    # Turns a list of songs into a spotify response dictionary. Used in user generation
    
    response_items = []
    for song in songs:
        track = {
            "track": {
                "name": song.name,
                "uri": song.uri,
                "artists": [{"name": artist.name, "uri": artist.uri} for artist in song.artists],
                "duration_ms": int(song.duration_s * 60 * 1000)  # converting back to milliseconds
            }
        }
        response_items.append(track)
    
    response = {
        "items": response_items
    }
    return response

"""
    The dataset loader class is used to load and work with the slices
    the 1 Million Playlists database uses.
"""

class DatasetLoader:

    def load_slice(slice_path, version="fast")->List[ Tuple[int, List[md.Song]]]:
        # loads into a list of playlists, each holding num_followers and songs in that playlist
        if version == "fast":
            return DatasetLoader.faster_load_slice(slice_path)
        
        elif version == "slow":
            return DatasetLoader.slow_load_slice(slice_path)
        
        else:
            return DatasetLoader.faster_load_slice(slice_path)

    def slow_load_slice(slice_path)->List[ Tuple[int, List[md.Song]]]:
        
        # loads into a list of playlists, each holding num_followers and songs in that playlist

        with open(slice_path, 'r') as f:
            slice_json = json.load(f)

        parsed_slice:list[(int, list[md.Song])] = []

        for playlist in slice_json["playlists"]:
            followers = playlist["num_followers"]
            parsed_playlist = []
            for track in playlist["tracks"]:
                song = md.Song(name=track["track_name"], 
                            uri=track["track_uri"],
                            artists=[md.Artist(name=track["artist_name"], uri=track["artist_uri"])],
                            duration_s=track["duration_ms"]/1000
                            )
                parsed_playlist.append(song)

            parsed_slice.append((followers, parsed_playlist))

        return parsed_slice


    def faster_load_slice(slice_path)->List[ Tuple[int, List[md.Song]]]:

        # use a list comprehension instead

        with open(slice_path, 'r') as f:
            slice_json = json.load(f)
        # Parse playlists into the desired format
        parsed_slice = [
            (
                playlist["num_followers"],
                [
                    md.Song(
                        name=track["track_name"],
                        uri=track["track_uri"],
                        artists=[md.Artist(name=track["artist_name"], uri=track["artist_uri"])],
                        duration_s=track["duration_ms"] / 1000  # Corrected conversion to seconds
                    )
                    for track in playlist["tracks"]
                ]
            )
            for playlist in slice_json["playlists"]
        ]

        return parsed_slice

# behavior class
class Dataset_Extractor():

    def __init__(self, database_path, profile=False) -> None:
        
        """
            playlist_path: path to the database file
            load_percent: what percent of the million databases to load (default is max)
            sorting_algorithm: which sorting algorithm to use for this ("map", "merge") are 2 
            profile: if to profile and track sorting time
        """
        self.database_path = database_path 
        self.profile = profile
        self.save_location = "NicheRank/algo_src/database"

        # check if database path exists
        if (not os.path.exists(self.database_path)):
            raise IOError(f'File doesnt exist: {self.database_path}')
        
    def create_database(self, load_percent=0.5, save=True):

        # loads both artist and music stats together
        artist_database: Dict[str, md.Artist_Stat] = self.extract_dataset_artist_stats(load_percent=load_percent)
        song_database: Dict[str, md.Song_Stat] = self.extract_dataset_song_stats(load_percent=load_percent)

        num_playlists = int(load_percent * 1_000_000)
        database = {
                    "artist_stats": artist_database, 
                    "song_stats": song_database
                    }
        # now save these as a database class
        save_name = f"database_{num_playlists}.json"
        save_path = os.path.join(self.save_location, save_name)

        with open(save_path, "w") as f:
            json.dump(database, f, cls=CustomJSONEncoder, indent=2)


    def extract_dataset_artist_stats(self, load_percent=0.5,json_parse="fast") -> Dict[str, md.Artist_Stat]:
        """
            creates a list of artist stats (unordered) 
        """

        if (load_percent < 0.0 or load_percent > 1.0):
            load_percent = 0.5
        else:
            load_percent = load_percent

        num_playlists = int(load_percent * 1_000_000) # how many playlists to parse out of 1M
        # first, load every artist in every playlist
        data_dir = os.path.join(self.database_path, 'data')
        endslice: int = num_playlists // 1000
        slices: List[str] = os.listdir(data_dir)
        artist_dict: Dict[str, md.Artist_Stat] = {} # artist_uri: Artist_Stat dataclass
        slice_range = tqdm(range(endslice + 1), disable= not self.profile)

        for i in slice_range:
            # current slice has playlists 
            cur_slice = slices[i]
            cur_slice_path = os.path.join(data_dir, cur_slice)
            playlists: List[Tuple[int, List[md.Song]]] = DatasetLoader.load_slice(cur_slice_path, json_parse)
            
            for j, (followers, playlist) in enumerate(playlists):
                if i == endslice and j == num_playlists % 1000:
                    # for processing final slice
                    break
                md.Stats_Extractor.extract_artiststats(playlist, artist_dict, followers=followers)
        return artist_dict        
        
    def extract_dataset_song_stats(self, load_percent=0.5, json_parse="fast") -> Dict[str, md.Song_Stat]:
        """
            Creates a list of song_stats (unordered)
        
        """
        if (load_percent < 0.0 or load_percent > 1.0):
            load_percent = 0.5
        else:
            load_percent = load_percent

        num_playlists = int(load_percent * 1_000_000) # how many playlists to parse out of 1M
        # first, load every artist in every playlist
        data_dir = os.path.join(self.database_path, 'data')
        endslice: int = num_playlists // 1000
        slices: List[str] = os.listdir(data_dir)
        songs_dict: Dict[str, md.Song_Stat] = {} # song_uri: song_stat dataclass
        slice_range = tqdm(range(endslice + 1), disable=not self.profile)

        for i in slice_range:
            cur_slice = slices[i]
            cur_slice_path = os.path.join(data_dir, cur_slice)
            playlists: List[Tuple[int, List[md.Song]]] = DatasetLoader.load_slice(cur_slice_path, json_parse)

            for j, (followers, playlist) in enumerate(playlists):
                if i == endslice and j == num_playlists % 1000:
                    break

                md.Stats_Extractor.extract_songstats(playlist, songs_dict, followers=followers)
                    
        return songs_dict