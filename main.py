# Nosso main.

import speech_recognition as sr


# Criar reconhecedor 

r = sr.Recognizer()

# Abrir microfone para capturar audio

with sr.Microphone() as source:
    while True:
        audio = r.listen(source) # Definir microfone como fonte

        print('Ouvindo...')
        print(r.recognize_google(audio, language='pt'))