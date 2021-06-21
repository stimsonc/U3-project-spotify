import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
from plotly import io

# Connect to spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_track(track):
    """Returns data on track in dictionary form"""
    # Get search results. Use first result.
    results = spotify.search(q='track:' + track, type='track')
    track = results['tracks']['items'][0]
    # The features I want
    features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    # All features for the track
    track_features = spotify.audio_features(tracks=[track['id']])[0]
    # Only features I want for in a dictionary
    track_features = {feature: track_features[feature] for feature in features}
    track_features['title'] = track['name']
    track_features['artist'] = track['album']['artists'][0]['name']
    track_features['id'] = track['id']
    # Change loudness to scale
    track_features['loudness'] = (track_features['loudness']+60) / 65.376
    return track_features


def track_options(track):
    results = spotify.search(q='track:' + track, type='track')
    tracks = results['tracks']['items']
    print(tracks)

track_options('Abbey Road')



def radar_plot(track_features):
    """Produces radar plot of track's features"""
    # Build dataframe
    radar_features = track_features.copy()
    del radar_features['id']
    del radar_features['title']
    del radar_features['artist']
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


# track_features = get_track('Creep')
# radar_plot(track_features)

