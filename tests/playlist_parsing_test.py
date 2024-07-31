import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../NicheRank/algo_src')))

from file_management import Dataset_Extractor 


def test_song_load(database):

    playlist_handler = Dataset_Extractor(database_path=database, profile=True)
    song_stats_dict = playlist_handler.load_song_stats(load_percent=0.001, save=True)

def test_artist_load(database):

    playlist_handler = Dataset_Extractor(database_path=database, profile=True)
    artist_stats_dict = playlist_handler.load_artist_stats(load_percent=0.001, save=True)

def test_edge_song_load(database):
    playlist_handler = Dataset_Extractor(database_path=database, profile=True)
    song_stats_dict = playlist_handler.load_song_stats(load_percent=1)

def test_edge_artist_load(database):
    playlist_handler = Dataset_Extractor(database_path=database, profile=True)
    artist_stats_dict = playlist_handler.load_artist_stats(load_percent=1)

def test_multiple_loads(database):
    various_lp = [0.01, 0.1, 0.25, 0.5]
    playlist_hander = Dataset_Extractor(database_path=database, profile=True)
    for lp in various_lp:
        start = time.time()
        playlist_hander.load_artist_stats(load_percent=lp, save=True)
        end = time.time()
        print(f"artist_stats load {lp} took {end-start} seconds")
        playlist_hander.load_song_stats(load_percent=lp, save=True)
        other_end = time.time()

        print(f"song_stats load {lp} took {other_end - end} seconds")

"""
    Test results:
    artist_stats load 0.01 took 20.90773630142212 seconds
    song_stats load 0.01 took 54.84874725341797 seconds
    artist_stats load 0.1 took 163.4431471824646 seconds
    song_stats load 0.1 took 254.976469039917 seconds
    artist_stats load 0.25 took 323.228542804718 seconds
    song_stats load 0.25 took 489.025447845459 seconds
    artist_stats load 0.5 took 589.7529063224792 seconds
    song_stats load 0.5 took 802.5563163757324 seconds

"""


def test():


    database_path = "/media/mattyb/UBUNTU 22_0/P3-template-main/spotify_million_playlist_dataset"
    test_multiple_loads(database_path)

if __name__ == "__main__":
    test()