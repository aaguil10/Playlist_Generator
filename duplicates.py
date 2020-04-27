from spotify_auth import getSpotipy
from common import getAllResults
from datetime import datetime
import csv
import json
import base64
import sys


csv.field_size_limit(sys.maxsize)

# convers track list to json and the encodes to 32 bit to avoid weird charaters
def encode_artist_tracks(track_list):
    id_name_list = []
    for trk in track_list:
        id_name_list.append({'id': trk['id'], 'name': trk['name']})
    j_dump = json.dumps(id_name_list)
    return base64.b32encode(j_dump.encode()).decode()
    
def decode_artist_tracks(ecoded_string):
    return json.loads(base64.b32decode(ecoded_string.encode()))


def get_all_album_tracks(album_id):
    results = sp.album(album_id)
    data = results['tracks']['items']
    if 'next' in results:
        while results['next']:
            results = sp.next(results)
            data.extend(results['tracks']['items'])
    return data

def get_artist_tracks_csv(artist_id):
    result = []
    curr_date = datetime.now().date()
    with open('album_tracks.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[0] == artist_id:
                    if row[1] == str(curr_date):
                        data = row[2]
                        return decode_artist_tracks(data)
            line_count += 1
    return result

# Gets all tracks form artist
def get_artist_tracks(artist_id, parent_tracks):
    tracks = get_artist_tracks_csv(artist_id)
    if len(tracks) == 0:
        results = getAllResults(sp, sp.artist_albums, artist_id)
        album_tracks = []
        curr_date = datetime.now().date()
        for result in results:
            album_tracks.extend(get_all_album_tracks(result['id']))
        data = encode_artist_tracks(album_tracks)
        with open('album_tracks.csv', 'a', newline='') as csvfile:
            fieldnames = ['artist_id', 'last_updated', 'data']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
            'artist_id': artist_id,
            'last_updated': curr_date,
            'data': data})
        tracks = get_artist_tracks_csv(artist_id)
    parent_tracks.extend(tracks)



def get_duplicates(track_id):
    track = sp.track(track_id)
    print('Searching for duplicates of ' + track['name'])
    current_track_name = track['name']
    duplicates = []
    artist_tracks = []
    for artist in track['artists']:
        get_artist_tracks(artist['id'], artist_tracks)
    print('artist_tracks ' + str(len(artist_tracks)))
    for trk in artist_tracks:
        if trk['name'] == current_track_name:
            duplicates.append(trk)
    return duplicates


def add_dupicates_to_csv(track_id):
    d = get_duplicates(track_id)
    print(d)

def deep_clean():
    with open('played_history_test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                add_dupicates_to_csv(row[0])
            line_count += 1
            if line_count > 2:
                break



sp = getSpotipy()
deep_clean()
#taco = base64.b32encode('my json dump'.encode()).decode()
#print(taco)
#pollo = base64.b32decode('NV4SA2TTN5XCAZDVNVYA====').decode()
#print(pollo)
