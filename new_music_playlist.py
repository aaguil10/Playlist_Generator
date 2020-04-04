from spotify_auth import getSpotipy
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, FR
import os


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
        print(e)
        last_friday = datetime.now() + relativedelta(weekday=FR(-1))
        curr_date = datetime.strptime(album_date, '%Y')
        return curr_date.date() >= last_friday.date()
    
def get_album_track_ids(album_response):
    ids = []
    for track in album_response['tracks']['items']:
        ids.append(track['id'])
    return ids

def add_recent_tracks(results):
    for result in results['items']:
        print('name: ' + result['name'] + ' release_date: ' + result['release_date'])
        if released_last_friday(result['release_date']):
            print('adding track')
            track_ids = get_album_track_ids(sp.album(result['uri']))
            sp.user_playlist_add_tracks(username, playlist_id, track_ids)

def search_through_albums(artist_id):
    results = sp.artist_albums(artist_id, limit=50)
    add_recent_tracks(results)
    while results['next']:
        results = sp.next(results)
        add_recent_tracks(results)


sp = getSpotipy()
playlist_id = create_playlist(sp, 'new_music_friday', 'finds all new music released after last friday')


search_through_albums('3TVXtAsR1Inumwj472S9r4')
