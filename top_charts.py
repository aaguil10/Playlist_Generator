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
    ['Denmark Top 50','37i9dQZEVXbL3J0k32lWnN'],
    ['Dominican Top 50','37i9dQZEVXbKAbrMR8uuf7'],
    ['Ecuador Top 50','37i9dQZEVXbJlM6nvL1nD1'],
    ['El Salvador Top 50','37i9dQZEVXbLxoIml4MYkT'],
    ['Estonia Top 50','37i9dQZEVXbLesry2Qw2xS'],
    ['Finland Top 50','37i9dQZEVXbMxcczTSoGwZ'],
    ['France Top 50','37i9dQZEVXbIPWwFssbupI'],
    ['Germany Top 50','37i9dQZEVXbJiZcmkrIHGU'],
    ['Greece Top 50','37i9dQZEVXbJqdarpmTJDL'],
    ['Guatemala Top 50','37i9dQZEVXbLy5tBFyQvd4'],
    ['Honduras Top 50','37i9dQZEVXbJp9wcIM9Eo5'],
    ['Hong Kong Top 50','37i9dQZEVXbLwpL8TjsxOG'],
    ['Hungary Top 50','37i9dQZEVXbNHwMxAkvmF8'],
    ['Iceland Top 50','37i9dQZEVXbKMzVsSGQ49S'],
    ['India Top 50','37i9dQZEVXbLZ52XmnySJg'],
    ['Indonesia Top 50','37i9dQZEVXbObFQZ3JLcXt'],
    ['Ireland Top 50','37i9dQZEVXbKM896FDX8L1'],
    ['Israel Top 50','37i9dQZEVXbJ6IpvItkve3'],
    ['Italy Top 50','37i9dQZEVXbIQnj7RRhdSX'],
    ['Japan Top 50','37i9dQZEVXbKXQ4mDTEBXq'],
    ['Latvia Top 50','37i9dQZEVXbJWuzDrTxbKS'],
    ['Lithuania Top 50','37i9dQZEVXbMx56Rdq5lwc'],
    ['Luxembourg Top 50','37i9dQZEVXbKGcyg6TFGx6'],
    ['Malaysia Top 50','37i9dQZEVXbJlfUljuZExa'],
    ['Malta Top 50','37i9dQZEVXbMD2H5HJqmx9'],
    ['Mexico Top 50','37i9dQZEVXbO3qyFxbkOE1'],
    ['Netherlands Top 50','37i9dQZEVXbKCF6dqVpDkS'],
    ['New Zealand Top 50','37i9dQZEVXbM8SIrkERIYl'],
    ['Nicaragua Top 50','37i9dQZEVXbISk8kxnzfCq'],
    ['Norway Top 50','37i9dQZEVXbJvfa0Yxg7E7'],
    ['Panama Top 50','37i9dQZEVXbKypXHVwk1f0'],
    ['Paraguay Top 50','37i9dQZEVXbNOUPGj7tW6T'],
    ['Peru Top 50','37i9dQZEVXbJfdy5b0KP7W'],
    ['Philippines Top 50','37i9dQZEVXbNBz9cRCSFkY'],
    ['Poland Top 50','37i9dQZEVXbN6itCcaL3Tt'],
    ['Portugal Top 50','37i9dQZEVXbKyJS56d1pgi'],
    ['Romania Top 50','37i9dQZEVXbNZbJ6TZelCq'],
    ['Singapore Top 50','37i9dQZEVXbK4gjvS1FjPY'],
    ['Slovakia Top 50','37i9dQZEVXbKIVTPX9a2Sb'],
    ['South Africa Top 50','37i9dQZEVXbMH2jvi6jvjk'],
    ['Spain Top 50','37i9dQZEVXbNFJfN1Vw8d9'],
    ['Sweden Top 50','37i9dQZEVXbLoATJ81JYXz'],
    ['Switzerland Top 50','37i9dQZEVXbJiyhoAPEfMK'],
    ['Taiwan Top 50','37i9dQZEVXbMnZEatlMSiu'],
    ['Thailand Top 50','37i9dQZEVXbMnz8KIWsvf9'],
    ['Turkey Top 50','37i9dQZEVXbIVYVBNw9D5K'],
    ['United Kingdom Top 50','37i9dQZEVXbLnolsZ8PSNw'],
    ['Uruguay Top 50','37i9dQZEVXbMJJi3wgRbAy'],
    ['Vietnam Top 50','37i9dQZEVXbLdGSmz6xilI'],
]

for charts_playlist in charts_playlists:
    add_playlist_tracks(charts_playlist)
