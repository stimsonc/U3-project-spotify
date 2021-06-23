import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
from plotly import io
import random
from flask_app.predict import wrangle

# Connect to spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Load dataframe
# path = '../data/spotify_songs.csv'
path = '/Users/Carl/Desktop/datascience/spotify_song_suggester/data/spotify_songs.csv'
df = pd.read_csv(path)
# Wrangle data
df2 = wrangle(df)


def random_track():
    """Returns a random track id"""
    num = random.randint(0, len(df2)-1)
    track_id = df2.iloc[num]['track_id']
    return track_id


def grab_five():
    """Returns a list of 5 track IDs"""
    five_list = []
    for i in range(5):
        five_list.append(random_track())
    return five_list


def get_track(track_id):
    """Returns data on track in dictionary form"""
    track = spotify.track(track_id)
    # Audio features
    features = ['danceability', 'energy', 'loudness', 'speechiness',
                'acousticness', 'instrumentalness', 'liveness', 'valence']
    track_features = spotify.audio_features(tracks=[track['id']])[0]
    track_features = {feature: track_features[feature] for feature in features}
    # Scale loudness
    track_features['loudness'] = (track_features['loudness'] + 60) / 65.376
    # Add title, artist, id, url to dict
    track_features['title'] = track['name']
    track_features['artist'] = track['album']['artists'][0]['name']
    track_features['id'] = track['id']
    track_features['url'] = 'https://open.spotify.com/track/' + track_id
    return track_features


def radar_plot(track_features):
    """Produces radar plot of track's features"""
    # Build dataframe
    radar_features = track_features.copy()
    del radar_features['id']
    del radar_features['title']
    del radar_features['artist']
    del radar_features['url']
    theta = list(radar_features.keys())
    r = list(radar_features.values())
    radar_df = pd.DataFrame(dict(r=r, theta=theta))
    # Create plot
    # Title, redundant if included elsewhere on the site
    # title = f"{track_features['title']} by {track_features['artist']}"
    # Figure object:
    fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')
    # Figure in html as a string:
    html = io.to_html(fig, full_html=False)
    # fig.show()
    return fig, html
