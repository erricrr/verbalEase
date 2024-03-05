from flask import Flask, request, render_template, send_file
import gemini_pro
from gtts import gTTS
from playsound import playsound

import atexit, os
import pyaudio
import wave
import subprocess

app = Flask(__name__)

@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/es")
def spanish(): 
    return render_template("chat.html", lang_title="Español", lang_code="es-US", 
                           intro_message="Hola, soy tu profesora de español. ¿Cómo estás?", placeholder="Escribe tu mensaje aquí...")

@app.route("/fr")
def french(): 
    return render_template("chat.html", lang_title="Français", lang_code="fr-FR", 
                        intro_message="Bonjour, je suis votre professeur de français. Comment allez-vous aujourd'hui ?", placeholder="Ecrire votre message...")

@app.route("/en")
def english(): 
    return render_template("chat.html", lang_title="English", lang_code="en-US", 
                        intro_message="Hello, I am your English teacher. How are you doing today?", placeholder="Write your message here...")

@app.route("/de")
def german(): 
    return render_template("chat.html", lang_title="Deutsch", lang_code="de-DE", 
                        intro_message="Hallo, ich bin Ihr Deutschlehrer. Wie geht es Ihnen?", placeholder="Schreibe deine Nachricht hier...")

# ADDED Vietnamese
@app.route("/vi")
def vietnamese(): 
    return render_template("chat.html", lang_title="Tiếng Việt", lang_code="vi-VN",
                        intro_message="Xin chào, tôi là giáo viên tiếng Việt của bạn. Bạn khỏe không?", placeholder="Viết tin nhắn của bạn ở đây...")

# ADDED Portuguese
@app.route("/pt")
def portuguese():
    return render_template("chat.html", lang_title="Português", lang_code="pt-BR",
                           intro_message="Olá, eu sou o seu professor de português. Como você está?", placeholder="Escreva sua mensagem aqui...")

# ADDED gtts for Vietnamese (vi-VN voice is not avaiable in macOS)
@app.route("/tts")
def tts():
    text = request.args.get("text")
    lang = request.args.get("lang")  # Get the language code from the query parameters

    if lang == "vi-VN":  # Check if the language is Vietnamese
        tts = gTTS(text, lang='vi')
        tts.save('audio.mp3')
        playsound('audio.mp3')
        return send_file('audio.mp3', mimetype='audio/mp3')
    else:
        return "Language not supported"
    

# ADDED record audio
@app.route("/record", methods=['GET'])
def record_voice():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 15

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording started. Speak into the microphone...")

    frames = []
    # for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)
    global recording
    recording = True

    for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
        if not recording:
            break
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    wav_filename = 'voice_recording.wav'

    stream.stop_stream()
    stream.close()
    p.terminate()

    wavefile = wave.open(wav_filename, 'wb')
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(p.get_sample_size(FORMAT))
    wavefile.setframerate(RATE)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    convert_to_wav(wav_filename, 'voice_recording.ogg')
    print("OGG recorded done")
    # os.remove('voice_recording.ogg')  # delete the .ogg file

    return send_file('voice_recording.ogg', mimetype="audio/ogg")

def convert_to_wav(input_file, output_file):
    print("OGG recorded converted to WAV")
    command = f'ffmpeg -i {input_file} -c:a libvorbis -q:a 4 -y {output_file}'
    subprocess.call(command, shell=True)

@app.route("/voice_recording.wav")
def audioFile():
    print("WAV played!")
    return send_file("voice_recording.wav", mimetype="audio/wav")


# Function to stop the recording
@app.route("/stop", methods=['POST'])
def stop_recording():
    global recording
    recording = False
    print("STOPPED!")
    return "Recording stopped"


# Function to delete the files when the app is closed
# def delete_files():
#     os.remove('voice_recording.ogg')
#     os.remove('voice_recording.wav')
#     print("Files deleted")
@app.route("/delete_files", methods=['POST'])
def delete_files():
    try:
        os.remove('voice_recording.ogg')
        os.remove('voice_recording.wav')
        return "Files deleted"
    except Exception as e:
        return "Error deleting files: " + str(e)

# Register the delete_files function to be called on exit
atexit.register(delete_files)


# No Change Below

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg') 
    userLang = request.referrer[-2:]
    print(userLang)
    response = gemini_pro.get_response(userText, userLang) 
    return response


if __name__ == '__main__':
    app.run()
