from spotify_auth import getSpotipy
from main import create_playlist
import pprint
import csv
import os
from common import for_each_element_in_history


username = os.environ['SPOTIPY_USERNAME']

# Adds all recently played tracks to CVS file.

def in_file(id):
    with open('played_history.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[0] == id:
                    return True
            line_count += 1
    return False
    
def add_to_cvs(track):
    if not in_file(track['id']):
        with open('played_history.csv', 'a', newline='') as csvfile:
            print('Added ' + track['name'])
            fieldnames = ['id', 'name', 'uri']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'id': track['id'], 'name': track['name'], 'uri': track['uri']})

def add_recents_to_played_history(sp):
    results = sp.current_user_recently_played()
    for result in results['items']:
        add_to_cvs(result['track'])
            
def add_saved_to_played_history(sp):
    results = sp.current_user_saved_tracks()
    for result in results['items']:
        add_to_cvs(result['track'])
    while results['next']:
        results = sp.next(results)
        for result in results['items']:
            add_to_cvs(result['track'])

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
    remove_tracks = []
    for result in results['items']:
        track_id = result['track']['id']
        if in_file(track_id):
            remove_tracks.append(track_id)
    while results['next']:
        results = sp.next(results)
        for result in results['items']:
            track_id = result['track']['id']
            if in_file(track_id):
                remove_tracks.append(track_id)
#    for track in remove_tracks:
#        print('removing : ' + str(remove_tracks))
    print('Removing ' + str(len(remove_tracks)) + ' tracks from ' + playlist_name)
    sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, remove_tracks)


def clean_playlists():
    clean_playlist('new_music_friday_7_5')
    clean_playlist('the_charts')

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
