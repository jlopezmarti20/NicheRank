import argparse
import os

from NicheRank.algo_src.file_management import Dataset_Extractor


"""
    This script is for Generating Your Own database from the Playlist Dataset. 
"""



parser = argparse.ArgumentParser(description="A simple example of argparse")

parser.add_argument("--load_percent", default=0.1, help="Percent of 1 Million Playlists to load")
parser.add_argument("--profile", default=True, help="Display progress or not")

def main():
    args = parser.parse_args()
    lp = args.load_percent
    playlist_dir = "NicheRank/playlist_database"
    playist_path = os.path.join(playlist_dir, "spotify_million_playlist_dataset")
    extractor = Dataset_Extractor(playist_path, profile=args.profile)
    extractor.create_database(load_percent=lp, save=True)

if __name__ == "__main__":
    main()