from spotify_auth import getSpotipy
from common import create_playlist
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

sp = getSpotipy()
create_saved_artist_cvs_sorted(sp)
#create_saved_artist_cvs(sp)
