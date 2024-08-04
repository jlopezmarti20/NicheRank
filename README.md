# Niche Song Ranking

## General Use Instructions

To use the database, please do the following:
1. pip -r requirements.txt
2. Download the json database files and put which one you would like in NicheRank/database
3. python3 NicheRank/manage.py runserver
4. python spotify.py
5. To use the Spotify API, leave user_login as 0. You must log in with these credentials, as Spotify for Developers only lets manually authorized users log in on unpublished projects (I would have to add your account to the list). [username: AmandaBrannon pw: Workingonit1!] change user_login to 1, 2, or 3, and it will randomly generate a fake user profile with 100000 points of data, as well as different sorting types (q=quick, m= merge).
## Dataset to Database Extraction

Due to the size of the database, we have already created it on our own. If you would like to generate your own database, do the following: 

1. Download zip from https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge#dataset 
2. Unzip file into the playlist_database folder.
3. Run the sctip playlist_parse.py with the % of playlists you want to be parsed as a float. The entire database is 1 Million playlists, which takes around 30 minutes. By default, the playlist is 0.1% parsed. 
    playlist_parse.py --load_percent 0.3 --profile True

## Contributors
Jesus Lopez 
Role: Frontend Developer

Amanda Brannon
Role: Data retrieval and Backend Developer

Matthew Boughton
Role: Backend Developer

