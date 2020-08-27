import './index.css';
import io from 'socket.io-client';

// Connecting to multiplayer server

// LOCAL TESTING
// var socket = io("http://127.0.0.1:8000/");

// REMOTE SERVER
var socket = io("https://rock-paper-scissors-ar.herokuapp.com/");

// Initialize doc elements
var video = document.getElementById("videoElement");
var playButton = document.getElementById("playButton");
var createRoomButton = document.getElementById("createRoomButton");
var joinRoomInput = document.getElementById("joinRoomInput");
var joinRoomButton = document.getElementById("joinRoomButton");
var roomStatusUpdates = document.getElementById("roomStatusUpdates");
var canvas = document.getElementById("videoCanvas");
var ctx = canvas.getContext('2d');
var selfImageCanvas = document.getElementById('handImageSelf');
var opponentImageCanvas = document.getElementById('handImageOpponent');
var selfImgCtx = selfImageCanvas.getContext('2d');
selfImgCtx.font = "240px Arial";
var opponentImgCtx = opponentImageCanvas.getContext('2d');
opponentImgCtx.font = "240px Arial";
var selfImg = new Image();
var oppImg = new Image();


// SOCKET IO CHANNELS
socket.on('connect', function() {
    console.log('Successfully connected to server! SID:', socket.id);
});

socket.on('room_status', (response) => {
    console.log(response);
    updateRoomStatus(response['status'])
})

socket.on('score', (response) => {
    var result = response[socket.id]['result'];
    updateScore(result);
    drawRoundResults(response);
})


if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function (stream) {
        video.srcObject = stream;
      })
      .catch(function (error) {
        console.log("Something went wrong!");
      });
}


function updateScore(result) {
    var score = Number(document.getElementById(result).innerHTML);
    document.getElementById(result).innerHTML = ++score;

    if (result === "win") {
        updateRoomStatus("You won!")
    } else if (result === "loss") {
        updateRoomStatus("You lost.")
    } else {
        updateRoomStatus("Tie!")
    }
}


// DISPLAY ROOM STATUS UPDATES 
function updateRoomStatus(text) {
    let li = document.createElement("li");
    li.textContent = text;
    roomStatusUpdates.appendChild(li);
}


video.onplay = function() {
    setTimeout(drawImg , 300);
};


function drawImg(){
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Rectangle: (X, Y, Width, Height);
    ctx.rect(20,80,200,200);
    ctx.lineWidth = "6";
    ctx.strokeStyle = "darkRed";    
    ctx.stroke();

    setTimeout(drawImg , 100);
}


createRoomButton.onclick = async function() {
    socket.emit('create_room');
}


joinRoomButton.onclick = async function() {
    var roomID = joinRoomInput.value.toUpperCase();
    socket.emit('join_room', {'room': roomID});
}


playButton.onclick = async function() {
    var tempCanvas = document.getElementById('tempCanvas');
    var temp_ctx = tempCanvas.getContext('2d');
    tempCanvas.width = 196;
    tempCanvas.height = 196;
    temp_ctx.drawImage(canvas, 23, 83, 193, 193, 0, 0, 196, 196);
    var img = tempCanvas.toDataURL("image/jpeg", 1.0);

    socket.emit('play', {'imageURL': img});
}


function drawRoundResults(result) {
    for (var k in result) {
        console.log(result[k]['hand']);
        if (k === socket.id) {
            // eslint-disable-next-line
            selfImg.onload = function() {
                selfImageCanvas.width = 170;
                selfImageCanvas.height = 170;
                selfImgCtx.drawImage(selfImg, 0, 0, 170, 170);
            }
            selfImg.src = result[k]['img'];
        }
        else {
            // eslint-disable-next-line
            oppImg.onload = function() {
                opponentImageCanvas.width = 170;
                opponentImageCanvas.height = 170;
                opponentImgCtx.drawImage(oppImg, 0, 0, 170, 170);
            }
            oppImg.src = result[k]['img'];
        }

    }
}
