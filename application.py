import os
import collections
import datetime

from flask import Flask, render_template, flash, request, abort
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

@app.route('/channels/<string:channelname>')
def channels_show(channelname):
    if channelname not in channels:
        abort(404)

    return render_template('channel.html', channelname=channelname, messages=channels[channelname])

@socketio.on('submit message')
def submit_message(data):
    text = data['message']
    sender = data['username']
    timestamp = datetime.datetime.now()

    message = {'text': text, 'sender': sender, 'timestamp': timestamp}
    json = {'text': text, 'sender': sender, 'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')}

    channels[data['channelname']].append(message)
    emit('announce message', json, broadcast=True)
