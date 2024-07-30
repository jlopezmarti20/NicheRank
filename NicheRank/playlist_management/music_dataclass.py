from dataclasses import dataclass
from typing import List

@dataclass
class Artist:
    name:str
    uri:str

@dataclass 
class Song:
    name:str
    uri:str
    artists: List[Artist]
    duration_s: int 

@dataclass
class Artist_Stat:
    artist:Artist
    total_s: int
    total_songs: int
    total_playlists:int # how many unique playlists out of 1 million this artist was on 
    weighted_listens: int # summation of each listen multiplied by the followers of that song artist

@dataclass
class Song_Stat:
    song:Song
    total_listens:int
    weighted_listens:int


"""
    SCORING_FUNCTIONS????
"""


def basic_score(song_stat:Song_Stat):
    # Simply return which has more songs
    return song_stat.total_listens

def weighted_score(song_stat:Song_Stat, multi=0.6):
    # idk
    return multi * song_stat.weighted_listens + song_stat.total_listens

