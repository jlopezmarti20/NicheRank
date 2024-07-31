from typing import Any, Union, List, Dict
import NicheRank.algo_src.music_dataclass as md


"""
    Stats Extractor takes a list of songs and extracts
    either Song_Stats into a dict, or Artist_Stats

"""

class Stats_Extractor():

    def __call__(songs:List[md.Song], stats_dict:Dict[str, Union[md.Song_Stat, md.Artist_Stat]], playlist_follows=1, type="artist") -> None:
        # extracts a "playlist" (only 1 if this is a persons listening history)
        if type == "artist":
            Stats_Extractor._artist_extract(songs, stats_dict, playlist_follows)
        elif type == "song":
            Stats_Extractor._song_extract(songs, stats_dict, playlist_follows)            
        else:
            print("Unavailible type given!")


    def _artist_extract(songs:List[md.Song], artist_stats_dict:Dict[str, md.Artist_Stat], follows):
        seen_artists = set()
        
        for song in songs:
            for artist in song.artists:
                if artist.uri not in artist_stats_dict:
                    artist_stats_dict[artist.uri] = md.Artist_Stat(artist=artist, total_playlists=0, total_s=0, total_songs=0, weighted_listens=0)
                artist_stats_dict[artist.uri].total_s += song.duration_s
                artist_stats_dict[artist.uri].weighted_listens += follows
                artist_stats_dict[artist.uri].total_songs += 1
                if artist.uri not in seen_artists:
                    artist_stats_dict[artist.uri].total_playlists += 1
                    artist_stats_dict.add(artist.uri)
    def _song_extract(songs:List[md.Song], song_stats_dict: Dict[str, md.Song_Stat], follows):

        for song in songs:
            if song.uri not in song_stats_dict:
                song_stat = md.Song_Stat(song=song, total_listens=0, weighted_listens=0)
                song_stats_dict[song.uri] = song_stat 
            song_stats_dict[song.uri].total_listens += 1
            song_stats_dict[song.uri].weighted_listens += follows