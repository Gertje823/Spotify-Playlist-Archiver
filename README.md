# Spotify-Playlist-Archiver
Simple script to scrape public Spotify playlist of users and save them in a sqlite database 

## How to use  
1. Click [here](https://developer.spotify.com/console/get-playlist/) and create a Spotify api token
2. Paste the token in `spotify_playlist_archiver.py`
3. Enter the userid's of the users you want to scrape in the users.txt
4. run `spotify_playlist_archiver.py`  

# Data that will be scraped
## Playlist
- Owner
- Name
- Thumbnail
- Description
- Collaborative
- Playlist id
- Spotify url
- Total tracks

## Tracks
- Artist
- Title
- Album
- Release date
- Cover
- Duration
- Popularity
- Spotify url
- Track number
- Playlist
- Added at
- Added by

## Userprofiles
- Username
- Display Name
- Followers
- Avatar
- Spotify url
