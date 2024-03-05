let isRecording = false;
// let recognition;
let recognition = null; // Declare the recognition variable outside the function

var lastTypedInputText = '';

let mediaRecorder = null;
let audioChunks = [];

var audioContext;
var mediaStreamSource;
var recorder;


$("#textInput").keydown(function (e) {
  // console.log(e);
  if (e.key == 'Enter') {
    getBotResponse();
    recordButton.src = 'static/img/record.svg';
    recognition.stop();
    isRecording = false;
  }
});


function toggleRecording() {
  var recordButton = document.getElementById('recordButton');
  if (!isRecording) {

    fetchRecording();

    if (window.hasOwnProperty('webkitSpeechRecognition')) {
      recognition = new webkitSpeechRecognition();

      recognition.continuous = true;
      recognition.interimResults = false;

      recognition.lang = lang;
      
      recognition.start();
      recognition.onresult = function (e) {
        var transcript = e.results[0][0].transcript;
        document.getElementById('textInput').value += transcript + ' ';
        
        lastInputText = transcript; // Store the last input text

        recognition.stop();
      };

      recognition.onerror = function (e) {
        console.log('error', e);
        recognition.stop();
      };

      //keeps recording until button pressed
      recognition.onend = function (e) {
        console.log('ended', e);
        if (isRecording){
          recognition.start();
        }
      };
      
    }
    
    recordButton.src = 'static/img/stop.svg';
    isRecording = true;

  }
  else {
    recordButton.src = 'static/img/record.svg';
    recognition.stop();
    isRecording = false;
    stopRecording();    
    getBotResponse();
    
  }
};


// Fetch /record route to record the voice_recording.wav file
function fetchRecording() {
  fetch('/record')
    .then(response => response.blob())
    .then(blob => {
      const audioURL = URL.createObjectURL(blob);
      console.log("fetchRecording called")
      return audioURL
    })
    .catch(error => console.error(error));
}

function stopRecording() {
  fetch('/stop', { method: 'POST' })
    .then(response => {
      if (response.ok) {
        console.log('Recording stopped');
      } else {
        console.error('Error stopping recording');
      }
    })
    .catch(error => console.error(error));
}


function playRecording() {
  const audioElement = new Audio();
  const timestamp = new Date().getTime(); // Generate a timestamp
  audioElement.src = `/voice_recording.wav?_=${timestamp}`; // Append the timestamp as a query parameter
  audioElement.play();
  console.log("playRecording called");
}

// // REPLAY TTS VOICE OR USER VOICE (NOT WORKING)



var isTyped = false;
var keystrokeCount = 0;

document.getElementById('textInput').addEventListener('keydown', function(event) {
  keystrokeCount++;

  if (keystrokeCount > 1) {
    isTyped = true;
  }
});

document.getElementById('recordButton').addEventListener('click', function(event) {
  isTyped = false;
  keystrokeCount = 0; // Reset keystroke count to 0 when the record button is clicked
});

function repeatAudioUser() {
  if (isTyped) {
    speakText(lastInputText);
  } else {
    playRecording();
  }
}


// End or Voice Recording

function generateBotResponse(rawText) {
  return $.get("/get", { msg: rawText });
}

// Added Vietnamese text-to-specch
function speakText(text) {
  if (lang == "vi-VN") {
    // Make an API call to the server to generate the audio file using gTTS
    return $.get("/tts", { text: text, lang: "vi-VN" });
  } else {
    var speech = new SpeechSynthesisUtterance(text);
    speech.lang = lang;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(speech);
    // Handle speech cutting off
    let r = setInterval(() => {
      if (!speechSynthesis.speaking) {
        clearInterval(r);
      } else {
        speechSynthesis.pause();
        speechSynthesis.resume();
      }
    }, 14000);
  }
}



function getBotResponse() {
  var rawText = $("#textInput").val();
  var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
  $("#textInput").val("");
  $("#chatbox").append(userHtml);
  document
    .getElementById("userInput")
    .scrollIntoView({ block: "start", behavior: "smooth" 
  });

    lastInputText = rawText; // Store the last input text

  generateBotResponse(rawText).done(function (data) {
    var botHtml = '<p class="botText"><span>' + data + '</span></p>';
    $("#chatbox").append(botHtml);
    document
      .getElementById("userInput")
      .scrollIntoView({ block: "start", behavior: "smooth" 
    });
    speakText(data);
  });
}


// ADDED to repeat bot reposnse audio

function repeatAudio() {
  var lastBotResponse = $("#chatbox .botText:last-child span").text();
  speakText(lastBotResponse);
}



// Delete ogg and wav file when refreshing browser
$(document).ready(function() {
  $(window).bind('beforeunload', function() {
    $.ajax({
      url: '/delete_files',
      type: 'POST',
      success: function(response) {
        console.log('Files deleted');
      },
      error: function(error) {
        console.error('Error deleting files');
      }
    });
  });
});


