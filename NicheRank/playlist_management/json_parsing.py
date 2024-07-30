import json
import music_dataclass as md

"""
    Methods for parsing json into objects for python class use.
    This can be edited according to however the database is setup.

"""
from typing import List, Tuple


def parse_spotify_history_json(response_path:str)->List[md.Song]:
    """
        parse playlist spotify into a list of dictionaries of song stats 
        see https://developer.spotify.com/documentation/web-api/reference/get-recently-played for more on responses
        return: 
            [
                {
                    song_name: str,
                    artists: [artist_name],
                    song_uri: string
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
            artists_list.append(md.Artist(name=artist["name"], uri=artist["uri"]))
        song = md.Song(name=track["name"],uri=track["uri"], artists=artists_list, duration_s=track["duration_ms"] / 60)
        recently_played.append(song) 

    return recently_played

def load_slice(slice_path)->List[Tuple[int, list[md.Song]]]:
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
                           duration_s=track["duration_ms"]/60
                           )
            parsed_playlist.append(song)

        parsed_slice.append((followers, parsed_playlist))

    return parsed_slice