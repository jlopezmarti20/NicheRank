# Niche Song Ranking

## General Use Instructions

To use the database, please do the following:
1. pip -r requirements.txt
2. A default database is already implemented. If you would like to change this, see Dataset to Database Extraction. To then use that database, change line 35 of spotify.py "DATABASE_USED = 'yourDatabaseNameHere'"
3. cd NicheRank
4. python3 NicheRank/manage.py runserver
5. python spotify.py
6. To use the Spotify API, leave spotify.py line 32 "user_login" as 0. You must log in with these credentials, as Spotify for Developers only lets manually authorized users log in on unpublished projects. [username: AmandaBrannon pw: Workingonit1!] (you can see what I have been listening to! If you give me your full name and email, I can allow up to 25 people access while it is in development mode). Change user_login to 1 through 7, and it will randomly generate a fake user profile with 100000 points (or more) of data, as well as use different sorting types (q=quick, m=merge). If you really want to, these can be manually changed for even more combinations for various user profiles
## Dataset to Database Extraction

Due to the size of the database, we have already created it on our own. If you would like to generate your own database, do the following: 

1. Download zip from https://drive.google.com/drive/folders/1P_A_GMWGeT8Z4Lz1Z0E65n_gdTMMibZ9?usp=sharing
2. Unzip file into the NicheRank/playlist_database folder.
3. Run the playlist_parse.py as   
    playlist_parse.py --load_percent 0.3 --profile True 
    where load_percent is % of million playlists to load and profile is if to display how much time it takes.

Keep in mind, it takes around 1.5 minutes to parse 10% of the database, so either keep the value low or give it some time.

## Contributors
Jesus Lopez 
Role: Frontend Developer

Amanda Brannon
Role: Data retrieval and Backend Developer

Matthew Boughton
Role: Backend Developer

