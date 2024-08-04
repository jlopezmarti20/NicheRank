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
    def __init__(self, name: str = None, uri: str = None, artists:List[Artist]=None, duration_s: int = None):
        super().__init__(uri)
        self.name = name
        self.artists = artists if artists is not None else []
        self.duration_s = int(duration_s)

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
    artist:Artist = None
    total_s: int = None
    total_songs: int = None
    weighted_listens: int = None # summation of each listen multiplied by the followers of that song artist

    def __init__(self, artist:Artist, uri: str, total_listens: int, weighted_listens: int):
        super().__init__(total_listens, weighted_listens)

    @property
    def popularity(self)->float:
        # simple popularity metric for how much an artist has been listened to.

        a = 0.05
        weighted_score = self.weighted_listens*a
        unweighted_score = self.total_songs

        return weighted_score + unweighted_score

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
            weighted_listens=self.weighted_listens + other.weighted_listens
        )

# songstats about a song from how it has been listened to.
class Song_Stat(Stat):
    song:Song
    total_listens:int
    weighted_listens:int # playlists with higher followers give this more

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

def convert_dict_to_music(json_dict):
    # converts a dict representation of a artist, song or stat into that object
    
    if "artists" in json_dict:
        # this is a song 
        song = Song(name=json_dict["name"],
                       uri=json_dict["uri"],
                       duration_s=json_dict["duration_s"])
        for artist in json_dict["artists"]:
            song.artists.append(convert_dict_to_music(artist))
        return song

    elif "artist" in json_dict:
        # this is an artist_stat
        return Artist_Stat(artist=convert_dict_to_music(json_dict["artist"]),
                              total_s=json_dict["total_s"],
                              total_songs=json_dict["total_songs"] ,
                              weighted_listens=json_dict["weighted_listens"])
    
    elif "song" in json_dict:
        # this is a song_stat
        return Song_Stat(song=convert_dict_to_music(json_dict["song"]),
                            total_listens=json_dict["total_listens"],
                            weighted_listens=json_dict["weighted_listens"])
    
    elif len(json_dict) == 2:
        # this is a artist 
        return Artist(name=json_dict["name"], uri=json_dict["uri"])


def convert_music_to_dict(music)-> dict:
    # encodes a music object as a dictionary for storage
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
    
    else:
        return None


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
                    artist_stats_dict[artist.uri] = Artist_Stat(artist=artist, total_s=0, total_songs=0, weighted_listens=0)
                artist_stats_dict[artist.uri].total_s += song.duration_s
                artist_stats_dict[artist.uri].weighted_listens += followers
                artist_stats_dict[artist.uri].total_songs += 1

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
        # {song_uri: (songname, artist_name, artist_uri, artist_name, total_listens, weighted_listens, time_listened)}
        
        for song in playlist:
            if song.uri not in optimized_songs_dict:
                song_stat = [song.name, song.artists[0].name, song.artists[0].get_uri(), 0, 0, 0]
                optimized_songs_dict[song.uri] = song_stat 
            optimized_songs_dict[song.uri][3] += 1 # total listens
            optimized_songs_dict[song.uri][4] += followers # weighted listens
            optimized_songs_dict[song.uri][5] += song.duration_s # time listened

        pass