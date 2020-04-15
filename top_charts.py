from spotify_auth import getSpotipy
from common import create_playlist
from common import in_file
import os

# Charts USA
#spotify:playlist:37i9dQZEVXbLRQDuF5jeBp

username = os.environ['SPOTIPY_USERNAME']

def get_all_charts_playlist_ids():
    all_tracks = []
    results = sp.playlist_tracks(the_charts_id, fields='items.track.id,next')
    for result in results['items']:
        all_tracks.append(result['track']['id'])
    while results['next']:
        results = sp.next(results)
        for result in results['items']:
            all_tracks.append(result['track']['id'])
    return all_tracks


def contains_track(track_id, playlist_ids):
    for curr_id in playlist_ids:
        if curr_id == track_id:
            return True
    return False

def add_playlist_tracks(playlist):
    playlist_ids = get_all_charts_playlist_ids()
    tracks = []
    results = sp.playlist_tracks(playlist[1], fields='items.track.id,total')
    for result in results['items']:
        id = result['track']['id']
        if not in_file('played_history.csv', id):
            if not contains_track(id, playlist_ids):
                tracks.append(id)
    if tracks:
        print('Added ' + str(len(tracks)) + ' tracks from ' + playlist[0])
        sp.user_playlist_add_tracks(username, the_charts_id, tracks)




sp = getSpotipy()
the_charts_id = create_playlist(sp, 'the_charts', '')


charts_playlists = [
    ['United States Top 50','37i9dQZEVXbLRQDuF5jeBp'],
    ['Argentina Top 50','37i9dQZEVXbMMy2roB9myp'],
    ['Australia Top 50','37i9dQZEVXbJPcfkRz0wJ0'],
    ['Austria Top 50','37i9dQZEVXbKNHh6NIXu36'],
    ['Belgium Top 50','37i9dQZEVXbJNSeeHswcKB'],
    ['Bolivia Top 50','37i9dQZEVXbJqfMFK4d691'],
    ['Brazil Top 50','37i9dQZEVXbMXbN3EUUhlg'],
    ['Bulgaria Top 50','37i9dQZEVXbNfM2w2mq1B8'],
    ['Canada Top 50','37i9dQZEVXbKj23U1GF4IR'],
    ['Chile Top 50','37i9dQZEVXbL0GavIqMTeb'],
    ['Colombia Top 50','37i9dQZEVXbOa2lmxNORXQ'],
    ['Costa Rica Top 50','37i9dQZEVXbMZAjGMynsQX'],
    ['Czech Republic Top 50','37i9dQZEVXbIP3c3fqVrJY'],
]

for charts_playlist in charts_playlists:
    add_playlist_tracks(charts_playlist)
