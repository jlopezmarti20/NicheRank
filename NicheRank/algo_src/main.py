import file_management as fm
import music_dataclass as md
from analyze_history import Mainstream_Engine, User_Metrics
from users import UserManager

from typing import List, Dict
import os

"""
    This meant to explain how this workflow should go. Each method of loading the data
    can be moldable to however the database works.

"""

DATABASE_DIR = "NicheRank/algo_src/database"
DEFAULT_DATABASE = "database_100000.json"

EXAMPLE_USERS_DIR = "NicheRank/algo_src/example_user_history"
DEFAULT_EXAMPLE_USER = ""


def test_generate_history():

    manager = UserManager()
    user:str = manager.generate_user_history(size=40, pop_level="med", gen_type="greedy")
    songs = manager.get_user_songs(user)

def get_metrics_fake_user(history_size, database_name=DEFAULT_DATABASE, pop_level="med", 
                          gen_type="greedy", sorting_type="q") -> User_Metrics:
    """
        Generate a fake user profile and then runs metric algorithm on that
        history_size: number of listens for history
        database_name: name of the database to use (for if user generated their own)
        pop_level: either low, med, or high for what to use for popularity
        gen_type: which algorithm to use for the playlist generation
        sorting_type: which sorting algorithm to use in metrics. q for quicksort, m for mergesort
    """

    # generate database 
    database_path = os.path.join(DATABASE_DIR, database_name)
    database = fm.deserialize_database(database_path)

    # generate user and username
    user_manager = UserManager(database)
    user_name = user_manager.generate_user_history(size=history_size, pop_level=pop_level, gen_type=gen_type)
    
    # parse in the spotify history
    json_history_path = os.path.join(EXAMPLE_USERS_DIR, user_name)
    song_history:List[md.Song] = fm.parse_spotify_history_json(json_history_path)

    # generate metrics
    metrics_engine = Mainstream_Engine(history=song_history, database=database)
    metrics:User_Metrics = metrics_engine.analyze_history(sorting=sorting_type)

    return metrics

def get_metrics_spotify_user(spotify_history_path, database_name=DEFAULT_DATABASE,
                             sorting_type="q") -> User_Metrics:
    """
        spotify_history_path: path to .json spotify file response
        database_name: name of database to use
        sorting_type: q or m for quicksort or mergesort

        returns: User Metrics object
    """
    # generate database 
    database_path = os.path.join(DATABASE_DIR, database_name)
    database = fm.deserialize_database(database_path)

    # parse history 
    song_history:List[md.Song] = fm.parse_spotify_history_json(spotify_history_path)

    # generate metrics
    metrics_engine = Mainstream_Engine(history=song_history, database=database)
    metrics = metrics_engine.analyze_history(sorting=sorting_type)
    return metrics

def main():
    get_metrics_fake_user(history_size=100000, pop_level="med", gen_type="greedy", sorting_type="q")
    get_metrics_fake_user(history_size=100000, pop_level="low", gen_type="greedy", sorting_type="m")
    

if __name__ == "__main__":
    main()