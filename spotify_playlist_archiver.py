import requests, json, sqlite3

# Set your spotify token here
token = "SPOTIFY_API_TOKEN_HERE"
def createdb():
    # DB connection
    conn = sqlite3.connect('Spotify_Archive.sqlite')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS Playlists(ID INTEGER PRIMARY KEY AUTOINCREMENT, Owner, Name, Thumbnail, Description, Collaborative, Playlist_id, Spotify_url, Total_tracks)''')
    c.execute(
        '''CREATE TABLE IF NOT EXISTS Tracks(ID  INTEGER PRIMARY KEY AUTOINCREMENT, Artist, Title, Album, Release_date, Cover, Duration , Popularity, Spotify_url, Track_number, Playlist, Added_at, Added_by)''')
    c.execute(
        '''CREATE TABLE IF NOT EXISTS Userprofiles(ID  INTEGER PRIMARY KEY AUTOINCREMENT, Username, Display_name, Followers, Avatar, Spotify_url)''')

    conn.commit()
    conn.close()

def addtrack2DB(Artist, Title, Album, Release_date, Cover, Duration , Popularity, Spotify_url, Track_number, Playlist, Added_at, Added_by):
    conn = sqlite3.connect('Spotify_Archive.sqlite')
    c = conn.cursor()
    params = (Artist, Title, Album, Release_date, Cover, Duration , Popularity, Spotify_url, Track_number, Playlist, Added_at, Added_by)
    print(params)
    try:
        c.execute("INSERT INTO Tracks(Artist, Title, Album, Release_date, Cover, Duration , Popularity, Spotify_url, Track_number, Playlist, Added_at, Added_by)VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", params)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

def addplaylist2DB(Owner, Name, Thumbnail, Description, Collaborative, Playlist_id, Spotify_url, Total_tracks):
    conn = sqlite3.connect('Spotify_Archive.sqlite')
    c = conn.cursor()
    params = (Owner, Name, Thumbnail, Description, Collaborative, Playlist_id, Spotify_url, Total_tracks)
    print(params)
    try:
        c.execute(
            "INSERT INTO Playlists(Owner, Name, Thumbnail, Description, Collaborative, Playlist_id, Spotify_url, Total_tracks)VALUES (?,?,?,?,?,?,?,?)",
            params)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

def addprofile2DB(Username, Display_name, Followers, Avatar, Spotify_url):
    conn = sqlite3.connect('Spotify_Archive.sqlite')
    c = conn.cursor()
    params = (Username, Display_name, Followers, Avatar, Spotify_url)
    print(params)
    try:
        c.execute(
            "INSERT INTO Userprofiles(Username, Display_name, Followers, Avatar, Spotify_url)VALUES (?,?,?,?,?)",
            params)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

def get_playlist_data(user):
    headers = {'Accept': 'application/json', 'Content-Type':'application/json','Authorization':f'Bearer {token}'}
#   Get userprifle data and add it to DB
    url = f"https://api.spotify.com/v1/users/{user}"
    r3 = requests.get(url, headers=headers).json()
    username = r3['id']
    display_name = r3['display_name']
    followers = r3['followers']['total']
    spotify_url = r3['external_urls']['spotify']
    try:
        avatar = r3['images'][0]['url']
    except:
        avatar = ""
    addprofile2DB(username, display_name, followers, avatar, spotify_url)
    url = f"https://api.spotify.com/v1/users/{user}/playlists?offset=0&limit=50"


    r  = requests.get(url, headers=headers)
#    Loop through all all playlists of user and add playlist to DB
    for item in r.json()['items']:
        if r.json()['total'] == 0:
            continue
        print(f"Playlist: {item['name']}\n\n")
        owner = item['owner']['display_name']
        try:
            thumbnail = item['images'][0]['url']
        except IndexError:
            thumbnail = ""
        description = item['description']
        Collaborative = item['collaborative']
        Playlist_id = item['id']
        Spotify_url = item['external_urls']['spotify']
        Total_tracks = item['tracks']['total']
        playlist_name = item['name']
        addplaylist2DB(owner, playlist_name, thumbnail, description, Collaborative, Playlist_id, Spotify_url, Total_tracks)



#       Get all tracks in playlist and add it to DB
        offset = 0
        try:
            url = item['tracks']['href']
            r4 = requests.get(url, headers=headers)
            total = r4.json()['total']
        except KeyError:
            url = item['tracks']['href']
            r4 = requests.get(url, headers=headers)
            total = r4.json()['total']
        while total > offset:
            print(f"Total tracks: {total}")
            url = f"{item['tracks']['href']}?offset={offset}&limit=100&market=NL"
            offset += 100
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                       'Authorization': f'Bearer {token}'}
            r2 = requests.get(url, headers=headers)
            #print(r2.json())
    #       Loop through all tracks in playlists of user and add them to DB
            for track in r2.json()['items']:
                try:
                    title = track['track']['name']
                except TypeError:
                    print("Error no title found... Skipping track")
                    continue

                duration_ms = track['track']['duration_ms']
                popularity = track['track']['popularity']
                track_number = track['track']['track_number']
                try:
                    spotify_urls = track['track']['external_urls']['spotify']
                except KeyError:
                    spotify_urls = ''
                album = track['track']['album']['name']
                release_date = track['track']['album']['release_date']
                try:
                    cover = track['track']['album']['images'][0]['url']
                except IndexError:
                    cover = ""
                added_at = track['added_at']
                Added_by = track['added_by']['id']
                artists = []
                for artist in track['track']['artists']:
                    artists.append(artist['name'])
                artists = ' ,'.join(artists)
                addtrack2DB(artists, title, album, release_date, cover, duration_ms, popularity, spotify_urls, track_number, playlist_name, added_at, Added_by)

createdb()
with open('users.txt') as f:
    lines = f.readlines()
    for user in lines:
        user = user.replace("\n","")
        print(user)
        get_playlist_data(user)