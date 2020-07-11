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
from common import find_duplicates
from common import tracks_to_ids
from get_playlist import remove_duplicates_in_playlist
from get_playlist import get_playlist_tracks


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

def remove_tracks_from_playlist(track_ids, playlist_name):
    playlist_id = create_playlist(sp, playlist_name, '')
    print('Removing ' + str(len(track_ids)) + ' tracks from ' + playlist_name)
    if len(track_ids) < 100:
        if track_ids:
            time.sleep(PAUSE_TIME)
            sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, track_ids)
    else:
        for track_id in track_ids:
            time.sleep(PAUSE_TIME)
            sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, [track_id])


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
        keys = create_key(track)
        # In case song has same name but extra artist for remix.
        should_remove = True
        for key in keys:
            if not key_in_history(key):
                should_remove = False
                break
        if should_remove:
            remove_tracks.append(id)
    remove_tracks_from_playlist(remove_tracks, playlist_name)
    remove_duplicates_in_playlist(playlist_name)



def clean_playlists():
    clean_playlist('new_music_friday_10')
    clean_playlist('discover_weekly')
    clean_playlist('the_charts')

sp = getSpotipy()

# Test
#clean_playlist('new_music_friday_6')

# Main
add_recents_to_played_history(sp)
add_from_history_playlist()
clean_playlists()

