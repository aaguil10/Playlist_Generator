import csv
import os

username = os.environ['SPOTIPY_USERNAME']

# Will return a list with all the results in spotipy_call
# Ex. sp.album(album_id) --> getAllResults(sp.album, album_id)
def getAllResults(sp, spotipy_call, param):
    data = []
    results = spotipy_call(param)
    data.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        data.extend(results['items'])
    return data


# Checks if playlist exist. Crates one if not.
# Returns playlist id.
def create_playlist(sp, name, description):
    results = sp.current_user_playlists(limit=50)
    for item in results['items']:
        if(item['name'] == name):
            return item['id']
    playlists = sp.user_playlist_create(username, name, description=description)
    return playlists['id']
    
# Takes in a function(track_id).
# Runs function on every element
def for_each_element_in_history(my_function):
    with open('history_test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                my_function(row[0])
            line_count += 1
    return False

# Opens cvs file and compares the first column with id.
# If it finds a match it will retrun true.
def in_file(file, id):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[0] == id:
                    return True
            line_count += 1
    return False
    
def in_history(id):
    with open('played_history.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[0] == id:
                    return True
            line_count += 1
    return False

# Returns list of the first column in cvs file
def load_data(cvs_name):
    ids = []
    with open(cvs_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                ids.append(row[0])
            line_count += 1
    return ids
    
# Returns list of the Nth column in cvs file
def load_data_at(cvs_name, nth_column):
    ids = []
    with open(cvs_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                ids.append(row[nth_column])
            line_count += 1
    return ids

def create_key(track):
    keys = []
    for artist in track['artists']:
        keys.append(track['name'] + '_' + artist['name'])
    return keys


