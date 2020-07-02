import spotipy
import spotipy.util as util
import os

#Docs for Scope
#https://developer.spotify.com/documentation/general/guides/scopes/

username = os.environ['SPOTIPY_USERNAME']

def getSpotipy():
    scope = 'user-library-read,playlist-modify-private,playlist-modify-public,user-read-recently-played, user-library-modify'
    token = util.prompt_for_user_token(username, scope)
    if token:
        return spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
        return null
