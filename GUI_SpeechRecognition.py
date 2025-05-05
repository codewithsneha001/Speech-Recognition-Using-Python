import PySimpleGUI as sg
import speech_recognition as sr
from gtts import gTTS
import os
import webbrowser
from pydub import AudioSegment
from deep_translator import GoogleTranslator


# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        sg.popup("Listening... Please speak into the microphone.")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            sg.popup("You said: " + text)
            return text
        except sr.UnknownValueError:
            sg.popup("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            sg.popup("Could not request results from Google Speech Recognition service; {0}".format(e))

# Function to open a website by speech
def open_website_by_speech():
    url = speech_to_text()
    if url:
        webbrowser.open(f"https://{url}")



def audio_to_text():
    print(sr.__version__)
    r = sr.Recognizer()

    file_audio = sr.AudioFile('C:/Users/Sneha Gangapuram/Desktop/SpeechRecognition/recorded.wav')

    with file_audio as source:
        audio_text = r.record(source)

    print(type(audio_text))
    try:
        recognized_text = r.recognize_google(audio_text)
        return recognized_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3" if os.name == 'nt' else "afplay output.mp3")

# Function to translate text using Google Translate API
def translate_text(text, target_lang):
    # translator = Translator()
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        translation=translator.translate(text, dest=target_lang)
        return translation
    except Exception as e:
        return f"Error: {e}"

# GUI Layout
layout = [
    [sg.Text("1.Speech to Text Converter")],
    [sg.Button("Convert Speech to Text")],
    [sg.Text("2.Open Website by Speech")],
    [sg.Button("Open Website by Speech")],
    [sg.Text("3.Recorded Audio to Text")],
    [sg.Input(key="-FILE-"), sg.FileBrowse()],
    [sg.Button("Convert Audio File To Text")],
    [sg.Text("4.Text to Speech"), sg.InputText(key="-TEXT2SPEECH-"), sg.Button("Convert Text to Speech")],
    [sg.Text("5.Google Translate"), sg.InputText(key="-TRANSLATE-"), sg.InputText(key="-TARGETLANG-", size=(5,1)), sg.Button("Translate")],
    [sg.Output(size=(50, 10))]
    # [sg.Text("", size=(40, 1), key="-OUTPUT-")]
]

window = sg.Window("Speech to Text", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "Convert Speech to Text":
        result = speech_to_text()
        if result:
            print("Recognized Text:", result)
    elif event == "Open Website by Speech":
        open_website_by_speech()
    elif event == "Convert Audio File To Text":
        result = audio_to_text()
        if result:
            print("Recognized Text from Audio:", result)
        else:
            print("error")
    elif event == "Convert Text to Speech":
        text = values["-TEXT2SPEECH-"]
        if text:
            text_to_speech(text)
    elif event == "Translate":
        text = values["-TRANSLATE-"]
        target_lang = values["-TARGETLANG-"]
        if text and target_lang:
            translation = translate_text(text, target_lang)
            # window["-OUTPUT-"].update(f"Translated Text: {translation}")
            print("Translated Text:", translation)
        else:
            # window["-OUTPUT-"].update("Please enter text and target language")
            print("Please enter text and target language")

window.close()
