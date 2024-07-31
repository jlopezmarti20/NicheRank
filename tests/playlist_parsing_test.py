import NicheRank.algo_src.organize_dataset as dataset_parsing


def test_song_load(database):

    playlist_handler = dataset_parsing.Playlist_Songstats_Creator(database_path=database, profile=True)
    song_stats_dict = playlist_handler.load_song_stats(load_percent=0.1)

def test_artist_load(database):

    playlist_handler = dataset_parsing.Playlist_Artist_Stats_Creator(database_path=database, profile=True)
    artist_stats_dict = playlist_handler.load_artist_stats(load_percent=0.1)

def test_edge_song_load(database):
    playlist_handler = dataset_parsing.Playlist_Songstats_Creator(database_path=database, profile=True)
    song_stats_dict = playlist_handler.load_song_stats(load_percent=1)


def test_edge_artist_load(database):
    playlist_handler = dataset_parsing.Playlist_Artist_Stats_Creator(database_path=database, profile=True)
    artist_stats_dict = playlist_handler.load_artist_stats(load_percent=1)

def test():

    database_path = "/media/mattyb/UBUNTU 22_0/P3-template-main/spotify_million_playlist_dataset"
    test_song_load(database_path)

if __name__ == "__main__":
    test()