
import os
import json_parsing
import music_dataclass as md

"""
    insert a spotify listening history json file and store, then output top songs, top artists etc

"""

default_recently_played = "idk" #! change this to config data!

class User_Taste():

    def __init__(self, spotify_history:str) -> None:
        # history_location: string of where spotify json file is
        self.spotify_history = spotify_history 
        self.artists_metrics = None
        self.songs_metrics = None

        pass

    def process_user_stats(self)->None:
        # TODO process and store a users favorite artists based on time listened  
        track_list = json_parsing.process_spotify_recently_played(self.recently_played)
        
        """
            Track_List:             
            [
                {
                    song_name: str,
                    artists: [artist_name],
                    song_id: string
                    duration_s: int                    
                }
            ]
        """
        song_history:list[md.Song] = json_parsing.parse_spotify_history_json(self.spotify_history)
        # updates artist_metrics and songs_metrics by going through track list
        

        pass

    def get_favorite_artists(self, n=None):
        # Return n favorite artists
        if (self.artists_metrics is None):
            return None
        
        # get all
        n = self.unique_artists_listened() if n is None else n
        
        pass

    def get_favorite_songs(self, n=None):
        # Return n Favorite songs
        if (self.songs_metrics is None):
            return None

        n = self.unique_songs_listened() if n is None else n


        pass 

    def unique_artists_listened(self)->int:
        # total artists youve listened to 
        pass

    def unique_songs_listened(self)->int:
        # total unique songs youve listened to
        pass