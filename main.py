from spotify_auth import getSpotipy
from common import create_playlist
from common import load_data_at
from duplicates import get_duplicates
import pprint
import csv
import os
import time

#https://github.com/plamere/spotipy
#https://spotipy.readthedocs.io/en/2.9.0/#api-reference
username = os.environ['SPOTIPY_USERNAME']

PAUSE_TIME = .1

# spotify:track:1EzrEOXmMH3G43AXT1y7pA
sp = getSpotipy()
def add_dupicates_to_lib(track_id):
    dup = get_duplicates(track_id)
    ids = []
    for track in dup:
        ids.append(track['id'])
    print(ids)
    if ids:
        if len(ids) < 50:
            sp.current_user_saved_tracks_add(tracks=ids)
        else:
            for i in ids:
                time.sleep(PAUSE_TIME)
                sp.current_user_saved_tracks_add(tracks=[i])
                
    return ids


def getAllLibTracks():
    data = []
    results = sp.current_user_saved_tracks()
    data.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        data.extend(results['items'])
    return data

def getHistory():
    data = []
    with open('played_history.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                data.append(row[0])
            line_count += 1
    tracks = []
    for item in data:
        time.sleep(PAUSE_TIME)
        track = sp.track(item)
        tracks.append(track)
    return tracks

def create_key(track):
    keys = []
    for artist in track['artists']:
        keys.append(track['name'] + '_' + artist['name'])
    return keys


def get_keys_in_file(file_name):
    items = load_data_at(file_name, 1)
    keys = []
    for item in items:
        keys.append(item)
    return keys;

# Create list of keys from played history
#results = getHistory()
#print('results: ' + str(len(results)))
#for result in results:
#    finished = get_keys_in_file('csv/history.csv')
#    keys = create_key(result)
#    for key in keys:
#        if key not in finished:
#            print('saving: ' + key)
#            with open('csv/history.csv', 'a', newline='') as csvfile:
#                       fieldnames = ['track_id', 'key']
#                       writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
##                       writer.writeheader()
#                       writer.writerow({
#                       'track_id': result['id'],
#                       'key': key})


def remove_row(values):
    with open('mark_saved_tracks.csv', 'rt') as inp, open('mark_saved_tracks_edited.csv', 'wt') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            should_add = True
            for value in values:
                if row[1] == value:
                    should_add = False
                    break
            if should_add:
                writer.writerow(row)
                
                
def save_finished_ids(values):
    h = load_finished_ids()
    with open('mark_saved_tracks_finished_ids.csv', 'a', newline='') as csvfile:
        fieldnames = ['id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for id in values:
            if id not in h:
                writer.writerow({'id': id})
                
                
def load_finished_ids():
    data = []
    with open('mark_saved_tracks_finished_ids.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                data.append(row[0])
            line_count += 1
    return data
    
def loadSavedTracks():
    data = []
    with open('mark_saved_tracks.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                data.append(row)
            line_count += 1
#    tracks = []
#    for item in data:
#        time.sleep(PAUSE_TIME)
#        track = sp.track(item)
#        tracks.append(track)
    return data

#res = loadSavedTracks()
#print('results: ' + str(len(res)))
#print(res[0])

# Create playlist with unique songs
#playlist_id = create_playlist(sp, 'full_library', 'All unique songs')
#results = loadSavedTracks()
#history = []
#history_ids = load_finished_ids()
#total_tracks = str(len(results))
#curr_index = 0
#try:
#    for result in results:
##        keys = create_key(result)
#        id = result[0]
#        key = result[1]
#        history.append(key)
#        curr_index = curr_index + 1
#        print(str(curr_index) + '/' + total_tracks + ' ' + 'id:' +  id + ' key: ' + key)
#        if id not in history_ids:
#            history_ids.extend(add_dupicates_to_lib(id))
#            history.append(key)
#            history_ids.append(id)
#            sp.user_playlist_add_tracks(username, playlist_id, [id])
#except Exception as err:
#    print(err)
#
#print('removing ' + str(len(history)) + ' rows')
#save_finished_ids(history_ids)
#remove_row(history)


def get_all_charts_playlist_ids(playlist_id):
    all_tracks = []
    results = sp.playlist_tracks(playlist_id, fields='items.track.id,next')
    for result in results['items']:
        all_tracks.append(result['track']['id'])
    while results['next']:
        results = sp.next(results)
        for result in results['items']:
            all_tracks.append(result['track']['id'])
    return all_tracks

#p_id = create_playlist(sp, 'full_library', 'All new music released after last friday')
#full_lib = get_all_charts_playlist_ids(p_id)
#print(str(len(full_lib)))
#
#full_library = []
#for id in full_lib:
#    if id not in full_library:
#        full_library.append(id)
#
#print(str(len(full_library)))
#
#fl_id = create_playlist(sp, 'Full Library', 'Alejandros Entire Library')
#count = 0
#for id in full_library:
#    count = count + 1
#    if count <= 3501:
#        continue
#    time.sleep(PAUSE_TIME)
#    sp.user_playlist_add_tracks(username, fl_id, [id])
