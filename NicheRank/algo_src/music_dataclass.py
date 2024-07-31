from dataclasses import dataclass, asdict
from typing import List


# data class
@dataclass
class Artist:
    name:str = None
    uri:str = None

    def __eq__(self, other: object) -> bool:
        if self.uri == other.uri:
            return True
        else:
            return False

@dataclass 
class Song:
    name:str = None
    uri:str = None
    artists: List[Artist] = None
    duration_s: int = None 

    def __eq__(self, other: object) -> bool:
        if self.uri == other.uri:
            return True
        else:
            return False

@dataclass
class Artist_Stat:
    artist:Artist = None
    total_s: int = None
    total_songs: int = None
    total_playlists:int = None # how many unique playlists out of 1 million this artist was on 
    weighted_listens: int = None # summation of each listen multiplied by the followers of that song artist

    @property
    def popularity(self)->float:
        return calculate_artist_popularity(self)

    def get_uri(self):
        return self.artist.uri

    def __add__(self, other):
        if not isinstance(other, Artist_Stat):
            return NotImplemented
        
        # Create a new Artist_Stat with combined values
        return Artist_Stat(
            artist=self.artist,
            total_s=self.total_s + other.total_s,
            total_songs=self.total_songs + other.total_songs,
            total_playlists=self.total_playlists + other.total_playlists,
            weighted_listens=self.weighted_listens + other.weighted_listens
        )
    
    def __eq__(self, other) -> bool:
        if self.artist.uri == other.artist.uri:
            return True
        else:
            return False

@dataclass
class Song_Stat:
    song:Song
    total_listens:int
    weighted_listens:int # playlists with higher followers give this more
    
    @property
    def popularity(self)->float:
        return calculate_song_popularity(self)
    
    def get_uri(self):
        return self.song.uri
    
    def __add__(self, other):
        if not isinstance(other, Song_Stat):
            return NotImplemented
        
        # Create a new Artist_Stat with combined values
        return Song_Stat(
            song=self.song,
            total_listens=self.total_listens + other.total_listens,
            weighted_listens=self.weighted_listens + other.weighted_listens,
        )
    def __eq__(self, other: object) -> bool:
        if self.song == other.song:
            return True
        else:
            return False

def convert_music_to_dict(music)-> dict:
    if isinstance(music, Song_Stat):
        return {
            'song': convert_music_to_dict(music.song),
            'total_listens': music.total_listens,
            'weighted_listens': music.weighted_listens
        }
    
    elif isinstance(music, Artist_Stat):

        return {
            'artist':convert_music_to_dict(music.artist),
            'total_s': music.total_s,
            'total_songs': music.total_songs,
            'total_playlists': music.total_playlists,
            'weighted_listens': music.weighted_listens
        }
        
    elif isinstance(music, Song):
        return {
            'name': music.name,
            'uri': music.uri,
            'artists': [convert_music_to_dict(artist) for artist in music.artists],
            'duration_s': music.duration_s
        }

    elif isinstance(music, Artist):
        return asdict(music)

def calculate_artist_popularity(artist_stat:Artist_Stat):
    # simple popularity metric
    a = 0.05
    weighted_score = artist_stat.weighted_listens*a
    unweighted_score = artist_stat.total_songs

    return weighted_score + unweighted_score

def calculate_song_popularity(song_stat:Song_Stat):

    a = 0.05
    weighted_score = song_stat.weighted_listens*a
    unweighted_score = song_stat.total_listens
    return weighted_score + unweighted_score