from spotify_auth import getSpotipy
import pprint
import csv

# Adds all recently played tracks to CVS file.

def in_file(id):
    with open('played_history.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[0] == id:
                    return True
            line_count += 1
    return False
    
def add_to_cvs(track):
    with open('played_history.csv', 'a', newline='') as csvfile:
        print('Added ' + track['name'])
        fieldnames = ['id', 'name', 'uri']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id': track['id'], 'name': track['name'], 'uri': track['uri']})

def add_recents_to_played_history(sp):
    results = sp.current_user_recently_played()
    for result in results['items']:
        track = result['track']
        if not in_file(track['id']):
            add_to_cvs(track)
            
def add_saved_to_played_history(sp):
    results = sp.current_user_saved_tracks()
    for result in results['items']:
        track = result['track']
        if not in_file(track['id']):
            add_to_cvs(track)
    while results['next']:
        results = sp.next(results)
        for result in results['items']:
            track = result['track']
            if not in_file(track['id']):
                add_to_cvs(track)


sp = getSpotipy()

#add_saved_to_played_history(sp)
add_recents_to_played_history(sp)
