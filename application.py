import os
import collections

from flask import Flask, render_template, flash, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


channels = collections.OrderedDict()

@app.route("/")
def index():
    return render_template('home.html')

@app.route('/channels', methods=['GET', 'POST'])
def channels_index():
    if request.method == 'POST':
        channelname = request.form.get('channelname')

        # Channel already existed
        if channelname in channels:
            flash('A channel with a same name has already existed.')

        # Create a new channel
        else:
            channels[channelname] = []

    return render_template('channels.html', channels=channels)
