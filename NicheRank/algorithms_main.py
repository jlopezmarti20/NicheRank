from NicheRank.algo_src.taste_global import Global_Taste
from NicheRank.algo_src.taste_user import User_Taste 
import algo_src.music_dataclass as md
from NicheRank.algo_src.popularity import Niche_Metrics

from typing import List, Tuple, Dict


import algo_src.json_parsing as parsing


"""
    This is an example that shows how the general workflow should look like for using the Modules Created

"""


def main():

    spotify_history_json = "location of retrieved user spotify song history as json"
    global_playlist_path = "location of json file with all of this"

    song_history:List[md.Song] = parsing.parse_spotify_history_json(spotify_history_json)
    user_taste = User_Taste()
    user_taste.process_user_history(song_history)

    global_taste = Global_Taste()
    global_taste.process_playlists(global_playlist_path)

    rater = Niche_Metrics(user_taste, global_taste)
    rater.calc_nicheness()

    nichcness = rater.get_nicheness()
    most_popular = rater.get_most_popular_songs(N=10)

    # we need to output users most popular songs and artists, AND the nicheness ratings of these

