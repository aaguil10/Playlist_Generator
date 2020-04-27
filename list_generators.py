from spotify_auth import getSpotipy
from common import create_playlist
from common import in_file
import csv


ARTIST_OCCURRENCES_KEY = 'ARTIST_OCCURRENCES'

# Creates a map {artist_id: {artist_obj}}
def add_to_artist_list(results, artists):
    for item in results['items']:
        track = item['track']
        for artist in track['artists']:
            key = artist['id']
            artists[key] = artist
            print("%32.32s %s" % (track['artists'][0]['name'], track['name']))
            
# Creates a map {artist_id: {artist_obj}}
def add_to_artist_list_with_count(results, artists, tracks_names):
    for item in results['items']:
        track = item['track']
        artist = track['artists'][0]['name']
        track_name_key = track['name'] + artist
        if track_name_key not in tracks_names:
            tracks_names.add(track_name_key)
            for artist in track['artists']:
                key = artist['id']
                if key in artists:
                    artists[key][ARTIST_OCCURRENCES_KEY] += 1
                else:
                    artist[ARTIST_OCCURRENCES_KEY] = 1
                    artists[key] = artist
                    print("%32.32s %s" % (artist['name'], track['name']))

# Creates cvs with all the artist in playlist
def generate_aritst_cvs(sp, playlist_name, cvs_name):
    playlist_id = create_playlist(sp, playlist_name, '')
    results = sp.playlist_tracks(playlist_id)
    artists = {}
    add_to_artist_list(results, artists)
    while results['next']:
        results = sp.next(results)
        add_to_artist_list(results, artists)
    with open(cvs_name, 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'uri']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for artist in list(artists.values()):
            writer.writerow({'id': artist['id'], 'name': artist['name'], 'uri': artist['uri']})
            
# Goes through all saved songs and adds artist to cvs file.
def create_saved_artist_cvs(sp):
    artists = dict()
    results = sp.current_user_saved_tracks()
    add_to_artist_list(results, artists)
    while results['next']:
        results = sp.next(results)
        add_to_artist_list(results, artists)

    with open('saved_artist.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'uri']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for artist in list(artists.values()):
            writer.writerow({'id': artist['id'], 'name': artist['name'], 'uri': artist['uri']})
            
    
def create_saved_artist_cvs_sorted(sp):
    artists = dict()
    tracks_names = set()
    results = sp.current_user_saved_tracks()
#    playlist_id = create_playlist(sp, 'jessica_full_library', '')
#    results = sp.playlist_tracks(playlist_id)
    add_to_artist_list_with_count(results, artists, tracks_names)
    while results['next']:
        results = sp.next(results)
        add_to_artist_list_with_count(results, artists, tracks_names)
        
    artists_list = list(artists.values())
    artists_list = sorted(artists_list, key = lambda i: i[ARTIST_OCCURRENCES_KEY],reverse = True)

        

    with open('saved_artist.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'uri', ARTIST_OCCURRENCES_KEY]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for artist in artists_list:
            writer.writerow({'id': artist['id'], 'name': artist['name'], 'uri': artist['uri'], ARTIST_OCCURRENCES_KEY: artist[ARTIST_OCCURRENCES_KEY]})
            
def get_id_from(obj):
    return obj['id']

artist_cache = {}
def add_artist_albums(artist_id, parent_albums):
    albums = []
    if artist_id in artist_cache:
        print('Got cached albums: ' + str(len(artist_cache[artist_id])))
        albums = artist_cache[artist_id]
    else:
        results = sp.artist_albums(artist_id)
        for result in results['items']:
            if result['uri'] not in parent_albums:
                albums.append(result['uri'])
        while results['next']:
            results = sp.next(results)
            for result in results['items']:
                if result['uri'] not in parent_albums:
                    albums.append(result['uri'])
        artist_cache[artist_id] = albums
    parent_albums.extend(albums)


def get_tracks_from_album_tracks_csv(album_id):
    result = []
    with open('album_tracks.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[3] == album_id:
                    result.append({'id': row[0], 'name': row[1], 'uri':row[2]})
            line_count += 1
    return result

# Gets album id returns list of track id with name
def save_album_tracks(album_id):
    tracks = get_tracks_from_album_tracks_csv(album_id)
    if len(tracks) == 0:
        album = sp.album(album_id)
        with open('album_tracks.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'name', 'uri', 'album_uri']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for trk in album['tracks']['items']:
                writer.writerow({'id': trk['id'], 'name': trk['name'], 'uri': trk['uri'], 'album_uri': album_id})
        tracks = save_album_tracks(album_id)
    return tracks

def get_duplicates(track):
    current_track_name = track['name']
    duplicates = []
    albums = []
    for artist in track['artists']:
        add_artist_albums(artist['id'], albums)
    for a in albums:
        album_tracks = save_album_tracks(a)
        for trk in album_tracks:
            if trk['name'] == current_track_name:
                duplicates.append(trk)
    return duplicates

def add_to_cvs(track):
    if not in_file('played_history.csv', track['id']):
        with open('played_history.csv', 'a', newline='') as csvfile:
            print('Added ' + track['name'])
            fieldnames = ['id', 'name', 'uri']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'id': track['id'], 'name': track['name'], 'uri': track['uri']})

def add_to_track_duplicates(track_id):
    track = sp.track(track_id)
    print('Searching for duplicates of ' + track['name'])
    duplicates = get_duplicates(track)
    for trk in duplicates:
        add_to_cvs(trk)
        

def deep_clean():
    with open('played_history.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                add_to_track_duplicates(row[0])
            line_count += 1



sp = getSpotipy()
deep_clean()

#create_saved_artist_cvs_sorted(sp)
#create_saved_artist_cvs(sp)
