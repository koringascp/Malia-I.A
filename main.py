# Nosso main.

import speech_recognition as sr


# Criar reconhecedor 



# Abrir microfone para capturar audio


while True:
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source) # Definir microfone como fonte
        
        

        try: 
            print(r.recognize_google(audio, language='pt-BR', show_all=False))
        except sr.UnknownValueError:
            print("Audio não reconhecido")
        except sr.RequestError as e:
            print("Não foi possível obter resultados; {0}".format(e))
        