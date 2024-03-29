# verbalEase
Practice Speaking a Foreign Language with AI

This project leverages Flask, Bootstrap, and GeminiPro 1.0 to construct a comprehensive AI-driven language learning application, building upon the foundational work of LinguaLearn (https://github.com/KhanradCoder/LinguaLearn) by **Adam Eubanks (https://github.com/KhanradCoder)**. I would like to acknowledge Mr. Eubanks's contributions and express my gratitude for providing the foundation for VerbalEase.

**Key Enhancements**:

* **Aesthetic Refinements**: Implemented CSS modifications.
* **Language Expansion**: Incorporated Vietnamese and Brazilian Portuguese language options.
* **Record Audio**: The user's last recorded response is now saved and available for playback.
* **Audio Playback**: Integrated functionality enables users to listen to their audio or repeat the bot's last response.
  * If the user types in input / there's no recording available, then the tts voice will be called.
* **Conversation Archiving**: Introduced a feature to save conversations as a PDF document.

This application is designed for local deployment and is optimized to function within Google Chrome. While it may be possible to access the application using other browsers or operating systems, certain features and functionalities may be limited or unavailable.

## Screenshots

| Home Page | Chat Page |
| :---: | :---: |
| ![VerbalEase Home Page](verbalEase_home.png) | ![VerbalEase Chat Page](verbalEase_chat.png) |

## Usage 
* Locate the file named ```config.ini```
* Add your Gemini API token to ```config.ini```
* Run the app with ```flask run```
