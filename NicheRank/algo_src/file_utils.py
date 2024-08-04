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

def deserialize_optimized_database(database_path)->Dict[Dict[str, md.Artist_Stat], Dict[str, md.Song_Stat]]:
    with open(database_path, 'r') as f:
        json_data = json.load(f)

    artist_dict = {tup[0]: convert_list_to_stat(tup) for tup in json_data["artist_stats"]}
    songs_dict = {tup[0]: convert_list_to_stat(tup) for tup in json_data["song_stats"]}

def convert_list_to_stat(tup: Tuple):
    """
        Converts a Stat Tuple into a Stat Object
        Artist: [artist_uri, name, total_listens, weighted_l, sec_l]
        Song: [song_uri, name, artist_uri_compressed, artist_name, total_listens, weighted_listen, seconds_listened]
    """

    if len(tup) == 5:
        artist = md.Artist_Stat(artist=md.Artist(tup[1], tup[0]),
                                total_s=tup[4],
                                weighted_listens=tup[3],
                                total_songs=tup[2])
        return artist
    elif len(tup) == 7:
        song = md.Song_Stat(
            song=md.Song(
                name=tup[1],
                uri=tup[0],
                artists=[md.Artist(tup[3], tup[2])],
                
                ),
                total_listens=tup[4],
                weighted_listens=5,)
        return song

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
    of json data the 1 Million Playlists database uses.
"""

class DatasetJsonLoader:

    def load_slice(slice_path, version="fast")->List[ Tuple[int, List[md.Song]]]:
        # loads into a list of playlists, each holding num_followers and songs in that playlist
        if version == "fast":
            return DatasetJsonLoader.load_slice(slice_path)
        
        elif version == "slow":
            return DatasetJsonLoader.slow_load_slice(slice_path)
        
        else:
            return DatasetJsonLoader.load_slice(slice_path)

    def load_slice(slice_path)->List[ Tuple[int, List[md.Song]]]:

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

"""
    DatasetToDatabase converts the 1M Playlist Dataset into a database
    with ArtistStats and SongStats saved as a optimized json file

"""
class DatasetToDatabase():

    def __init__(self, database_path, profile=False) -> None:
        
        """
            playlist_path: path to the database file
            load_percent: what percent of the million databases to load (default is max)
            sorting_algorithm: which sorting algorithm to use for this ("map", "merge") are 2 
            profile: if to profile and track sorting time
        """
        self.database_path = database_path 
        self.profile = profile
        self.save_location = "NicheRank/database"

        # check if database path exists
        if (not os.path.exists(self.database_path)):
            raise IOError(f'File doesnt exist: {self.database_path}')
        
    def create_database(self, load_percent=0.5, save=True):

        # loads both artist and music stats together
        song_database: Dict[str, Tuple] = self.extract_dataset_song_stats(load_percent=load_percent)
        artist_database: Dict[str, Tuple] = self.extract_artiststats_from_song_database(song_database, load_percent=load_percent)
        
        num_playlists = int(load_percent * 1_000_000)
        database = {
                    "artist_stats": [ (uri, *stats) for uri, stats in artist_database], 
                    "song_stats": [(uri, *stats) for uri, stats in song_database]
                    }
        # now save these as a database class
        save_name = f"database_{num_playlists}.json"
        save_path = os.path.join(self.save_location, save_name)

        with open(save_path, "w") as f:
            json.dump(database, f, cls=CustomJSONEncoder, indent=2)

    def extract_artiststats_from_song_database(self, song_database:Dict[str, Tuple], load_percent) -> Dict[str, Tuple]:
        """
            loads artist database from already created song database. Magic!!!
        
            returns: {artist_uri:(name, total_listens, weighted_l, sec_l)}
        """

        artist_stats_dict = {}

        for song_uri, (song_name, artist_name, artist_uri, total_listens, weighted_listens, time_s_listened) in song_database.items():
            if artist_uri not in artist_stats_dict:
                new_artist = (artist_name, 0, 0, 0)
                artist_stats_dict[artist_uri] = new_artist
            artist_stats_dict[artist_uri][1] += total_listens
            artist_stats_dict[artist_uri][2] += weighted_listens
            artist_stats_dict[artist_uri][3] += time_s_listened
        return artist_stats_dict
        
    def extract_dataset_song_stats(self, load_percent=0.5, json_parse="fast") -> Dict[str, Tuple]:
        """
            Creates a list of song_stats (unordered)
            returns dict of song info as 
            {str: (name, artist_uri_compressed, total_listens, weighted_listen, seconds_listened)}
        
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
            playlists: List[Tuple[int, List[md.Song]]] = DatasetJsonLoader.load_slice(cur_slice_path, json_parse)

            for j, (followers, playlist) in enumerate(playlists):
                if i == endslice and j == num_playlists % 1000:
                    break

                md.Stats_Extractor.optimized_extract_songstats(playlist, songs_dict, followers=followers)
                    
        return songs_dict
    