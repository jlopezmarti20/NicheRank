from dataclasses import dataclass
from typing import List

@dataclass
class Artist:
    name:str = None
    uri:str = None

@dataclass 
class Song:
    name:str = None
    uri:str = None
    artists: List[Artist] = None
    duration_s: int = None 

@dataclass
class Artist_Stat:
    artist:Artist = None
    total_s: int = None
    total_songs: int = None
    total_playlists:int = None # how many unique playlists out of 1 million this artist was on 
    weighted_listens: int = None # summation of each listen multiplied by the followers of that song artist

@dataclass
class Song_Stat:
    song:Song
    total_listens:int
    weighted_listens:int # playlists with higher followers give this more


