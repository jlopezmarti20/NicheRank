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

## Problem
Our project aimed to solve the question as to whether a Spotify user is listening to popular or niche music and artists in comparison with the one-million playlist Spotify dataset.

## Motivation
Our motivation was that Spotify does not have any sort of metrics as to how popular your current listening history is. Through our web application, a user is able to sign into their Spotify account, give access permission, and then be presented with how popular their music taste is, as well as their top songs and artists.



## Contributors

Jesus Lopez 

**Role:** 

Frontend Developer

Led the frontend development using ReactJS and DJango with REST Frameworks, creating user interface, including buttons, text fields, and ensuring easy integration between the backend and frontend. 



Amanda Brannon

**Role:** 

Data retrieval and Backend Developer

Created and utilized the Spotify API for user authentication and user data extraction to be used in the comparison algorithms. Assisted with integration of the backend and frontend.


Matthew Boughton

**Role:**

Backend Developer

Created inheritance heirarcy for songs, artists, songstats and artist stats. Parsed the million playlists dataset and created an compression serialization and deserialization workflow. Created greedy user history generation and metrics for scoring users popularity score in comparison to global database. Created the quicksort and mergesort for quickly sorting the listening history by its local listens and according to the global listens, all within a inheritance based sorting structure. Controlled serialization of data into json and control flow of analysis algorithm and population scoring. 


