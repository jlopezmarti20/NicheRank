from dataclasses import dataclass, asdict, field
from typing import List, Dict


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
    artists: List[Artist] = field(default_factory=list)
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
        if self.artist == other.artist:
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

def convert_dict_to_music(json_dict):
    # dict is a dictionary representing a dataclass object
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
                              total_playlists=json_dict["total_playlists"],
                              weighted_listens=json_dict["weighted_listens"])
    
    elif "song" in json_dict:
        # this is a song_stat
        return Song_Stat(song=convert_dict_to_music(json_dict["song"]),
                            total_listens=json_dict["total_listens"],
                            weighted_listens=json_dict["weighted_listens"])
    
    elif len(json_dict) == 2:
        # this is a artist 
        return Artist(name=json_dict["name"], uri=json_dict["uri"])

# for json encoding
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
    
    else:
        return None


class Stats_Extractor():

    def extract_artist_stats_from_songs(songs: List[Song]) -> List[Artist_Stat]:
        # extract artist stats from songs
        AS_dict = {}
        Stats_Extractor.extract_artiststats(songs, AS_dict, 1)
        return [stat for uri, stat in AS_dict.items()]

    def extract_artiststats(songs:List[Song], artist_stats_dict:Dict[str, Artist_Stat], followers):
        seen_artists = set()
        
        for song in songs:
            for artist in song.artists:
                if artist.uri not in artist_stats_dict:
                    artist_stats_dict[artist.uri] = Artist_Stat(artist=artist, total_playlists=0, total_s=0, total_songs=0, weighted_listens=0)
                artist_stats_dict[artist.uri].total_s += song.duration_s
                artist_stats_dict[artist.uri].weighted_listens += followers
                artist_stats_dict[artist.uri].total_songs += 1
                if artist.uri not in seen_artists:
                    artist_stats_dict[artist.uri].total_playlists += 1
                    seen_artists.add(artist.uri)
    
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

