from spotify_auth import getSpotipy
from common import getAllResults
from common import in_file
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, FR
import csv
import json
import base64
import sys
import spotipy
import time

PAUSE_TIME = .05

csv.field_size_limit(sys.maxsize)

# convers track list to json and the encodes to 32 bit to avoid weird charaters
def encode_artist_tracks(track_list):
    id_name_list = []
    for trk in track_list:
        id_name_list.append({'id': trk['id'], 'name': trk['name']})
#    j_dump = json.dumps(id_name_list)
#    return base64.b32encode(j_dump.encode()).decode()
    return id_name_list
    
def decode_artist_tracks(ecoded_string):
    return json.loads(base64.b32decode(ecoded_string.encode()))


def get_all_album_tracks(album_id):
    time.sleep(PAUSE_TIME)
    results = sp.album(album_id)
    data = results['tracks']['items']
    if 'next' in results:
        while results['next']:
            time.sleep(PAUSE_TIME)
            results = sp.next(results)
            data.extend(results['tracks']['items'])
    return data
    
def isRecent(album_date):
    last_friday = datetime.now() + relativedelta(weekday=FR(-1))
    a_date = datetime.strptime(album_date, '%Y-%m-%d')
    if a_date > last_friday:
        return True
    return False
    
    

def get_artist_tracks_csv(artist_id):
    result = []
    with open('album_tracks.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[0] == artist_id:
                    if isRecent(row[1]):
                        data = row[2]
                        return decode_artist_tracks(data)
            line_count += 1
    return result

# Gets all tracks form artist
def get_artist_tracks(artist_id, parent_tracks):
    tracks = get_artist_tracks_csv(artist_id)
    if len(tracks) > 0:
        print('Using cached version')
    if len(tracks) == 0:
        time.sleep(PAUSE_TIME)
        results = getAllResults(sp, sp.artist_albums, artist_id)
        album_tracks = []
        curr_date = datetime.now().date()
        for result in results:
            album_tracks.extend(get_all_album_tracks(result['id']))
        data = encode_artist_tracks(album_tracks)
#        with open('album_tracks.csv', 'a', newline='') as csvfile:
#            fieldnames = ['artist_id', 'last_updated', 'data']
#            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#            writer.writeheader()
#            writer.writerow({
#            'artist_id': artist_id,
#            'last_updated': curr_date,
#            'data': data})
#        tracks = get_artist_tracks_csv(artist_id)
        tracks = data
    parent_tracks.extend(tracks)



def get_duplicates(track_id):
    time.sleep(PAUSE_TIME)
    track = sp.track(track_id)
#    print('Searching for duplicates of ' + track['name'])
    current_track_name = track['name']
    duplicates = []
    artist_tracks = []
    for artist in track['artists']:
        get_artist_tracks(artist['id'], artist_tracks)
    for trk in artist_tracks:
        if trk['name'] == current_track_name:
            duplicates.append(trk)
    return duplicates

def add_to_cvs(track_id):
    if not in_file('played_history.csv', track_id):
        track = sp.track(track_id)
        with open('played_history.csv', 'a', newline='') as csvfile:
            print('Added ' + track['name'])
            fieldnames = ['id', 'name', 'uri']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'id': track['id'],
            'name': track['name'],
            'uri': track['uri']})

def add_dupicates_to_csv(track_id):
    d = get_duplicates(track_id)
    for t in d:
        add_to_cvs(t['id'])

def deep_clean():
    row_count = 0
    with open('played_history.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = sum(1 for row in csv_reader)

    with open('played_history.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                print(str(line_count) + '/' + str(row_count) +
                ' Searching for duplicates of ' + row[1])
                add_dupicates_to_csv(row[0])
            line_count += 1


def main():
    try:
        deep_clean()
    except spotipy.client.SpotifyException:
        print('we got it!')
        sp = getSpotipy()
        main()

sp = getSpotipy()
#main()
    
