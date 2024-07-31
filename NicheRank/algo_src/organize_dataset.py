import os 
from tqdm import tqdm
import time
from typing import List, Tuple, Dict
import json_parsing
import cProfile
import pstats
from io import StringIO
import json

import music_dataclass as md
from extraction import Stats_Extractor


"""
    from dataset location, returns dictionary of uid to the stat associated to it
    
"""



# behavior class
class Dataset_Manager():

    def __init__(self, database_path, profile=False) -> None:
        
        """
            playlist_path: path to the database file
            load_percent: what percent of the million databases to load (default is max)
            sorting_algorithm: which sorting algorithm to use for this ("map", "merge") are 2 
            profile: if to profile and track sorting time
        """
        self.database_path = database_path 
        self.profile = profile
        self.save_location = "NicheRank/algo_src/playlist_stats"

        # check if database path exists
        if (not os.path.exists(self.database_path)):
            raise IOError(f'File doesnt exist: {self.database_path}')
        
    def load_artist_stats(self, load_percent=0.5,json_parse="fast", save=False) -> Dict[str, md.Artist_Stat]:
        """
            creates a list of artist stats (unordered) 
        """

        if (load_percent < 0.0 or load_percent > 1.0):
            load_percent = 0.5
        else:
            load_percent = load_percent

        num_playlists = int(load_percent * 1_000_000) # how many playlists to parse out of 1M
        # first, load every artist in every playlist
        data_dir = os.path.join(self.database_path, 'data')
        endslice: int = num_playlists // 1000
        slices: List[str] = os.listdir(data_dir)
        artist_dict: Dict[str, md.Artist_Stat] = {} # artist_uri: Artist_Stat dataclass
        slice_range = tqdm(range(endslice + 1), disable= not self.profile)
        extractor = Stats_Extractor()

        for i in slice_range:
            # current slice has playlists 
            cur_slice = slices[i]
            cur_slice_path = os.path.join(data_dir, cur_slice)
            playlists: List[Tuple[int, List[md.Song]]] = json_parsing.load_slice(cur_slice_path,json_parse)
            
            for j, (followers, playlist) in enumerate(playlists):
                if i == endslice and j == num_playlists % 1000:
                    # for processing final slice
                    break
                extractor(playlist, artist_dict, stat_type="artist", followers=followers)

        if save:
            self.save_artist_stats(artist_dict, num_playlists)
        return artist_dict        
        
    def load_song_stats(self, load_percent=0.5, json_parse="fast", save=False) -> Dict[str, md.Song_Stat]:
        """
            Creates a list of song_stats (unordered)
        
        """
        if (load_percent < 0.0 or load_percent > 1.0):
            load_percent = 0.5
        else:
            load_percent = load_percent

        num_playlists = int(load_percent * 1_000_000) # how many playlists to parse out of 1M
        # first, load every artist in every playlist
        data_dir = os.path.join(self.database_path, 'data')
        endslice: int = num_playlists // 1000
        slices: List[str] = os.listdir(data_dir)
        songs_dict: Dict[str, md.Song_Stat] = {} # song_uri: song_stat dataclass
        slice_range = tqdm(range(endslice + 1), disable=not self.profile)
        extractor = Stats_Extractor()

        for i in slice_range:
            cur_slice = slices[i]
            cur_slice_path = os.path.join(data_dir, cur_slice)
            playlists: List[Tuple[int, List[md.Song]]] = json_parsing.load_slice(cur_slice_path,json_parse)

            for j, (followers, playlist) in enumerate(playlists):
                if i == endslice and j == num_playlists % 1000:
                    break

                extractor(playlist, songs_dict, stat_type="song", followers=followers)
                    
        if save:
            self.save_song_stats(songs_dict, num_playlists)
        return songs_dict
    
    def save_song_stats(self, songs_dict, num_playlists):
        save_name = f"song_stats_{num_playlists}.json"
        json_sample = json.dumps(songs_dict, cls=json_parsing.CustomJSONEncoder, indent=4)
        save_path = os.path.join(self.database_path, save_name)
        with open(save_path, "w") as f:
            json.dump(json_sample, f)

    def save_artist_stats(self, artists_dict, num_playlists):
        save_name = f"artist_stats_{num_playlists}.json"
        save_path = os.path.join(self.database_path, save_name)
        json_sample = json.dumps(artists_dict, cls=json_parsing.CustomJSONEncoder, indent=4)
        with open(save_path, "w") as f:
            json.dump(json_sample, f)


def example_main():

    # get an example of like 100 or so playlists and stats
    dataset_location = "/media/mattyb/UBUNTU 22_0/P3-template-main/spotify_million_playlist_dataset"

    manager = Dataset_Manager(dataset_location)

    artist_stats = manager.load_artist_stats(load_percent=0.05, save=True) 
    song_stats = manager.load_song_stats(load_percent=0.05, save=True)



        



if __name__ == "__main__":
    example_main()