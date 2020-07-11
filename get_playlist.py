from spotify_auth import sp
from common import create_playlist
from common import remove_history_tracks
from common import remove_history_tracks
from common import add_to_playlist
from common import tracks_equal
from common import tracks_to_ids
from common import find_duplicates
from common import PAUSE_TIME
from common import username
import os
import time

def get_playlist_tracks(playlist_id):
    all_tracks = []
    results = sp.playlist_tracks(playlist_id)
    for result in results['items']:
        all_tracks.append(result['track'])
    while results['next']:
        results = sp.next(results)
        for result in results['items']:
            all_tracks.append(result['track'])
    return all_tracks

def copy_playlist(playlist_id, new_playlist_name):
    new_playlist_id = create_playlist(sp, new_playlist_name, '')
    new_playlist_tracks = get_playlist_tracks(new_playlist_id)
    curr_playlist_tracks = get_playlist_tracks(playlist_id)
    duplicate_tracks = []
    for curr_track in curr_playlist_tracks:
        for old_tacks in new_playlist_tracks:
            if tracks_equal(curr_track, old_tacks):
                duplicate_tracks.append(curr_track)
    ids = []
    for curr in curr_playlist_tracks:
        if curr not in duplicate_tracks:
            ids.extend(tracks_to_ids([curr]))
    add_to_playlist(new_playlist_id, ids)
    
def remove_specific_occurrences(elements, playlist_name):
    playlist_id = create_playlist(sp, playlist_name, '')
    print('Removing ' + str(len(elements)) + ' duplicate tracks from ' + playlist_name)
    if len(elements) < 100:
        if elements:
            time.sleep(PAUSE_TIME)
            sp.user_playlist_remove_specific_occurrences_of_tracks(username, playlist_id, elements)
    else:
        for track_id in elements:
            time.sleep(PAUSE_TIME)
            sp.user_playlist_remove_specific_occurrences_of_tracks(username, playlist_id, [elements])

def remove_duplicates_in_playlist(playlist_name):
    playlist_id = create_playlist(sp, playlist_name, '')
    tracks = get_playlist_tracks(playlist_id)
    duplicates = find_duplicates(tracks)
    rem = []
    position = 0
    for curr in tracks:
        if curr in duplicates:
            rem.append({'uri': curr['id'], 'positions': [position]})
            duplicates.remove(curr)
        position = position + 1
    remove_specific_occurrences(rem, playlist_name)

#remove_duplicates_in_playlist('jessica_jammers_2')
#copy_playlist('spotify:playlist:37i9dQZEVXcIivLcW8uIZq', 'discover_weekly')

# Create a playlist with all of jessica's tracks
#copy_playlist('spotify:playlist:37i9dQZEVXcIivLcW8uIZq', 'jessi_full')
