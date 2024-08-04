import argparse
import os
import sys

sys.path.append("NicheRank/algo_src")

from file_utils import DatasetToDatabase

"""
    This script is for Generating Your Own database from the Playlist Dataset. 
"""

DEFAULT_LP = 0.1

parser = argparse.ArgumentParser(description="A simple example of argparse")

parser.add_argument("--load_percent", default=DEFAULT_LP, help="Percent of 1 Million Playlists to load")
parser.add_argument("--profile", default=True, help="Display progress or not")

def handle_lp(args) -> float:
    lf = float(args.load_percent)
    if (lf > 1.0 or lf< 0.0):
        lf = DEFAULT_LP

    return lf

def main():
    args = parser.parse_args()
    lp = handle_lp(args)
    playlist_dir = "NicheRank/playlist_dataset"
    playist_path = os.path.join(playlist_dir, "spotify_million_playlist_dataset")
    extractor = DatasetToDatabase(playist_path, profile=args.profile)
    extractor.create_database(load_percent=lp, save=True)

if __name__ == "__main__":
    main()