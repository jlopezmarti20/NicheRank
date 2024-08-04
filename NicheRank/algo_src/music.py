from dataclasses import dataclass, asdict, field
from typing import List, Dict

"""
    Music stores classes for artists, songs, 
    songstats and artiststats. 
"""
 
class Music:
    
    def __init__(self, uri:str = None) -> None:
        self.uri:str = self.set_uri(uri) 

    def set_uri(self, uri) -> str:
        return uri.rsplit(":", 1)[-1] 

    def get_uri(self):
        return self.uri
    
    def __eq__(self, other: object) -> bool:
        return self.uri == other.uri

# Stores a artists name and uri, checks if artists are equal
class Artist(Music):
    name:str = None
    uri:str = None

    def  __init__(self, name:str = None, uri: str = None) -> None:
        super().__init__(uri)
        self.name = name


class Song(Music):
    def __init__(self, name: str = None, uri: str = None, artists:List[Artist]=None):
        super().__init__(uri)
        self.name = name
        self.artists = artists if artists is not None else []

class Stat:
    def __init__(self, total_listens: int = None, weighted_listens: int = None):
        self.total_listens = total_listens
        self.weighted_listens = weighted_listens

    @property
    def popularity(self) -> float:
        raise NotImplementedError("Subclasses should implement this method")

    def get_uri(self):
        raise NotImplementedError("Subclasses should implement this method")

    def __add__(self, other):
        raise NotImplementedError("Subclasses should implement this method")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Stat):
            return NotImplemented
        return self.get_uri() == other.get_uri()

# stores stats about an artist
class Artist_Stat(Stat):

    def __init__(self, artist:Artist, total_listens: int, weighted_listens: int):
        super().__init__(total_listens, weighted_listens)
        self.artist = artist

    @property
    def popularity(self)->float:
        # simple popularity metric for how much an artist has been listened to.

        a = 0.05
        weighted_score = self.weighted_listens*a
        unweighted_score = self.total_listens

        return weighted_score + unweighted_score

    def get_uri(self):
        return self.artist.uri

    def __add__(self, other):
        if not isinstance(other, Artist_Stat):
            return NotImplemented
        
        # Create a new Artist_Stat with combined values
        return Artist_Stat(
            artist=self.artist,
            total_songs=self.total_listens + other.total_listens,
            weighted_listens=self.weighted_listens + other.weighted_listens
        )

# songstats about a song from how it has been listened to.
class Song_Stat(Stat):

    def __init__(self, song:Song, total_listens: int = None, weighted_listens: int = None):
        super().__init__(total_listens, weighted_listens)
        self.song = song

    @property
    def popularity(self)->float:
        # simple metric for a songs listening time
        a = 0.05
        weighted_score = self.weighted_listens*a
        unweighted_score = self.total_listens
        return weighted_score + unweighted_score
        
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

"""
    The stats extractor takes a list of songs and extracts its
    artist stats or songstats from it.
"""

class Stats_Extractor():

    def extract_artist_stats_from_songs(songs: List[Song]) -> List[Artist_Stat]:
        # extract artist stats from songs
        AS_dict = {}
        Stats_Extractor.extract_artiststats(songs, AS_dict, 1)
        return [stat for uri, stat in AS_dict.items()]

    def extract_artiststats(songs:List[Song], artist_stats_dict:Dict[str, Artist_Stat], followers):
        
        for song in songs:
            for artist in song.artists:
                if artist.uri not in artist_stats_dict:
                    artist_stats_dict[artist.uri] = Artist_Stat(artist=artist, total_listens=0, weighted_listens=0)
                artist_stats_dict[artist.uri].weighted_listens += followers
                artist_stats_dict[artist.uri].total_listens += 1

    def extract_song_stats_from_songs(songs: List[Song]) -> List[Song_Stat]:
        SS_dict = {}
        Stats_Extractor.extract_songstats(songs, SS_dict, 1)
        return [stat for uri, stat in SS_dict.items()]    

    def extract_songstats(songs:List[Song], song_stats_dict: Dict[str, Song_Stat], followers):

        for song in songs:
            if song.uri not in song_stats_dict:
                song_stat = Song_Stat(song=song, total_listens=0, weighted_listens=0)
                song_stats_dict[song.uri] = song_stat 
            song_stats_dict[song.uri].total_listens += 1
            song_stats_dict[song.uri].weighted_listens += followers


    def optimized_extract_songstats(playlist:List[Song], optimized_songs_dict: Dict[str, List], followers=1):
        # optimized extracts songstats from playlist
        # {song_uri: [name, artist_uri, artist_name, total_listens, weighted_listens]}
        
        for song in playlist:
            if song.uri not in optimized_songs_dict:
                song_stat = [song.name, song.artists[0].name, song.artists[0].get_uri(), 0, 0]
                optimized_songs_dict[song.uri] = song_stat 
            optimized_songs_dict[song.uri][3] += 1 # total listens
            optimized_songs_dict[song.uri][4] += followers # weighted listens

        pass