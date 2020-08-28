# RockPaperScissorsAR (online + multiplayer)
Creating the classic two-player Rock, Paper, Scissors game with AR that uses computer vision to detect each player's gestures. 

## How to Play

### Creating a Room
Visit the website at https://aakarsharya.github.io/RockPaperScissorsAR/ to begin. Make sure to allow camera access from your browser (preferably chrome).
1. Click 'Create Room' to create a game room.
2. Share the Room ID with your friend.
3. Ask your friend to enter the room id, then select 'Join Room'.

### Using the Hand Gesture Recognizer
1. Place your hand so that it appears in the red box shown in the display. Ensure that the background is plain, there is good lighting, and your entire hand fits in the display.
2. Once you have selected your gesture, select 'Play' to capture and send your image to the Computer Vision Model.
3. Once both players in the room have sent their gestures, the computer vision model will process the images and compute the winner.

## How it Works
The front-end and back-end components were built and deployed separately. They communicate with each other via Web Sockets for bidirectional communication (data flows both ways between client and server).

### Frontend
The frontend was built with Javascript, HTML, CSS. It uses the Socket.io client API to establish a websocket connection with the backend server.

### Backend
The backend was built with Flask and Python-Socketio. The Socket.io server API was used for event handling. The server uses Pillow and OpenCV for image processing. Once images from the client are processed and coverted to pixel arrays, they are passed to a custom convolutional neural network for hand gesture detection.

### Convolutional Neural Network
A custom convolutional neural network was built using tensorflow and keras, then trained on a dataset of hand images, and finally saved. The saved weights were loaded to the server, so that the server could use this network to make predictions on new images of hand gestures from clients.

### Collecting Data
"collectImages.py" leverages opencv to capture hand images and create a custom dataset. Hand gesture images from Kaggle's Rock, Paper, Scissors dataset were then added to this dataset. Finally, all images were converted to grayscale to boost performance and accuracy.

## Tech Stack
### Languages
- Python
- Javascript
- HTML
- CSS

### Libraries and Frameworks
- flask
- socket.io
- tensorflow
- keras
- openCV
- pillow
- sci-kit Learn

### Server + Deployment
- gunicorn
- eventlet
- heroku (server)
- github-pages (frontend)





