"""Spotify dashboard with Flask."""
from flask import Flask, request, render_template, url_for, redirect
from flask_app.modules import get_track, radar_plot, random_track, grab_five
from flask_app.predict import recommendation, select_nearest_songs

APP = Flask(__name__)


@APP.route('/index', methods=['GET', 'POST'])
def index():
    """Asks user to input track to analyze"""
    random_sample = grab_five()
    if request.method == 'POST':
        track_id = request.form['track_id']
        # Get random id if user does not input
        if not track_id:
            track_id = random_track()
        track_features = get_track(track_id)
        fig, html = radar_plot(track_features)
        return html, render_template('visualize.html', track_features=track_features)
    return render_template('index.html', random_sample=random_sample)


@APP.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Asks user to input track to get recommendations"""
    random_sample = grab_five()
    if request.method == 'POST':
        track_id = request.form['track_id']
        # Get random id if user does not input
        if not track_id:
            track_id = random_track()
        input_track = get_track(track_id)
        # Model results
        rec_songs = select_nearest_songs(track_id)
        output_tracks = recommendation(rec_songs)
        return render_template('prediction.html',
                               input_track=input_track, output_tracks=output_tracks)
    return render_template('recommend.html', random_sample=random_sample)


@APP.route('/')
def landing():
    return redirect(url_for('index'))


if __name__ == '__main__':
    APP.run()
