from spotify_auth import getSpotipy
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, FR
from common import create_key
import os
import csv
import time

from common import load_data


#datetime docs
#https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

username = os.environ['SPOTIPY_USERNAME']


ALEJANDRO = 'ALEJANDRO'
JESSICA = 'JESSICA'
CURRENT_USER = ALEJANDRO
PAUSE_TIME = .05

playlist_title = {
    JESSICA: 'jessica_jammers',
    ALEJANDRO: 'new_music_friday_9'
}

favorite_artists = {
    JESSICA: 'jessica_artists.csv',
    ALEJANDRO: 'saved_artist.csv'
}

def create_playlist(sp, name, description):
    results = sp.current_user_playlists(limit=50)
    for item in results['items']:
        if(item['name'] == name):
            return item['id']
    playlists = sp.user_playlist_create(username, name, description=description)
    return playlists['id']

def released_last_friday(album_date):
    try:
        last_last_friday = datetime.now() + relativedelta(weekday=FR(-2))
        last_friday = datetime.now() + relativedelta(weekday=FR(-1))
        curr_date = datetime.strptime(album_date, '%Y-%m-%d')
        if curr_date.date() <= last_friday.date():
            return curr_date.date() > last_last_friday.date()
    except Exception as e:
        try:
            last_friday = datetime.now() + relativedelta(weekday=FR(-1))
            curr_date = datetime.strptime(album_date, '%Y')
            return curr_date.date() >= last_friday.date()
        except Exception as ex:
            print(e)
            return False
    
def is_track_by(track, artist_id):
    for artist in track['artists']:
        if artist['id'] == artist_id:
            return True
    return False
    
def get_album_track_ids(album_response, artist_id):
    ids = []
    for track in album_response['tracks']['items']:
        if ' - ' in track['name']:
            remix_bucket.append(track['id'])
            continue
        if 'Remix' in track['name']:
            remix_bucket.append(track['id'])
            continue
        if is_track_by(track, artist_id):
            print('Adding track: ' + track['name'])
            ids.append(track['id'])
    return ids
    
def remove_duplicate_tracks(track_ids):
    time.sleep(PAUSE_TIME)
    response = sp.playlist_tracks(playlist_id)
    playlist_keys = []
    new_list = []
    for t in response['items']:
        playlist_keys.extend(create_key(t['track']))
    for id in track_ids:
        time.sleep(PAUSE_TIME)
        keys = create_key(sp.track(id))
        in_playlist = False
        for key in keys:
            if key in playlist_keys:
                in_playlist = True
        if not in_playlist:
            new_list.append(id)
    return new_list
     
            
def remove_history_tracks(track_ids):
    history_ids = load_data('played_history.csv')
    for id in history_ids:
        if id in track_ids:
            track_ids.remove(id)

def add_to_playlist(track_ids):
    if CURRENT_USER == ALEJANDRO:
        remove_history_tracks(track_ids)
    track_ids = remove_duplicate_tracks(track_ids)
    if len(track_ids) < 100:
        if track_ids:
            time.sleep(PAUSE_TIME)
            sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    else:
        for track_id in track_ids:
            time.sleep(PAUSE_TIME)
            sp.user_playlist_add_tracks(username, playlist_id, [track_id])

def should_add_to_list(result):
    if released_last_friday(result['release_date']):
        if result['album_group'] != 'appears_on':
            if 'US' in result['available_markets']:
                return True
    return False
    


def add_recent_tracks(results, artist_id):
    black_list = load_data('black_list_artists.csv')
    if artist_id in black_list:
        return
    for result in results['items']:
        if should_add_to_list(result):
            time.sleep(PAUSE_TIME)
            print( 'release_date: ' + result['release_date'] +
            ' id: ' + result['id'] +
                    ' name: ' + result['name'] +
                    ' album_group: ' + result['album_group'] +
                    ' album_type: ' + result['album_type'])
            if result['release_date'] not in accepted_dates:
                accepted_dates.append(result['release_date'])
            time.sleep(PAUSE_TIME)
            track_ids = get_album_track_ids(sp.album(result['uri']), artist_id)
            add_to_playlist(track_ids)

def search_through_albums(artist_id):
    time.sleep(PAUSE_TIME)
    results = sp.artist_albums(artist_id, album_type='album')
    add_recent_tracks(results, artist_id)
    time.sleep(PAUSE_TIME)
    results = sp.artist_albums(artist_id, album_type='single')
    add_recent_tracks(results, artist_id)
    

sp = getSpotipy()
playlist_id = create_playlist(sp, playlist_title[CURRENT_USER], 'All new music released after last friday')


accepted_dates = []
remix_bucket = []
ids = load_data(favorite_artists[CURRENT_USER])
for id in ids:
    search_through_albums(id)
add_to_playlist(remix_bucket)
print('accepted_dates: ' + str(accepted_dates))

