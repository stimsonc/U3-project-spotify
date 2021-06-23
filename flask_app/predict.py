import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import joblib
import pandas as pd
import pickle

# Load model
# path = '../model/nn.joblib'
path = '/Users/Carl/Desktop/datascience/spotify_song_suggester/model/nn.joblib'
nn = joblib.load(path)
# dtm_filename = '../model/nlp_dtm.pkl'
dtm_filename = '/Users/Carl/Desktop/datascience/spotify_song_suggester/model/nlp_dtm.pkl'
dtm = pickle.load(open(dtm_filename, 'rb'))

# Connect to spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Load song dataframe
# path = '../data/spotify_songs.csv'
path = '/Users/Carl/Desktop/datascience/spotify_song_suggester/data/spotify_songs.csv'
df = pd.read_csv(path)


def recommendation(track_list):
    """Takes track_id from model, returns data on the track"""
    # Get track data
    recommended = []
    for i in range(5):
        track = spotify.track('spotify:track:' + track_list[i]['id'])
        track_url = 'https://open.spotify.com/track/' + track_list[i]['id']
        title = track['name']
        artist = track['album']['artists'][0]['name']
        album_cover = track['album']['images'][1]['url']
        recommended.append({'url': track_url, 'artist': artist,
                            'title': title, 'album_cover': album_cover})
        pass
    return recommended


def select_nearest_songs(id):
    df2 = wrangle(df)
    track_num = df2.loc[df2['track_id'] == id]
    x = track_num.index
    x = x[0]
    x = x.item()
    doc = dtm.loc[x].values
    result = nn.kneighbors([doc], n_neighbors=6)
    rec_songs = []
    for i in range(5):
        song = result[1][0][1 + i]
        id = df.loc[song]['track_id']
        rec_songs.append({'id': id})
    return rec_songs


def wrangle(data):
    # drop null values
    data = data.dropna()
    # restrict to songs with lyrics in English
    data = data[data['language'] == 'en']
    # drop duplicates
    data = data.drop_duplicates(subset=['track_name', 'track_artist'],
                                keep='first')
    # Reduce features in dataset
    features = ['track_id', 'track_name', 'track_artist', 'lyrics', 'track_album_name', 'playlist_name',
                'playlist_genre']
    data = data[features]
    # reset index
    data = data.reset_index()
    return data


i = select_nearest_songs('6b9SBw4AxSJUYEetOS5Sc8')
print(recommendation(i))