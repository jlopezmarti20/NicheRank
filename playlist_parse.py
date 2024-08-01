import argparse
import os

from NicheRank.algo_src.file_management import Dataset_Extractor


"""
    This script is for Generating Your Own database size if you would like to.
"""



parser = argparse.ArgumentParser(description="A simple example of argparse")

parser.add_argument("--load_percent", default=0.1 help="Percent of 1 Million Playlists to load")
parser.add_argument("--profile", default=True, help="Display progress or not")

def main():
    args = parser.parse_args()
    lp = args.load_percent
    path = os.path.join("playlist_database", "spotify_million_playlist_dataset")
    extractor = Dataset_Extractor(path, profile=args.profile)
    extractor.load_artist_stats(load_percent=lp, save=True)
    extractor.load_song_stats(load_percent=lp, save=True)

if __name__ == "__main__":

    main()
