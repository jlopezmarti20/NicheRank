import NicheRank.algo_src.taste_user as ut
import NicheRank.algo_src.taste_global as gt
import NicheRank.algo_src.music_dataclass as md

"""

    THIS IS THE MOST IMPORTANT CLASS!!! 
    Takes 2 lists of either 


"""


class Niche_Metrics():

    def __init__(self, user_taste:ut.User_Taste, global_taste: gt.Global_Taste) -> None:
        self.niche_score = None
        self.user_taste = user_taste
        self.global_taste = global_taste

        self.popularity = None

    def calc_nicheness(self, user: ut.User_Taste, globe_taste: gt.Global_Taste):

        # get nicheness from these 2 users
        pass

    def get_popularity_rating(self):
        return self.popularity
    
    def get_popular_songs(N=10):
        # return N of the top popular songs

        pass

    def get_popular_artists(N=10):
        # return N of your top artists

        pass