from typing import Dict, List, Tuple
import random
import os
import json

from file_utils import deserialize_database, parse_spotify_history_json, create_spotify_response
from sorting import Sorter
import music as md

DEFAULT_USERS_DIR = "NicheRank/example_users"

"""
    UserManager generates example histories of various popularity 
    levels as if you have requested from spotify your requests.
"""

class UserManager():

    def __init__(self, database=None) -> None:
        # database is what music database we are pulling from

        if database is None:
            database_dir = "NicheRank/database"
            database_path = os.path.join(database_dir, "database_100000.json")
            database = deserialize_database(database_path)
        elif isinstance(database, str):
            database_dir = "NicheRank/database"
            database_path = os.path.join(database_dir, database)
            database = deserialize_database(database_path)

        self.database_artist_stats = database["artist_stats"]
        self.database_song_stats = database["song_stats"]
        self.users_dir = DEFAULT_USERS_DIR

    def generate_user_history(self, size, pop_level="med", name=None) -> str:
        """
            Creates a user and saved them in example_user_history

            returns a string of that users name
        """

        song_history: List[md.Song] = []

        song_history = self.greedy_generate_history(size=size, pop_level=pop_level)

        save_name = name if name != None else f"user_{pop_level}_{size}"
        save_name = save_name + ".json" if ".json" not in save_name else save_name

        # save this history like its a spotify response        
        spotify_response = create_spotify_response(song_history)
        save_path = os.path.join(self.users_dir, save_name)
        with open(save_path, "w") as f:
            json.dump(spotify_response, f)

        return save_name


    def get_user_songs(self, name) -> List[md.Song]:
        # selects a user from example user history and gets their songs
        name = name + ".json" if ".json" not in name else name
        path = os.path.join(self.users_dir, name)
        if not os.path.exists(path):
            return []
        songs = parse_spotify_history_json(path)
        return songs

    def delete_user(self, name):
        # deletes a user from random user history
        if ".json" not in name:
            name += ".json"

        user_path = os.path.join(self.users_dir, f"{name}")
        if os.path.exists(user_path):
            os.remove(user_path)

    def delete_all_users(self):
        # deletes all users in folder
        for user in os.listdir(self.users_dir):
            os.remove(os.path.join(self.users_dir, user))


    def greedy_generate_history(self, size:int = 10000, pop_level="a"):
        """
            This method uses a greedy algorithm for playlist generation
            pop_level: a, b, c. This reflects what to choose from the limited view during the greedy generation.
            size: number of songs in playlist
        """

        local_size = 15

        # grap a bunch of songs, and then choose the one of nth popularity 
        stats_list = [(uri, song_stat.popularity)for uri, song_stat in self.database_song_stats.items()]

        stats_normed:List[Tuple[str, float]] = UserManager.normalize_pop_list(stats_list)

        i = 0
        history:List[str] = [None] * size

        while (i < size):
            choices = [None] * local_size
            for j in range(local_size): 
                rand_idx = random.randint(0, len(stats_normed) - 1)
                choices[j] = stats_normed[rand_idx]
            # we now want the small, medium, or large 
            # choose the smallest, medium or large value by using a heap 
            Sorter.quicksort(choices)

            if pop_level == "a":
                c_idx = local_size//2 + int(local_size*0.1) # size of greedy algorithm view size
            elif pop_level == "b":
                c_idx = int(local_size*0.2)
            elif pop_level == "c":
                c_idx = 0

            song = choices[c_idx]
            times_listened = random.randint(0,int(size*0.001) + 30) 

            # add this song this many times!
            j = 0
            while (j < times_listened and i < size):
                history[i] = song
                j += 1
                i += 1

        
        # map the uris back to songs
        songs = [None] * size
        for i in range(len(history)):
            (uri, _) = history[i]
            song = self.database_song_stats[uri].song
            songs[i] = song

        return songs
    
    def normalize_pop_list(pop_list: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        mi = min(pop for _, pop in pop_list)
        ma = max(pop for _, pop in pop_list)
        return [(uri, (pop - mi)*100/(ma-mi)) for (uri, pop) in pop_list]

