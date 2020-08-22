"""
NEED TO DELETE THIS FILE, MIGRATING ALL FRONTEND TO USE JAVASCRIPT/HTML/CSS + SOCKETIO 
FOR COMMUNICATION
"""

# ML Model
import sys
sys.path.append('..')
from training import hands
from training.train import ConvNet

# User Interface
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from undecorated import undecorated

# Camera and Image Processing
import cv2
import numpy as np
from camera import VideoCamera, generate

# Multiplayer Gameplay
from flask import Flask, Response
from flask_cors import CORS
import socketio as sio # Python SocketIO Client Library

server = Flask(__name__)
CORS(server)
socketio = sio.Client()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__, 
    server=server,
    external_stylesheets=external_stylesheets
)

model = ConvNet()
model.load()

########## Website Layout #########
app.layout = html.Div([
    html.H1(
        "Rock Paper Scissors AR",
        style={
            'text-align': 'center'
        }
    ),
    html.Br(),
    html.Div(
        children=[
            html.Img(
                id='camera',
                src='/video_feed',
                style={
                    'height': '50%',
                    'width': '50%',
                    'text-align': 'center'
                }
            ),
            html.Ul(
                id='room-updates',
                style={
                    'height': '50%',
                    'width': '20%'
                }
            )
        ],
        style={'text-align': 'inline-block'}
    ),
    html.P(id='placeholder5'),
    html.Br(),
    html.Div(
        children=[
            html.Button(
                'Predict',
                id='predict-btn'
            ),
            html.Br(),
            html.P(
                id='prediction'
            )
        ]
    ),
    html.Div(
        children=[
            dcc.Input(
                id='test-room-id',
                placeholder='test message',
                style={'display': 'inline-block'}
            ),
            html.Button(
                'Test',
                id='test-btn',
                style={'display': 'inline-block'}
            ),
            html.P(id='placeholder1')
        ],
        style={'text-align': 'center'}
    ),
    html.Br(),
    html.Div(
        children=[
            dcc.Input(
                id='input-room-id',
                placeholder='Enter Room ID',
                style={'display': 'inline-block'}
            ),
            html.Button(
                'Join Room',
                id='join-room-btn',
                style={'display': 'inline-block'}
            ),
            html.P(id='placeholder2')
        ],
        style={'text-align': 'center'}
    ),
    html.Div(
        children=[
            html.Button(
                'Create Room',
                id='create-room-btn',
                style={'display': 'inline-block'}
            ),
            html.P(
                id='display-room-id', 
                style={'display': 'inline-block'}
            ),
            html.P(id='current-room-display')
        ],
        style={'text-align': 'center'}
    )
])


######### CALLBACKS #########
@app.callback(Output('prediction', 'children'), [
    Input('predict-btn', 'n_clicks'),
])
def predict(n_clicks):
    if n_clicks != None:
        # get image from video feed, crop to find hand, and pass to model to get prediction
        img = cv2.imdecode(np.fromstring(video_feed(True)[1], dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img[100:500, 100:500]
        img = cv2.resize(img, (227, 227))
        prediction = model.predict(img)
        if prediction == "other":
            return "Could not identify hand, please try again!"
        else:
            return prediction


######### FLASK SERVER #########
@app.server.route('/video_feed')
def video_feed(capture=False):
    camera = VideoCamera()
    if capture:
        return Response(generate(camera), mimetype='multipart/x-mixed-replace; boundary=frame'), camera.getFrame()
    else:
        return Response(generate(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


######### SOCKET.IO #########
socketio.connect('http://localhost:8000/') # connect to server

# DISPLAYING STATUS UPDATES
DISPLAY_TEXT = ''
def updatePlaceholder(displayText):
    global DISPLAY_TEXT
    DISPLAY_TEXT = displayText
    print('Update Display Text:', DISPLAY_TEXT)


# TEST FUNCTION
@app.callback(Output('placeholder1', 'children'), [
    Input('test-btn', 'n_clicks'), 
    Input('test-room-id', 'value')
])
def test123(n_clicks, test_room_id):
    # global updatePlaceholder
    if type(n_clicks) is int:
        socketio.emit('test', {'code': 0, 'room': test_room_id}, callback=updatePlaceholder)
        socketio.sleep(2)
        print('placeholder 2: ', DISPLAY_TEXT)
        return DISPLAY_TEXT
    

@socketio.on('test_server_message')
def server_message(data):
    print('message from server:', str(data))


# CREATE A ROOM
CURRENT_ROOM = ''
@app.callback(Output('current-room-display', 'children'), [
    Input('create-room-btn', 'n_clicks')
])
def createRoom(n_clicks): 
    if n_clicks != None:
        socketio.emit('create_room', callback=updatePlaceholder)
        socketio.sleep(2)
        print('placeholder after: ', DISPLAY_TEXT)
        return DISPLAY_TEXT


# JOIN A ROOM
@app.callback(Output('placeholder2', 'children'), [
    Input('join-room-btn', 'n_clicks'), 
    Input('input-room-id', 'value')
])
def joinRoom(n_clicks, room_id):
    if n_clicks != None:
        socketio.emit('join_room', data={'room': room_id, 'sid': socketio.sid})


# ROOM STATUS CHANNEL
@socketio.on('room_status')
def roomStatus(data):
    print('message from server:', data['status'])


if __name__=='__main__':
    app.run_server(debug=True, port=sys.argv[1])
