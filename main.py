from spotify_auth import getSpotipy
from common import create_playlist
import pprint
import csv
import os

#https://github.com/plamere/spotipy
#https://spotipy.readthedocs.io/en/2.9.0/#api-reference
username = os.environ['SPOTIPY_USERNAME']




sp = getSpotipy()
#generate_aritst_cvs('jessica_music_dump', 'jessica_artist.csv')

# spotify:playlist:2a7xasL3VvF85iJ38jxgFJ
#results = sp.artist_albums('5aIqB5nVVvmFsvSdExz408', album_type='single')
#for result in results['items']:
#    print(result['release_date'] + ' album_type: ' + result['album_type'] + ' ' + result['name'])
#while results['next']:
#    print('---')
#    results = sp.next(results)
#    for result in results['items']:
#        print(result['release_date'] + ' album_type: ' + result['album_type'] + ' ' + result['name'])
 
#print('*****')
#
#results = sp.artist_albums('2a7xasL3VvF85iJ38jxgFJ', album_type='album')
#for result in results['items']:
#    print(result['release_date'] + ' album_type: ' + result['album_type'] + ' ' + result['name'])
#while results['next']:
#    print('---')
#    results = sp.next(results)
#    for result in results['items']:
#        print(result['release_date'] + ' album_type: ' + result['album_type'] + ' ' + result['name'])
#
#print('*****')
 

#create_saved_artist_cvs(sp)
#playlist_id = create_playlist(sp, 'my_test_playlist', 'Some thing')
#print(playlist_id)
