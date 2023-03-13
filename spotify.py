import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Set up authentication with Spotify API
load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
cache_path = os.path.join(os.path.dirname(__file__), '.cache')

class Spotify():

    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,client_secret, scope="user-read-playback-state user-modify-playback-state", redirect_uri=redirect_uri, cache_path=cache_path))
    
    def isPlaying(self):
        # Get information about the currently playing track
        current_track = self.sp.current_playback()

        # Check if there is a track playing
        if current_track is not None and current_track['is_playing']:
            # Check if the track is from Spotify
            if current_track['currently_playing_type'] == 'track':
                return True
        else:
            return False
    
    def pauseSong(self):
        self.sp.pause_playback()
    
    def playSong(self):
        self.sp.start_playback()