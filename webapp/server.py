# ML Model
import sys
sys.path.append('..')
from training import hands
from training.train import ConvNet

# Multiplayer Socket Libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import socketio as sio # Python SocketIO Client Library
from game import Game
from player import Player

# Image Processing
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

socketio = sio.Server()
app = Flask(__name__)
app.wsgi_app = sio.WSGIApp(socketio, app.wsgi_app)
CORS(app)

# Custom ML Model
model = ConvNet()
model.load()

ROOMS = {}

########## ROUTING FLASK API CALLS #########
@app.route('/predict', methods=['POST'])
def predict():
    print("Image Received...")
    data = request.get_json()
    imageURL = data['imageURL'].replace('data:image/jpeg;base64,' ,'')
    imgBytes = base64.b64decode(imageURL)
    img = Image.open(BytesIO(imgBytes))
    img  = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (227, 227))
    cv2.imwrite(filename="sampleImage.jpg", img=img)
    prediction = model.predict(img)
    print(prediction)
    return {"prediction": prediction}


def findPlayer(sid):
    for room_id, room in ROOMS.items():
        if sid in room.players:
            return {'found': True, 'room': room_id}
    return {'found': False, 'room': None}


def leaveRoom(sid, room):
    socketio.emit(
        'room_status', 
        data={'status': "SUCCESS - Player ({0}) has left the room ({1}).".format(sid, room)},
        room=room
    )
    socketio.leave_room(sid=sid, room=room)
    ROOMS[room].removePlayer(sid)

    # Close empty rooms
    if ROOMS[room].numPlayers == 0:
        socketio.emit(
            'room_status',
            data={'status': "INFO - Closing empty room ({}).".format(room)},
            room=room
        )
        socketio.close_room(room=room)
        del ROOMS[room]
    

def joinRoom(sid, room):
    if ROOMS[room].numPlayers < 2:
        socketio.enter_room(room=room, sid=sid)
        ROOMS[room].addPlayer(sid)
        socketio.emit(
            'room_status', 
            data={'status': "SUCCESS - Player ({0}) has joined the room ({1}).".format(sid, room)},
            room=room
        )
        # return {'success': True}
    
    else:
        socketio.emit(
            'room_status', 
            {'status': "ERROR - Player ({0}) cannot join room ({1}), room is full.".format(sid, room)},
            to=sid
        )
        # return {'success': False}


def printRoomOccupants():
    print('ROOMS AND THEIR PLAYERS:')
    print('\n----------------------------------\n')
    for room in ROOMS.values():
        print(room.to_json())
    print('\n----------------------------------\n')


@socketio.on('create_room')
def createRoom(sid):
    # Creating new game lobby
    game = Game()
    room = game.game_id
    ROOMS[room] = game

    # Check if player is in another game
    playerData = findPlayer(sid)

    # Join new room
    joinRoom(sid, room)

    # Leave the other room
    if playerData['found']:
        leaveRoom(sid, playerData['room'])
        
    printRoomOccupants()
    # return room

@socketio.on('join_room')
def onJoin(sid, data):
    if data['room'] in ROOMS.keys():

        # Check if player is in another game
        playerData = findPlayer(sid)

        # Join the new room
        joinRoom(sid, data['room'])

        # Leave the other room
        if playerData['found']:
            leaveRoom(sid, playerData['room'])

    else:
        socketio.emit(
            'room_status', 
            data={'status': "ERROR - Cannot join room: {}, room does not exist.".format(data['room'])},
            to=sid
        )
    
    printRoomOccupants()

@socketio.on('leave_room')
def onLeave(sid, data):
    if data['room'] in ROOMS.keys():
        leaveRoom(sid, data['room'])

    printRoomOccupants()


@socketio.on('test')
def testMessage(sid, data):
    # print('sid:', str(sid), 'data:', str(data))
    data['code'] += 1
    # socketio.emit('test_server_message', data=data, room=data['room'])
    return "SERVER", "callback test message was finally received"
    

if __name__ == '__main__':
    # socketio.run(app, port=8000)
    app.run(debug=True, port=8000)
