from typing import Any
from NicheRank.algo_src.taste_user import User_Listening_Profile

"""
    Global Taste takes in the million playlists database and 
    generates a global taste ranking according to a chosen PopularityMetric scoring class.

    This is what we will compare to the individual user to get their nicheness score 

"""

class Global_Taste():

    def __init__(self) -> None:
        pass

    def process_playlists(self, playlist_path)->None:
        """
            Generate a ranking of playlists using your own popularity metric
        """
