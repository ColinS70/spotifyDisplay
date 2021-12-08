import spotifyApi
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send, emit
import simple_websocket
from threading import Thread, Event
import time
from jinja2 import Environment, PackageLoader, select_autoescape
#Import librarys 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'theultraepicsecretkey!@#$%^&*()'
socketio = SocketIO(app)
#Init app (for calling functions) and secret key, and define its an socketio app


thread = Thread()
#Define a thread 



def handleSongChange():
    while 1 == 1:
        if(spotifyApi.getData(1) == 0):
            print('nothing playing')
            with app.app_context():
                jsonData = jsonify('',render_template('/blankTemp.html'))
                socketio.emit('update',jsonData.get_json(), namespace='/update')
            waitLoop = True
            while waitLoop:
                if(spotifyApi.getData(1) == 0):
                    print('waiting')
                    time.sleep(5)
                else:
                    waitLoop = False
        #If nothing is playing, send html that turns the screen black, then beginin waiting (check every 5 seconds if song is playing)

        else:
            if(spotifyApi.getData(2) == 0):
                songData = spotifyApi.getData(0)
                songName = songData.get('songName')
                songPop = songData.get('songPop')
                dance = songData.get('dance')
                energy = songData.get('energy')
                albName = songData.get('albName')
                relDate = songData.get('relDate')
                totalTracks = songData.get('totalTracks')
                artName = songData.get('artName')
                artPopularity = songData.get('artPopularity')
                artImgLoc = songData.get('artImgLoc')
                covImgLoc = songData.get('covImgLoc')
                with app.app_context():
                    jsonData = jsonify('',render_template('/indexTemp.html',songName=songName,songPop=songPop,dance=dance,energy=energy,albName=albName,relDate=relDate,totalTracks=totalTracks,artName=artName,artPopularity=artPopularity,artImgLoc=artImgLoc,covImgLoc=covImgLoc))
                    socketio.emit('update',jsonData.get_json(), namespace='/update')
                    pastSong = songName
                time.sleep(5)
            else:
                time.sleep(5)
        #If song is playing, render a template with the given information (Pulled from the spoitifyApi.py file)
        #The with app.app_contect() is because I need the jsonify and render template functions from the flask app, but this is running in a thread so it cant acces them without this line


@socketio.on('connect', namespace='/update')
def test_connect():
    global thread
    print('connected')
    if not thread.is_alive():
        print('Starting Thread')
        thread = socketio.start_background_task(handleSongChange)
#If a socket connection is made and no thread is alive, start a thread

@app.route('/')
def index():
    if(spotifyApi.getData(1) == 1):
        songData = spotifyApi.getData(0)
        songName = songData.get('songName')
        songPop = songData.get('songPop')
        dance = songData.get('dance')
        energy = songData.get('energy')
        albName = songData.get('albName')
        relDate = songData.get('relDate')
        totalTracks = songData.get('totalTracks')
        artName = songData.get('artName')
        artPopularity = songData.get('artPopularity')
        artImgLoc = songData.get('artImgLoc')
        covImgLoc = songData.get('covImgLoc')
        return render_template('/index.html',songName=songName,songPop=songPop,dance=dance,energy=energy,albName=albName,relDate=relDate,totalTracks=totalTracks,artName=artName,artPopularity=artPopularity,artImgLoc=artImgLoc,covImgLoc=covImgLoc)
    else:
        return render_template('/index.html',songName=':)',songPop=':)',dance=':)',energy=':)',albName=':)',relDate=':)',totalTracks=':)',artName=':)',artPopularity=':)',artImgLoc=':)',covImgLoc=':)')
        jsonData = jsonify('',render_template('/blankTemp.html'))
        socketio.emit('update',jsonData.get_json(), namespace='/update')
#When user first visits site, it renders a template if a song is playing and returns it
#If no song is playing, it renders a template with variables being ':)' then quickly blanks out screen

socketio.run(app,host="0.0.0.0")
#Run the app 