from typing import Any
from user_taste import User_Listening_Profile

"""
    Global Taste takes in the million playlists database and 
    generates a global taste ranking according to a chosen PopularityMetric scoring class.

    This is what we will compare to the individual user to get their nicheness score 

"""

class Global_Taste():

    def __init__(self) -> None:
        pass


    def calculate_nicheness(user: User_Listening_Profile):
        """
            EXTREMELY IMPORTANT!!! 
            Takes a users listening profile and matches it to the global popularity 
            ranking to calculate that users nicheness score. 
        """
