import file_management as fm
import music_dataclass as md
from analyze_history import Mainstream_Engine, User_Metrics

from typing import List, Dict
import os

"""
    This meant to explain how this workflow should go. Each method of loading the data
    can be moldable to however the database works.

"""

def generate_user():
    pass

def get_history_path()-> str:
    # returns whereever the history is of songs
    example_history_dir = "/home/mattyb/Desktop/summer_class_2024/DSA/Projects/NicheRank/NicheRank/algo_src/example_user_history/"
    example_user_history_50 = "user_rand_173217_50.json"
    return os.path.join(example_history_dir, example_user_history_50)

def test_user():
    json_history_path:str = get_history_path()
    user_song_hist:List[md.Song] = fm.parse_spotify_history_json(json_history_path)
    database_path = "NicheRank/algo_src/database/database_10000.json"
    database = fm.deserialize_database(database_path)

    user_engine = Mainstream_Engine(user_song_hist, database)
    metrics: User_Metrics = user_engine.analyze_history()
    pass

def main():
    test_user()

    pass

if __name__ == "__main__":
    main()