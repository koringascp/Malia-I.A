from math import trunc
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import os
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import datetime
import wikipedia



# reconhecedor de fala https://www.weatherapi.com/api-explorer.aspx#forecast
sr = speech_recognition.Recognizer()

#TTS
speaker = tts.init()
speaker.setProperty('rate', 150)

#lista de tarefas array
todo_list = ['ir ao shopping', 'Limpar o quarto', 'Treinar malia']

#api scopes spotify
os.environ['SPOTIPY_CLIENT_ID'] = ''
os.environ['SPOTIPY_CLIENT_SECRET'] = ''
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com/callback'
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

#funções

#criar notas func
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

#adicionar lista de tarefas func
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

#mostrar lista de tarefas func
def show_todos():
    speaker.say("Você tem as seguintes tarefas em sua lista.")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

#olá func
def hello():
    speaker.say("Olá, em que posso ajudar?")
    speaker.runAndWait()

#sair func
def quit():
    speaker.say("Certo, até mais tarde!")
    speaker.runAndWait()
    sys.exit(0)

#tocar musica spotify func
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
                #nome_musica = results['tracks']['items'][0]['name']
                track_uri = results['tracks']['items'][0]['uri']

                speaker.say(f'Tocando {musica} no spotify')
                speaker.runAndWait()
                done = True

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


#wikipedia func

def wikipedia1():
    
    global sr
    speaker.say("Me fale o que voçê deseja pesquisar?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                sr.adjust_for_ambient_noise(mic, duration=0.2)
                audio = sr.listen(mic)

                wikipedia1 = sr.recognize_google(audio, language='pt-BR')
                wikipedia1 =  wikipedia1.lower()

                speaker.say(f'Pesquisando sobre{wikipedia1} encontrei as seguintes informações.')
                speaker.runAndWait()
                done = True
                wikipedia.set_lang( "pt" )
                info = wikipedia.summary(wikipedia1, sentences=2)

                speaker.say(info)
                speaker.runAndWait()
                
        except:        
            speaker.say("Erro, Falha na conexão tente novamente!")
            speaker.runAndWait()
            done = True

#tags + call func

mappings = {
    "saudacao": hello,
    "crir_nota": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "playspotify": playspotify,
    "wikipedia": wikipedia1,
    "despedida": exit
}

#train/intents

assistant = GenericAssistant('intents.json', intent_methods=mappings)
speaker.say("Iniciando treinamento do modelo.")
speaker.runAndWait()

assistant.train_model()
speaker.say("Salvando modelo treinado.")
speaker.runAndWait()

assistant.save_model()
speaker.say("Aguarde um pouco, Carregando modelo treinado.")
speaker.runAndWait()

assistant.load_model()
speaker.say("Pronto estou aguardando seus comandos.")
speaker.runAndWait()

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


