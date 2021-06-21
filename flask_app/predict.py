import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask_app.modules import get_track
from joblib import load
import pandas as pd
import pickle

# import numpy as np
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import TfidfVectorizer
# from re import compile as rcompile
# from sklearn.model_selection import train_test_split
# from sklearn.neighbors import NearestNeighbors

# Load model
nn = load('../model/nn.joblib')
dtm_filename = '../model/nlp_dtm.pkl'
dtm = pickle.load(open(dtm_filename, 'rb'))

# Connect to spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def recommendation(track_id):
    """Takes track_id from model, returns data on the track"""
    # Get track data
    track = spotify.track('spotify:track:' + track_id)
    track_url = 'https://open.spotify.com/track/' + track_id
    title = track['album']['name']
    artist = track['album']['artists'][0]['name']
    album_cover = track['album']['images'][1]['url']
    # Put data in dictionary
    recommended = {'url': track_url, 'artist': artist,
                         'title': title, 'album_cover': album_cover}
    return recommended

# print(recommendation('Tigerlily'))


def select_nearest_songs(id):
    df = pd.read_csv('../data/spotify_songs.csv')

    track_num = df.loc[df['track_id'] == id]
    x = track_num.index
    x = x[0]
    x = x.item()
    doc = dtm.loc[x].values
    result = nn.kneighbors([doc], n_neighbors=6)
    rec_songs = {"id" :[]};

    for i in range(5):
        song = result[1][0][ 1 +i]
        id = df.loc[song]['track_id']
        rec_songs['id'].append(id)
    return rec_songs


select_nearest_songs('00cqd6ZsSkLZqGMlQCR0Zo')

