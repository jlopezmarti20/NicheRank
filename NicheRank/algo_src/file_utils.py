import json
from typing import List, Tuple, Dict
import os
from tqdm import tqdm
import time

import music as md

DEFAULT_DATASET_LOCATION = "NicheRank/playlist_dataset"
DEFAULT_DATABASE_DIRECTORY = "NicheRank/database"

"""
    Methods for creating or reading json information and database files.
"""

def deserialize_database(database_path)->Dict[Dict[str, md.Artist_Stat], Dict[str, md.Song_Stat]]:
    # turns a database of json files into a dictionary of Music Objects
    artist_path = os.path.join(database_path, "artist_stats.json")
    song_path = os.path.join(database_path, "song_stats.json")
    
    with open(artist_path, 'r') as f:
        artist_stats = json.load(f)

    with open(song_path, 'r') as f:
        song_stats = json.load(f)

    artist_dict = {tup[0]: convert_list_to_stat(tup) for tup in artist_stats}
    songs_dict = {tup[0]: convert_list_to_stat(tup) for tup in song_stats}

    return {"artist_stats": artist_dict,
            "song_stats": songs_dict}

def convert_list_to_stat(tup: Tuple)-> md.Stat:
    """
        Converts a Stat Tuple into a Stat Object
        Artist: [artist_uri, name, total_listens, weighted_l]
    """

    if len(tup) == 4:
        artist = md.Artist_Stat(artist=md.Artist(name=tup[1], uri=tup[0]),
                                weighted_listens=tup[3],
                                total_listens=tup[2])
        return artist
    elif len(tup) == 6:
        # [song_uri, name, artist_uri_compressed, artist_name, total_listens, weighted_listen]
        song = md.Song_Stat(
            song=md.Song(
                    name=tup[1],
                    uri=tup[0],
                    artists=[md.Artist(uri=tup[3], name=tup[2])],
                ),
                total_listens=tup[4],
                weighted_listens=tup[5]
                )
        return song

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
        song = md.Song(name=track["name"],uri=track["uri"], artists=artists_list)
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

    def __init__(self, dataset_path=DEFAULT_DATASET_LOCATION, save_location=DEFAULT_DATABASE_DIRECTORY, profile=False) -> None:
        
        """
            playlist_path: path to the database file to be saved
            load_percent: what percent of the million databases to load (default is max)
            sorting_algorithm: which sorting algorithm to use for this ("map", "merge") are 2 
            profile: if to profile and track sorting time
        """
        self.dataset_path = dataset_path 
        self.profile = profile
        self.save_location = save_location

        # check if database path exists
        if (not os.path.exists(self.dataset_path)):
            raise IOError(f'File doesnt exist: {self.dataset_path}')
        
    def create_database(self, load_percent=0.5, save=True):

        # loads both artist and music stats together
        songstat_dir: Dict[str, Tuple] = self.extract_dataset_song_stats(load_percent=load_percent)
        artiststat_dir: Dict[str, Tuple] = self.extract_artiststats_from_song_database(songstat_dir, load_percent=load_percent)
        
        num_playlists = int(load_percent * 1_000_000)
        artist_stats = [ (uri, *stats) for uri, stats in artiststat_dir.items()]
        song_stats = [(uri, *stats) for uri, stats in songstat_dir.items()]

        # now save these into a directory with artists json and songs json

        current_time = time.localtime()

        # Format the time as a string
        time_string = time.strftime("%H:%M:%S", current_time)

        # Format the date and time as a string
        dir_name = f"db_{num_playlists}_{time_string}"
        save_path = os.path.join(self.save_location, dir_name)
        os.mkdir(save_path)
        # save song and artist stats into their sperate json files
        artiststats_path = os.path.join(save_path, "artist_stats.json")
        with open(artiststats_path, "w") as f:
            json.dump(artist_stats, f)

        songstats_path = os.path.join(save_path, "song_stats.json")
        with open(songstats_path, "w") as f:
            json.dump(song_stats, f)

    def extract_artiststats_from_song_database(self, song_database:Dict[str, List], load_percent) -> Dict[str, Tuple]:
        """
            loads artist database from already created song database. 
            returns: {artist_uri:(name, total_listens, weighted_l, sec_l)}
        """

        artist_stats_dict = {}

        for song_uri, (song_name, artist_name, artist_uri, total_listens, weighted_listens) in tqdm(song_database.items(), desc="Processing song stats into artist stats."):
            if artist_uri not in artist_stats_dict:
                new_artist = [artist_name, 0, 0]
                artist_stats_dict[artist_uri] = new_artist
            artist_stats_dict[artist_uri][1] += total_listens
            artist_stats_dict[artist_uri][2] += weighted_listens
            
        return artist_stats_dict
        
    def extract_dataset_song_stats(self, load_percent=0.5) -> Dict[str, List]:
        """
            Creates a list of song_stats (unordered)
            returns dict of song info as 
            {str: (name, artist_uri, artist_name, total_listens, weighted_listens)}
        
        """
        if (load_percent < 0.0 or load_percent > 1.0):
            load_percent = 0.5
        else:
            load_percent = load_percent

        num_playlists = int(load_percent * 1_000_000) # how many playlists to parse out of 1M
        # first, load every artist in every playlist
        data_dir = os.path.join(self.dataset_path, 'data')
        endslice: int = num_playlists // 1000
        slices: List[str] = os.listdir(data_dir)
        songs_dict: Dict[str, md.Song_Stat] = {} # song_uri: song_stat dataclass
        slice_range = tqdm(range(endslice + 1), disable=not self.profile, desc="Processing songs into songstats.")

        for i in slice_range:
            cur_slice = slices[i]
            cur_slice_path = os.path.join(data_dir, cur_slice)
            playlists: List[Tuple[int, List[md.Song]]] = DatasetJsonLoader.load_slice(cur_slice_path)

            for j, (followers, playlist) in enumerate(playlists):
                if i == endslice and j == num_playlists % 1000:
                    break

                md.Stats_Extractor.optimized_extract_songstats(playlist, songs_dict, followers=followers)
                    
        return songs_dict