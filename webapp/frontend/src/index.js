// // import React from 'react';
// // import ReactDOM from 'react-dom';
import './index.css';
// // import App from './App';

var video = document.getElementById("videoElement");
var captureButton = document.getElementById("playButton");
var canvas = document.getElementById("videoCanvas");
var ctx = canvas.getContext('2d');

video.onplay = function() {
    setTimeout(drawImg , 300);
};

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
    })
    .catch(function (err0r) {
      console.log("Something went wrong!");
    });
}

function drawImg(){
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    // console.log(canvas.width, canvas.height);

    // ctx.rect(pX,pY,faceArea,faceArea);
    ctx.rect(20,80,200,200);
    ctx.lineWidth = "6";
    ctx.strokeStyle = "darkRed";    
    ctx.stroke();

    setTimeout(drawImg , 100);
}

captureButton.onclick = async function() {
    console.log("triggered!")
    var tempCanvas = document.getElementById('tempCanvas');
    var temp_ctx = tempCanvas.getContext('2d');
    tempCanvas.width = 196;
    tempCanvas.height = 196;
    temp_ctx.drawImage(canvas, 23, 83, 196, 196, 0, 0, 196, 196);
    var result = tempCanvas.toDataURL("image/jpeg", 1.0);
    console.log(result);

    const url = "http://127.0.0.1:8000/predict";
    fetch( url, {
        method: 'POST',
        body: JSON.stringify({
            'imageURL': result
        }), 
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => response.json())
    .then(data => {
      console.log(data['prediction']);
    })
    // console.log(response.json())
}
