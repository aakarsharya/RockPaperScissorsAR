# ML Model
from model.convnet import ConvNet

# Server + Socket Libraries
from flask import Flask
import socketio as sio # Python SocketIO Client Library

# Gameplay 
from gameplay.game import Game

# Image Processing
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image


socketio = sio.Server(cors_allowed_origins='*')
app = Flask(__name__)
app.wsgi_app = sio.WSGIApp(socketio, app.wsgi_app)

# Custom ML Model
model = ConvNet()
model.load("model/rps_model2.h5")

ROOMS = {}

########## HELPER FUNCTIONS ##########
def processImage(data):
    imageURL = data['imageURL'].replace('data:image/jpeg;base64,', '')
    imgBytes = base64.b64decode(imageURL)
    img = Image.open(BytesIO(imgBytes))
    img  = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (227, 227))
    img = np.reshape(img, (227,227,1))
    return img


def findPlayer(sid):
    for room_id, room in ROOMS.items():
        if room.containsPlayer(sid):
            return {'found': True, 'room': room_id}
    return {'found': False, 'room': None}


########## SOCKET IO FUNCTIONS ##########
def leaveRoom(sid, room):
    # Leave room
    socketio.emit(
        'room_status', 
        data={'status': "Opponent left room {}.".format(room)},
        room=room, 
        skip_sid=sid
    )
    socketio.leave_room(sid=sid, room=room)
    ROOMS[room].removePlayer(sid)
    if ROOMS[room].containsPlayer(sid):
        print('the player was not deleted properly')
    # Close empty rooms
    if ROOMS[room].numPlayers == 0:
        socketio.emit(
            'room_status',
            data={'status': "Closing empty room ({}).".format(room)},
            room=room
        )
        socketio.close_room(room=room)
        del ROOMS[room]
    

def joinRoom(sid, room):
    if ROOMS[room].numPlayers < 2:
        socketio.enter_room(room=room, sid=sid)
        ROOMS[room].addPlayer(sid)

        # Notify opponent
        socketio.emit(
            'room_status', 
            data={'status': "Opponent joined room {}.".format(room)},
            room=room,
            skip_sid=sid
        )

        # Notify client that they were able to join room
        socketio.emit(
            'room_status', 
            data={'status': "You joined room {}.".format(room)},
            to=sid
        )

        return True
    
    else:
        # Notify client that they were not able to join room
        socketio.emit(
            'room_status', 
            {'status': "Sorry, room {} is full.".format(room)},
            to=sid
        )

        return False


def printRoomOccupants():
    print('\nROOMS AND THEIR PLAYERS:')
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
    joinSuccess = joinRoom(sid, room)

    # Leave the other room
    if playerData['found'] and joinSuccess:
        leaveRoom(sid, playerData['room'])
        
    printRoomOccupants()


@socketio.on('join_room')
def onJoin(sid, data):
    if data['room'] in ROOMS.keys():

        # Check if player is in another game
        playerData = findPlayer(sid)

        # Join the new room
        joinSuccess = joinRoom(sid, data['room'])

        # Leave the other room
        if playerData['found'] and joinSuccess:
            leaveRoom(sid, playerData['room'])

    else:
        socketio.emit(
            'room_status', 
            data={'status': "Sorry, room {} does not exist.".format(data['room'])},
            to=sid
        )
    
    printRoomOccupants()


@socketio.event
def disconnect(sid):
    playerData = findPlayer(sid)
    if playerData['found']:
        print('player was found in room', playerData['room'])
        leaveRoom(sid, playerData['room'])

    print(sid, "DISCONNECTED")
    printRoomOccupants()


@socketio.on('play')
def play(sid, data):
    img = processImage(data)
    prediction = model.predict(img)
    playerData = findPlayer(sid)
    room = playerData['room']
    player = ROOMS[room].getPlayer(sid)
    player.updateHand(prediction, data['imageURL'])
    
    if ROOMS[room].isReady():
        result = ROOMS[room].play()
        socketio.emit(
            'score', 
            data=result,
            room=room
        )
        printRoomOccupants()

    else:
        socketio.emit(
            'room_status', 
            data={'status': "Waiting for opponent."},
            to=sid
        )

    printRoomOccupants()
    
if __name__ == '__main__':
    app.run()
