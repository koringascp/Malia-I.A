from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

# reconhecedor de fala
sr = speech_recognition.Recognizer()


speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['ir ao shopping', 'Limpar o quarto', 'Treinar malia']

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

                filename = sr.recognize_google(audio)
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

                item = sr.recognize_google(audio)
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
                



mappings = {
    "saudacao": hello,
    "crir_nota": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "despedida": exit
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

assistant.save_model()

assistant.load_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(mic, duration=0.2)
            audio = sr.listen(mic)

            message = sr.recognize_google(audio, language='pt-BR')
            message = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        sr = speech_recognition.Recognizer()


