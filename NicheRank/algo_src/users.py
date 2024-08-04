from typing import Dict, List, Tuple
import random
import os
import json

from file_management import deserialize_database, parse_spotify_history_json, create_spotify_response
from sorting import Sorter
import music as md

"""
    UserManager generates example histories of various popularity 
    levels as if you have requested from spotify your requests.
"""

class UserManager():
    #WAHOOOo
    def __init__(self, database=None) -> None:
        # database is what music database we are pulling from

        if database is None:
            database_dir = "NicheRank/algo_src/database"
            database_path = os.path.join(database_dir, "database_100000.json")
            database = deserialize_database(database_path)
        elif isinstance(database, str):
            database_dir = "NicheRank/algo_src/database"
            database_path = os.path.join(database_dir, database)
            database = deserialize_database(database_path)

        self.database_artist_stats = database["artist_stats"]
        self.database_song_stats = database["song_stats"]
        self.users_dir = "NicheRank/algo_src/example_user_history"

    def generate_user_history(self, size, pop_level="med", name=None, gen_type="greedy") -> str:
        """
            Creates a user and saved them in example_user_history

            returns a string of that users name
        """

        song_history: List[md.Song] = []
        if gen_type == "greedy":
            song_history = self.greedy_generate_history(size=size, pop_level=pop_level)
        elif gen_type == "heap":
            song_history = self.heap_generate_history(size=size, pop_level=pop_level)

        save_name = name if name != None else f"user_{pop_level}_{size}_{gen_type}"
        save_name = save_name + ".json" if ".json" not in save_name else save_name

        # save this history like its a spotify response        
        spotify_response = create_spotify_response(song_history)
        save_path = os.path.join(self.users_dir, save_name)
        with open(save_path, "w") as f:
            json.dump(spotify_response, f)

        return save_name

    def get_user_songs(self, name) -> List[md.Song]:
        # selects a user from example user history
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
        for user in os.listdir(self.users_dir):
            os.remove(os.path.join(self.users_dir, user))


    def heap_generate_history(self, size:int, pop_level="med"):
        """
            Each song has artists it is made by 
        """
        
        pass

    def greedy_generate_history(self, size:int = 10000, pop_level="med"):
        """
            This method uses a greedy algorithm for playlist generation
            pop_level: low, med, or high. This reflects the listening habits of the user
            size: number of songs in playlist
        """
        unknown_song_add = 0.05 # add a random unknown song to list

        spontiniety = random.uniform(0.4, 1)  # how likely you are to listen to a bunch of songs
        max_times_listened = 20

        # grap a bunch of songs, and then choose the one of nth popularity 
        stats_list = [(uri, song_stat.popularity)for uri, song_stat in self.database_song_stats.items()]

        stats_normed:List[Tuple[str, float]] = UserManager.normalize_pop_list(stats_list)

        i = 0
        local_size = 7
        history:List[str] = [None] * size

        while (i < size):
            choices = [None] * local_size
            for j in range(local_size): 
                rand_idx = random.randint(0, len(stats_normed) - 1)
                choices[j] = stats_normed[rand_idx]
            # we now want the small, medium, or large 
            # choose the smallest, medium or large value by using a heap 
            Sorter.quicksort(choices)
            if random.uniform(0,1) < unknown_song_add:
                # add a unknown song to mix
                # TODO make this
                new_song = UserManager.gen_random_song()
            else:    
                # dont add a random song
                if pop_level == "low":
                    choose_idx = local_size - 1
                elif pop_level == "med":
                    choose_idx = local_size//2
                elif pop_level == "high":
                    choose_idx = 0
                new_song = choices[choose_idx] 
            # add this song this many times!
            times_listened = int(random.randint(0, max_times_listened) * spontiniety)
            j = 0
            while (j < times_listened and i < size):
                history[i] = new_song
                j += 1
                i += 1

        # shuffle these songs
        UserManager.shuffle(history)
        
        # map the uris back to songs
        songs = [None] * size
        for i in range(len(history)):
            (uri, _) = history[i]
            song = self.database_song_stats[uri].song
            songs[i] = song

        return songs

    def shuffle(history):
        # todo maybe inpliment shuffle algorithm
        return
    
    def normalize_pop_list(pop_list: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        mi = min(pop for _, pop in pop_list)
        ma = max(pop for _, pop in pop_list)
        return [(uri, (pop - mi)*100/(ma-mi)) for (uri, pop) in pop_list]

