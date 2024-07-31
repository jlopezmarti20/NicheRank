from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Artist:
    name:str = None
    uri:str = None
    def to_dict(self):
        return asdict(self)

@dataclass 
class Song:
    name:str = None
    uri:str = None
    artists: List[Artist] = None
    duration_s: int = None 

    def to_dict(self):
        return{
            'name': self.name,
            'uri': self.uri,
            'artists': [artist.todict() for artist in self.artists],
            'duration_s': self.duration_s
        }

@dataclass
class Artist_Stat:
    artist:Artist = None
    total_s: int = None
    total_songs: int = None
    total_playlists:int = None # how many unique playlists out of 1 million this artist was on 
    weighted_listens: int = None # summation of each listen multiplied by the followers of that song artist
    def to_dict(self):
        return {
            'artist': self.artist.to_dict(),
            'total_s': self.total_s,
            'total_songs': self.total_songs,
            'total_playlists': self.total_playlists,
            'weighted_listens': self.weighted_listens
        }

@dataclass
class Song_Stat:
    song:Song
    total_listens:int
    weighted_listens:int # playlists with higher followers give this more
    
    def to_dict(self):
        return {
            'song': self.song.to_dict(),
            'total_listens': self.total_listens,
            'weighted_listens': self.weighted_listens
        }
    
