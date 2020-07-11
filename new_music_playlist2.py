from spotify_auth import sp
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, FR
from common import create_key
import os
import csv
import time

from common import sp
from common import PAUSE_TIME
from common import load_data
from common import load_data_at
from common import create_playlist
from common import remove_duplicates
from common import remove_history_tracks
from common import tracks_to_ids
from common import add_to_playlist


username = os.environ['SPOTIPY_USERNAME']
REMIX_INDICATORS = [' - ', 'remix', 'version']

ALEJANDRO = 'ALEJANDRO'
JESSICA = 'JESSICA'
TEST = 'TEST'
CURRENT_USER = JESSICA

playlist_title = {
    JESSICA: 'jessica_jammers_2',
    ALEJANDRO: 'new_music_friday_10',
    TEST: 'new_music_friday_TEST'
}

favorite_artists = {
    JESSICA: 'jessica_artists.csv',
    ALEJANDRO: 'saved_artist.csv',
    TEST: 'cvs_test/saved_artist.csv'
}

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

def should_add_to_list(result):
    if released_last_friday(result['release_date']):
        if result['album_group'] != 'appears_on':
            if 'US' in result['available_markets']:
                return True
    return False
    
def get_album_tracks(album_response, artist_id):
    tracks = []
    for track in album_response['tracks']['items']:
        tracks.append(track)
    return tracks

def get_recent_tracks(results, artist_id):
    if CURRENT_USER == ALEJANDRO:
        black_list = load_data('csv/black_list_artists.csv')
        if artist_id in black_list:
            return []
    artist_recent_tracks = []
    for result in results['items']:
        if should_add_to_list(result):
            time.sleep(PAUSE_TIME)
            print( 'release_date: ' + result['release_date'] +
            ' id: ' + result['id'] + ' name: ' + result['name'])
            time.sleep(PAUSE_TIME)
            tracks = get_album_tracks(sp.album(result['uri']), artist_id)
            artist_recent_tracks.extend(tracks)
            if result['release_date'] not in accepted_dates:
                accepted_dates.append(result['release_date'])
    return artist_recent_tracks

def main():
    ids = load_data(favorite_artists[CURRENT_USER])
    artist_names = load_data_at(favorite_artists[CURRENT_USER], 1)
    new_songs = []
    index = 0
    num_ids = str(len(ids))
    for artist_id in ids:
        artist_name = artist_names[index]
        index = index + 1
        print(str(index) + '/' + num_ids + ': ' + artist_name)
        try:
            time.sleep(PAUSE_TIME)
            results = sp.artist_albums(artist_id, album_type='album')
            new_songs.extend(get_recent_tracks(results, artist_id))
        except Exception as e:
            print(e)
        try:
            time.sleep(PAUSE_TIME)
            results = sp.artist_albums(artist_id, album_type='single')
            new_songs.extend(get_recent_tracks(results, artist_id))
        except Exception as e:
            print(e)
    print('New songs: ' + str(len(new_songs)))
    
    print('Removing duplicates...')
    new_songs = remove_duplicates(new_songs)
    print('New songs: ' + str(len(new_songs)))
    
    if CURRENT_USER == ALEJANDRO:
        print('Removing tracks in history...')
        new_songs = remove_history_tracks(new_songs)
        print('New songs: ' + str(len(new_songs)))
        
    main_bucket = []
    remix_bucket = []
    for track in new_songs:
        name = track['name']
        add_to_main = True
        for indicator in REMIX_INDICATORS:
            if indicator in name.lower():
                remix_bucket.append(track)
                add_to_main = False
        if add_to_main:
            main_bucket.append(track)
    print('main_bucket: ' + str(len(main_bucket)))
    print('remix_bucket: ' + str(len(remix_bucket)))
    playlist_id = create_playlist(sp, playlist_title[CURRENT_USER], 'All new music released after last friday')
    add_to_playlist(playlist_id, tracks_to_ids(main_bucket))
    add_to_playlist(playlist_id, tracks_to_ids(remix_bucket))
    

#sp = getSpotipy()
accepted_dates = []
main()
print('accepted_dates: ' + str(accepted_dates))

