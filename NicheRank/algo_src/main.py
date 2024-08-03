import file_management as fm
import music_dataclass as md
from analyze_history import Mainstream_Engine, User_Metrics

from typing import List, Dict
import os

"""
    This meant to explain how this workflow should go. Each method of loading the data
    can be moldable to however the database works.

"""

def get_history_path()-> str:
    # returns whereever the history is of songs
    example_history_dir = "/home/mattyb/Desktop/summer_class_2024/DSA/Projects/NicheRank/NicheRank/algo_src/example_user_history/"
    example_user_history_50 = "user_rand_173217_50.json"
    return os.path.join(example_history_dir, example_user_history_50)
    
def get_global_artiststats() -> Dict[str, md.Artist_Stat]:
    artists_database = "NicheRank/algo_src/playlist_stats/artist_stats_10000.json"
    return fm.global_playlist_to_music_dict(artists_database)

def get_global_songstats()->Dict[str, md.Song_Stat]:
    songs_database = "NicheRank/algo_src/playlist_stats/song_stats_10000.json"
    return fm.global_playlist_to_music_dict(songs_database)

def main():

    json_history_path:str = get_history_path()
    user_song_hist:List[md.Song] = fm.parse_spotify_history_json(json_history_path)

    global_songstats = get_global_songstats()
    global_artiststats = get_global_artiststats()

    user_engine = Mainstream_Engine(user_song_hist, global_artiststats, global_songstats)
    metrics: User_Metrics = user_engine.analyze_history()
    pass



if __name__ == "__main__":
    main()