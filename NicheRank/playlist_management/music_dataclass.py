from dataclasses import dataclass
from typing import Any

@dataclass
class Artist:
    name:str
    uri:str

@dataclass 
class Song:
    name:str
    uri:str
    artists: list[Artist]
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

# todo generate dummy artist popularity calculators to use
class Artist_Popularity_Score_Calculator():

    def __init__(self, w_m=0) -> None:
        self.weight_multiplier = w_m


    def __call__(self, artist:Artist_Stat) -> float:
        # depends on which one we load 
        sum = artist.total_playlists

    def _weighted_popularity(self, artist):
        return artist
    
    def length_weighted(self, artist:Artist_Stat):
        # returns artist stats
        return


# todo create sample song popularity calculators 
class Song_Popularity_Score_Calculator():

    def __init__(self) -> None:
        pass

    def __call__(self, song_stat:Song_Stat) -> Any:
        pass