from math import trunc
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import os
import spotipy 
from spotipy.oauth2 import SpotifyOAuth



# reconhecedor de fala
sr = speech_recognition.Recognizer()

#TTS
speaker = tts.init()
speaker.setProperty('rate', 150)


todo_list = ['ir ao shopping', 'Limpar o quarto', 'Treinar malia']


os.environ['SPOTIPY_CLIENT_ID'] = '7daa8d1f378d481d98e1dfcd61e34cd4'
os.environ['SPOTIPY_CLIENT_SECRET'] = '675990aa8d454265abad49133b75cc92'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com/callback'

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

#funções

def create_note():
    global sr

    speaker.say("Oque você quer escrever na sua nota")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            
            with speech_recognition.Microphone() as mic:
                sr.adjust_for_ambient_noise(mic, duration=0.2)
                audio = sr.listen(mic)

                note = sr.recognize_google(audio)
                note = note.lower()

                speaker.say("Diga uma nome de arquivo")
                speaker.runAndWait()

                sr.adjust_for_ambient_noise(mic, duration=0.2)
                audio = sr.listen(mic)

                filename = sr.recognize_google(audio, language='pt-BR')
                filename = filename.lower()

            with open(f"{filename}.txt", 'w') as f:
                f.write(note)
                done = True

                speaker.say(f"Eu criei a nota {filename}")
                speaker.runAndWait()
        
        except speech_recognition.UnknownValueError:
            sr = speech_recognition.Recognizer()

            speaker.say("Eu não consegui te entender! Tente novamente!")
            speaker.runAndWait()


def add_todo():
    global sr
    speaker.say("Oque você quer adicionar?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                sr.adjust_for_ambient_noise(mic, duration=0.2)
                audio = sr.listen(mic)

                item = sr.recognize_google(audio, language='pt-BR')
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"Eu adicionei {item} a lista de tarefas")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            sr = speech_recognition.Recognizer()

            speaker.say("Eu não consegui te entender! Tente novamente!")
            speaker.runAndWait()

def show_todos():
    speaker.say("Você tem as seguintes tarefas em sua lista.")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say("Olá, em que posso ajudar?")
    speaker.runAndWait()

def quit():
    speaker.say("Certo, até mais tarde!")
    speaker.runAndWait()
    sys.exit(0)

def playspotify():
    global sp
    global sr
    speaker.say("Que música você quer ouvir?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                sr.adjust_for_ambient_noise(mic, duration=0.2)
                audio = sr.listen(mic)

                musica = sr.recognize_google(audio, language='pt-BR')
                musica = musica.lower()#.replace('tocar no spotify','').strip()

                results = sp.search(musica,1,0,"track")

                #nome_artista = results['tracks']['items'][0]['artists'][0]['name']
                nome_musica = results['tracks']['items'][0]['name']
                track_uri = results['tracks']['items'][0]['uri']

                speaker.say(f'Tocando {nome_musica} no spotify')
                speaker.runAndWait()

            try:
                sp.start_playback(uris=[track_uri])
            except:
                speaker.say("Ouve algum problema ao tentar reproduzir a música")
                speaker.say("é necessario ser premium, para que eu possa controlar seu spotify")


        except speech_recognition.UnknownValueError:
            sr = speech_recognition.Recognizer()

            speaker.say("Eu não consegui te entender! Tente novamente!")
            speaker.runAndWait()
            done = True
                


#tags + call func

mappings = {
    "saudacao": hello,
    "crir_nota": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "playspotify": playspotify,
    "despedida": exit
}

#train/intents

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

assistant.save_model()

assistant.load_model()

#main

while True:
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(mic, duration=0.2)
            audio = sr.listen(mic)

            message = sr.recognize_google(audio, language='pt-BR')
            message = message.lower()

            print(f"Reconhecido: {message}")

        assistant.request(message)
       
        
    except speech_recognition.UnknownValueError:
        sr = speech_recognition.Recognizer()


