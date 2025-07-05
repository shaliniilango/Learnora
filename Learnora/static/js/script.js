let video = document.getElementById('video');
let emotionDisplay = document.getElementById('emotionDisplay');
let helpTogglePrompt = document.getElementById('helpTogglePrompt');

let helpSpoken = false;
let pausedForConfirmation = false;

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; });

// Start polling emotion every 5s
let emotionPolling = setInterval(() => {
    if (!pausedForConfirmation) {
        captureAndSend();
    }
}, 5000);

// Capture frame and send to server
function captureAndSend() {
    let canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    canvas.toBlob(blob => {
        let formData = new FormData();
        formData.append('frame', blob);

        fetch('/api/emotion', {
            method: 'POST',
            body: formData
        }).then(res => res.json())
          .then(data => {
              processEmotion(data);
          });
    }, 'image/jpeg');
}

// Handle backend response
function processEmotion(data) {
    const emotion = data.emotion.toLowerCase();
    const confused = data.confused;

    emotionDisplay.innerText = "Current Emotion: " + emotion;

    if (confused && !helpSpoken) {
        pausedForConfirmation = true;
        helpSpoken = true;
        showHelpPrompt();
        speakText("You seem confused. Are you?");
    }
}

// Show Yes/No toggle buttons
function showHelpPrompt() {
    helpTogglePrompt.style.display = 'block';
}

// Called when user clicks Yes or No
function handleToggleResponse(userSaidYes) {
    helpTogglePrompt.style.display = 'none';

    if (userSaidYes) {
        window.location.href = "/chat";
    } else {
        pausedForConfirmation = false;
        helpSpoken = false;
    }
}

// Speak text via backend
function speakText(text) {
    fetch('/api/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(res => res.json())
    .then(data => {
        let audio = new Audio(data.audio_url);
        audio.play();
    });
}
