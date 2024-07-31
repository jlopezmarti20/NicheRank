
import NicheRank.algo_src.sorting as sorting
import NicheRank.algo_src.music_dataclass as md



def create_songs_from_uris(uris):
    return [md.Song(name="", uri=uri) for uri in uris]

def basic_merge_test(given_uris, target_uris):
    songs = create_songs_from_uris(given_uris)
    merged_songs = SongSorter.basic_merge_sort(songs)

    for song, freq in merged_songs:
        print(f"{song.uri}: freq {freq}")
    
    assert(len(merged_songs) == len(target_uris))
    
def hash_merge_test(given_uris, target_uris):
    songs = create_songs_from_uris(given_uris)
    merged_songs = SongSorter.hash_merge_sort(songs)

    for song, freq in merged_songs:
        print(f"{song.uri}: freq {freq}")
    
    assert(len(merged_songs) == len(target_uris))

def basic_merge_sort_testing():
    # test song sorting
    input_1 = ["323232", "454", "65", "10", "4"]
    expected_1 = ["4", "10", "65", "454", "323232"]
    basic_merge_test(input_1, expected_1)
    hash_merge_test(input_1, expected_1)

    # now test if they properly merge when sorting
    input_2 = ["50", "4", "5", "4", "6", "56", "1", "50"]
    expected_2 = ["1", "56", "4", "5", "6", "50"]

    basic_merge_test(input_2, expected_2)
    hash_merge_test(input_2, expected_2)


def basic_testing():
    # 
    
    pass


def all_tests():

    pass


if __name__ == "__main__":

    all_tests()