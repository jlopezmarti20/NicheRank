import json
import music_dataclass as md

"""
    Methods for parsing json into objects for python class use

"""


def parse_spotify_history_json(response_path:str)->list[md.Song]:
    """
        parse playlist spotify into a list of dictionaries of song stats 
        see https://developer.spotify.com/documentation/web-api/reference/get-recently-played for more on responses
        return: 
            [
                {
                    song_name: str,
                    artists: [artist_name],
                    song_id: string
                    duration_s: int                    
                }
            ]
    """

    with open(response_path, "r") as f:
        response_json = json.load(f)

    recently_played: list[md.Song_Stat] = [] # list of song dataclasses
    for play_history in response_json["items"]:
        # organizes json object into more easily parsable list of song dataclasses

        track = play_history["track"]
        artists = track["artists"]
        # process as list of artist names? 
        artists_list:list[md.Artist] = []
        for artist in artists:
            artists_list.append(md.Artist(name=artist["name"], id=artist["id"]))
        song = md.Song(name=track["name"],id=track["id"], artists=artists_list, duration_s=track["duration_ms"] / 60)
        recently_played.append(song) 

    return recently_played

class Json_Playlist_Database_Handler():

    custom_location = "/media/mattyb/UBUNTU 22_0/P3-template-main/spotify_million_playlist_dataset"

    def __init__(self, dataset_location:str =None, num_playlists:int = None) -> None:
        
        """
            dataset_location: string of the filepath to dataset
            num_playlists: value from 0 to 1 Million that gives number of playlists to be included in handler
        """

        self.dataset_location = dataset_location if dataset_location is not None else self.custom_location
        self.num_playlists = 1_000_000 if num_playlists is None else num_playlists

    def get_slice_filename(i_slice) ->str:
        # returns string to the 
        pass

    def get_playlist_json(i:int ):
        # returns a dict of the ith playlist in dataset
        pass