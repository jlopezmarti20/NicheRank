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

"""
    Classes for 

"""

class Artist_Scorer():

    def __call__(self, artist_stat:md.Artist_Stat, metric="basic") -> None:
        if metric == "basic":
            return Artist_Scorer.basic_scoring(artist_stat)
        elif metric == "weighted":
            return Artist_Scorer.weighted_score(artist_stat)
        elif metric == "grafted":
            return Artist_Scorer.grafted_score(artist_stat)

    def basic_score(artist_stat:md.Artist_Stat):
        # Simply return which has more songs
        return artist_stat.total_listens

    def follower_weighted_score(artist_stat:md.Artist_Stat, multi=0.6):
        # artists with higher 

        return multi * artist_stat.weighted_listens + artist_stat.total_listens
    
    def time_weighted_score(artist_stat:md.Artist_Stat, multi=0.6):
        # artists with higher overall listening matter more

        pass

class Song_Scorer():

    metrics = ["basic", "weighted", "grafted"]

    def __call__(self, song_stat: md.Song_Stat, metric = "basic") -> Any:
        if metric == "basic":
            return Song_Scorer.basic_scoring(song_stat)
        elif metric == "weighted":
            return Song_Scorer.follower_weighted_score(song_stat)
        elif metric == "grafted":
            return Song_Scorer.time_weighted_score(song_stat)


    def basic_scoring(song_stat: md.Song_Stat):
        
        return song_stat.total_listens 

    def follower_weighted_score(song_stat: md.Song_Stat):
        # a higher playlist playing this give it more power
        return song_stat.weighted_listens
    
    def time_weighted_score(song_stat: md.Song_Stat, a=0.05):
        # larger songs are worth more
        duration_addition = a*song_stat.total_listens*song_stat.song.duration_s
        return song_stat.total_listens + duration_addition