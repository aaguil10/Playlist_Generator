from spotify_auth import getSpotipy
import pprint
import csv
import os

#https://github.com/plamere/spotipy
#https://spotipy.readthedocs.io/en/2.9.0/#api-reference
username = os.environ['SPOTIPY_USERNAME']


# Checks if playlist exist. Crates one if not.
# Returns playlist id.
def create_playlist(sp, name, description):
    results = sp.current_user_playlists(limit=50)
    for item in results['items']:
        if(item['name'] == name):
            return item['id']
    playlists = sp.user_playlist_create(username, name, description=description)
    return playlists['id']



def add_to_artist_list(results, artists):
    for item in results['items']:
        track = item['track']
        for artist in track['artists']:
            key = artist['id']
            artists[key] = artist
            print("%32.32s %s" % (track['artists'][0]['name'], track['name']))

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



sp = getSpotipy()


#create_saved_artist_cvs(sp)
#playlist_id = create_playlist(sp, 'my_test_playlist', 'Some thing')
#print(playlist_id)
