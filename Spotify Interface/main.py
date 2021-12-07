import handler
import spotifyApi
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send, emit
import simple_websocket
from threading import Thread, Event
import time
from jinja2 import Environment, PackageLoader, select_autoescape


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


thread = Thread()
thread_stop_event = Event()


def handleSongChange():
    songData = spotifyApi.getData(0)
    if(songData == 0):
        pastSong = ''
    else:
        songName = songData.get('songName')
        pastSong = songName

    while 1 == 1:
        songData = spotifyApi.getData(0)
        if(songData == 0):
            songName = 'none'
        else:
            songName = songData.get('songName')
        if(songName != pastSong):
            if(songName == 'none'):
                time.sleep(5)
            else:
                songName,songPop,dance,energy,albName,relDate,totalTracks,artName,artPopularity,artImgLoc,covImgLoc = handler.handle()
                with app.app_context():
                    jsonData = jsonify('',render_template('/indexTemp.html',songName=songName,songPop=songPop,dance=dance,energy=energy,albName=albName,relDate=relDate,totalTracks=totalTracks,artName=artName,artPopularity=artPopularity,artImgLoc=artImgLoc,covImgLoc=covImgLoc))
                    socketio.emit('update',jsonData.get_json(), namespace='/update')
                    pastSong = songName
        time.sleep(5)


@socketio.on('connect', namespace='/update')
def test_connect():
    global thread
    print('connected')
    if not thread.is_alive():
        print('Starting Thread')
        thread = socketio.start_background_task(handleSongChange)

@app.route('/')
def index():
    songName,songPop,dance,energy,albName,relDate,totalTracks,artName,artPopularity,artImgLoc,covImgLoc = handler.handle()
    return render_template('/index.html',songName=songName,songPop=songPop,dance=dance,energy=energy,albName=albName,relDate=relDate,totalTracks=totalTracks,artName=artName,artPopularity=artPopularity,artImgLoc=artImgLoc,covImgLoc=covImgLoc)


socketio.run(app)