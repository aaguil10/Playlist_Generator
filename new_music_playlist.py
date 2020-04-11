from spotify_auth import getSpotipy
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, FR
import os
import csv

from common import load_data


#datetime docs
#https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

username = os.environ['SPOTIPY_USERNAME']

def create_playlist(sp, name, description):
    results = sp.current_user_playlists(limit=50)
    for item in results['items']:
        if(item['name'] == name):
            return item['id']
    playlists = sp.user_playlist_create(username, name, description=description)
    return playlists['id']

def released_last_friday(album_date):
    try:
        last_friday = datetime.now() + relativedelta(weekday=FR(-1))
        curr_date = datetime.strptime(album_date, '%Y-%m-%d')
        return curr_date.date() >= last_friday.date()
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
        if is_track_by(track, artist_id):
            print('Adding track: ' + track['name'])
            ids.append(track['id'])
    return ids
    
def remove_duplicate_tracks(track_ids):
    response = sp.playlist_tracks(playlist_id, fields='items.track.id')
    for t in response['items']:
        id = t['track']['id']
        if id in track_ids:
            track_ids.remove(t['track']['id'])
            
def remove_history_tracks(track_ids):
    history_ids = load_data('played_history.csv')
    for id in history_ids:
        if id in track_ids:
            track_ids.remove(id)

def add_to_playlist(track_ids):
    remove_history_tracks(track_ids)
    remove_duplicate_tracks(track_ids)
    if track_ids:
        sp.user_playlist_add_tracks(username, playlist_id, track_ids)

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
            print('id: ' + result['id'] +
                    ' name: ' + result['name'] +
                    ' release_date: ' + result['release_date'] +
                    ' album_group: ' + result['album_group'] +
                    ' album_type: ' + result['album_type'])
            track_ids = get_album_track_ids(sp.album(result['uri']), artist_id)
            add_to_playlist(track_ids)

def search_through_albums(artist_id):
    results = sp.artist_albums(artist_id, limit=50)
    add_recent_tracks(results, artist_id)
    while results['next']:
        results = sp.next(results)
        add_recent_tracks(results, artist_id)

sp = getSpotipy()
playlist_id = create_playlist(sp, 'new_music_friday_5', 'All new music released after last friday')

ids = load_data('saved_artist.csv')
for id in ids:
    search_through_albums(id)


