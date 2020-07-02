from spotify_auth import getSpotipy
from main import create_playlist
import pprint
import csv
import os
import time
from common import for_each_element_in_history
from common import in_history
from common import create_key
from common import key_in_history


username = os.environ['SPOTIPY_USERNAME']
PAUSE_TIME = .05
HISTORY_DIRECTORY = 'csv/history.csv'

# Adds all recently played tracks to CVS file.
    
def add_to_cvs(track):
    if not in_history(track['id']):
        with open('played_history.csv', 'a', newline='') as csvfile:
            print('Added ' + track['name'])
            fieldnames = ['id', 'name', 'uri']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'id': track['id'], 'name': track['name'], 'uri': track['uri']})
    keys = create_key(track)
    for key in keys:
        if not key_in_history(key):
            with open(HISTORY_DIRECTORY, 'a', newline='') as csvfile:
                print('Added ' + key)
                fieldnames = ['id', 'key']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'id': track['id'], 'key': key})

def add_recents_to_played_history(sp):
    results = sp.current_user_recently_played()
    for result in results['items']:
        add_to_cvs(result['track'])
            

# Add all songs in history playlist to history csv
def add_from_history_playlist():
    tracks = []
    history_id = create_playlist(sp, 'history', '')
    results = sp.playlist_tracks(history_id)
    for result in results['items']:
        tracks.append(result['track'])
    while results['next']:
        results = sp.next(results)
        for result in results['items']:
            tracks.append(result['track'])
    for track in tracks:
        add_to_cvs(track)
        sp.user_playlist_remove_all_occurrences_of_tracks(username, history_id, [track['id']])


def clean_playlist(playlist_name):
    playlist_id = create_playlist(sp, playlist_name, '')
    results = sp.playlist_tracks(playlist_id)
    playlist_tracks = []
    for result in results['items']:
        playlist_tracks.append(result['track'])
    while results['next']:
        results = sp.next(results)
        for result in results['items']:
            playlist_tracks.append(result['track'])
        
    remove_tracks = []
    for track in playlist_tracks:
        id = track['id']
#        if in_history(id):
#            remove_tracks.append(id)
#            continue
        keys = create_key(track)
        # In case song has same name but extra artist for remix.
        should_remove = True
        for key in keys:
            if not key_in_history(key):
                should_remove = False
                break
        if should_remove:
            remove_tracks.append(id)
            
    print('Removing ' + str(len(remove_tracks)) + ' tracks from ' + playlist_name)
    if len(remove_tracks) < 100:
        if remove_tracks:
            time.sleep(PAUSE_TIME)
            sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, remove_tracks)
    else:
        for track_id in remove_tracks:
            time.sleep(PAUSE_TIME)
            sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, [track_id])


def clean_playlists():
    clean_playlist('new_music_friday_9')
    clean_playlist('the_charts')
    clean_playlist('jessi_randos')

sp = getSpotipy()

# Test
#for_each_element_in_history(add_dupicate_tracks)
#add_saved_to_played_history(sp)
#add_recents_to_played_history(sp)
#clean_playlist('new_music_friday_6')

# Main
add_recents_to_played_history(sp)
add_from_history_playlist()
clean_playlists()

