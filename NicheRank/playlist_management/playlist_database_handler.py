import os 
import music_dataclass as md

"""
    This class works as a script that goes through and converts each artist into a map of artist_id to artist dataclass  
"""

class Playlist_Database_Handler():

    def __init__(self, database_path, load_percent=0.5, sorting_algorithm="map", profile=False) -> None:
        
        """
            playlist_path: path to the database file
            load_percent: what percent of the million databases to load (default is max)
            sorting_algorithm: which sorting algorithm to use for this ("map", "merge") are 2 
            profile: if to profile and track sorting time
        """
        self.database_path = database_path 
        self.load_percent = load_percent 
        self.num_playlists = load_percent * 1_000_000
        self.sorting_algorithm = sorting_algorithm
        self.profile = profile

        self.global_song_stats = None
        self.global_artist_stats = None

        # check if database path exists
        if (not os.path.exists(self.database_path)):
            raise IOError(f'File doesnt exist: {self.database_path}')
        
    def save_artist_stats(self,save_path="NicheRank/playlist_management/playlist_stats"):
        
        # TODO maybe switch this functionality to json parsing? 
        artist_stats: list[md.Artist_Stat] = self.load_unordered_global_artist_stats()
        json_name = f"artist_stats_{self.num_playlists}_{self.sorting_algorithm}.json"
        fpath = os.path.join(save_path, json_name)
        pass

    def save_song_stats(self, save_path="NicheRank/playlist_management/playlist_stats"):
        song_stats: list[md.Song_Stat] = self.load_unordered_global_song_stats()
        json_name = f"song_stats_{self.num_playlists}_{self.sorting_algorithm}.json"

        pass
        
    def load_artist_stats(self) -> list[md.Artist_Stat]:
        """
            creates a list of artist stats (unordered) 
        """



        pass

    def load_song_stats(self) -> list[md.Song_Stat]:
        """
            Creates a list of song_stats (unordered)
        
        """

        pass


def test():

    database_path = "/media/mattyb/UBUNTU 22_0/P3-template-main/spotify_million_playlist_dataset"

    pass

if __name__ == "__main__":
    test()