"""Spotify dashboard with Flask."""
from flask import Flask, request, render_template, url_for, redirect
from flask_app.modules import get_track, radar_plot


APP = Flask(__name__)


@APP.route('/index', methods=['GET', 'POST'])
def index():
    """Asks user to input track to analyze"""
    if request.method == 'POST':
        track = request.form['track']
        track_features = get_track(track)
        fig, html = radar_plot(track_features)
        return html, render_template('visualize.html', track_features=track_features)
    return render_template('index.html')


@APP.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Asks user to input track to analyze"""
    if request.method == 'POST':
        track = request.form['track']
        # Get model prediction for track
        # model = ...
        pred = 'Happy Birthday!'
        return render_template('prediction.html', track=track, pred=pred)
    return render_template('recommend.html')


@APP.route('/')
def landing():
    return redirect(url_for('index'))


if __name__ == '__main__':
    APP.run()
