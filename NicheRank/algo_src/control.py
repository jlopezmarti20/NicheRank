import sys
from typing import List, Dict
import os
import file_utils as fm
import music as md
from analyze_history import HistoryAnalyzer, User_Metrics
from users import UserManager
import itertools



"""
    Control allows all the pieces to come together from the Database, User, and Analytics engine
    to produce final results.
"""

DATABASE_DIR = "NicheRank/database"
DEFAULT_DATABASE = "default_db_100000" # by default use the 100_000 songs database

EXAMPLE_USERS_DIR = "NicheRank/example_users"


def test_generate_history():

    manager = UserManager()
    user:str = manager.generate_user_history(size=40, pop_level="b")
    songs = manager.get_user_songs(user)

def get_metrics_fake_user(history_size, database_name=DEFAULT_DATABASE, pop_level="med", 
                          sorting_type="q") -> User_Metrics:
    """
        Generate a fake user profile and then runs metric algorithm on that
        history_size: number of listens for history
        database_name: name of the database to use (for if user generated their own)
        pop_level: either a,b,c for greedy algorithm choices
        sorting_type: which sorting algorithm to use in metrics. q for quicksort, m for mergesort
    """

    # generate database 
    database_path = os.path.join(DATABASE_DIR, database_name)
    database = fm.deserialize_database(database_path)

    # generate user and username
    user_manager = UserManager(database)
    user_name = user_manager.generate_user_history(size=history_size, pop_level=pop_level)
    
    # parse in the spotify history
    json_history_path = os.path.join(EXAMPLE_USERS_DIR, user_name)
    song_history:List[md.Song] = fm.parse_spotify_history_json(json_history_path)

    # generate metrics
    metrics_engine = HistoryAnalyzer(history=song_history, database=database)
    metrics:User_Metrics = metrics_engine.analyze_history(sorting=sorting_type)

    return metrics

def get_metrics_spotify_user(history, database_name=DEFAULT_DATABASE,
                             sorting_type="q") -> User_Metrics:
    """
        history: either a str path to .json spotify file response, or a dictionary of the json response
        database_name: name of database to use
        sorting_type: q or m for quicksort or mergesort

        returns: User Metrics object
    """

    # generate database 
    database_path = os.path.join(DATABASE_DIR, database_name)
    database = fm.deserialize_database(database_path)
    
    # parse history 
    song_history:List[md.Song] = fm.parse_spotify_history_json(history)

    # generate metrics
    metrics_engine = HistoryAnalyzer(history=song_history, database=database)
    metrics = metrics_engine.analyze_history(sorting=sorting_type)
    return metrics

def test_fake_user_gen_examples():
    size_choices = [100, 1000, 100000]
    pop_levels = ["a", "b", "c"]
    sorts = ["q", "m"]
    test_combinations = itertools.product(size_choices, pop_levels, sorts)
    resulting_metrics = []
    print("Testing creation of fake users")
    for size, pop_level, s in test_combinations:
        print(f"testing {size} {pop_level} {s}")
        metric = get_metrics_fake_user(history_size=size, pop_level=pop_level, sorting_type=s)    
        resulting_metrics.append(metric)
        print(f"pop score of {metric.pop_score}")
    
    print("finished testing all the parts!")

def test_spotify_history():
    history = "user_history.json"
    sorting_type = "m"
    database_name = "db_10000"
    get_metrics_spotify_user(history, sorting_type=sorting_type, database_name=database_name)


def large_user_test():

    m1 = get_metrics_fake_user(history_size=100000, pop_level="a", sorting_type="q")
    m2 = get_metrics_fake_user(history_size=100000, pop_level="b", sorting_type="m")


def main():
    test_fake_user_gen_examples()

if __name__ == "__main__":
    main()