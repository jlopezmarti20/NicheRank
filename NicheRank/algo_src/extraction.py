from typing import Any, Union, List, Dict

import music_dataclass as md


"""
    Stats Extractor takes a list of songs and returns a Dict of 
    the URI to Music Object

"""

class Stats_Extractor():

    def history_AS_extract(songs: List[md.Song]) -> List[md.Artist_Stat]:
        AS_dict = {}
        Stats_Extractor.extract_artiststats(songs, AS_dict, 1)
        return [stat for uri, stat in AS_dict.items()]

    def extract_artiststats(songs:List[md.Song], artist_stats_dict:Dict[str, md.Artist_Stat], followers):
        seen_artists = set()
        
        for song in songs:
            for artist in song.artists:
                if artist.uri not in artist_stats_dict:
                    artist_stats_dict[artist.uri] = md.Artist_Stat(artist=artist, total_playlists=0, total_s=0, total_songs=0, weighted_listens=0)
                artist_stats_dict[artist.uri].total_s += song.duration_s
                artist_stats_dict[artist.uri].weighted_listens += followers
                artist_stats_dict[artist.uri].total_songs += 1
                if artist.uri not in seen_artists:
                    artist_stats_dict[artist.uri].total_playlists += 1
                    seen_artists.add(artist.uri)
    
    def history_SS_extract(songs: List[md.Song]) -> List[md.Song_Stat]:
        SS_dict = {}
        Stats_Extractor.extract_songstats(songs, SS_dict, 1)
        return [stat for uri, stat in SS_dict.items()]    

    def extract_songstats(songs:List[md.Song], song_stats_dict: Dict[str, md.Song_Stat], followers):

        for song in songs:
            if song.uri not in song_stats_dict:
                song_stat = md.Song_Stat(song=song, total_listens=0, weighted_listens=0)
                song_stats_dict[song.uri] = song_stat 
            song_stats_dict[song.uri].total_listens += 1
            song_stats_dict[song.uri].weighted_listens += followers

