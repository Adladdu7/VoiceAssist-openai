import openai
import pyttsx3
import speech_recognition as sr
from time import sleep
from console import console
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

#####################################################     CONFIG
role = "Tu es un assistant pertinant et variés pouvant répondre a une multitude de sujet."
speak = True
openai.api_key = API_KEY
##################################################### Ne touchez a rien d'autre a moins de savoir se que vous faites/ Don't did anything further if you don't know what you are doing

engine = pyttsx3.init()

####Fonction permettant la reconnaissance vocale et mise sous forme de texte 'speech_recognition'
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source :
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Erreur inconnue réessayer')

#####Fonction utilisant 'pyttsx3' afin de reciter le texte de réponse

def speak_text(bot_response):
    engine.say(bot_response)
    engine.runAndWait()

#####Affichage du menu
def print_menu():
    console.information('=======================================================')
    console.information('1.Commencer a poser des questions')
    console.information('2.Afficher la configuration actuelle')
    console.information('3.Modifier le role')
    console.information('4.Modifier la clef API')
    console.information('5.Voix')
    console.information('6.Quitter')
    console.information('=======================================================')

####Définition des choix
while True:
    print_menu()
    option = console.input('Veuillez faire un choix >>')

    if option == '1':
            while True:
            

                console.information('Dites "Genius" pour commencer a poser une question, ou "Stop" pour retourner au menu')
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    audio = recognizer.listen(source)
                    try:
                        transcription = recognizer.recognize_google(audio)
                        
                        if transcription.lower() == "genius":
                            filename = "input.wav"
                            if speak == True:
                              speak_text("Je suis a votre écoute")
                            console.informationsucc("Je suis a votre écoute")
                            with sr.Microphone() as source:
                                recognizer = sr.Recognizer()
                                source.pause_threshold = 1
                                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                                with open(filename, "wb") as f:
                                    f.write(audio.get_wav_data())

                                text = transcribe_audio_to_text(filename)
                                if text=="stop":
                                    break
                                else:
                                    console.information(f"Vous avez dit: {text}")

                            response = openai.ChatCompletion.create(                         #requete vers openai
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content":
                                role},
                                {"role": "user", "content": text},
                            ],
                            temperature=0.9,
                            max_tokens=150,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0,
                            n=1,
                            stop=["\nUser:"],
                        )
                        elif transcription.lower() == "stop":
                            break


                        bot_response = response["choices"][0]["message"]["content"]


                        
                        if speak==True:
                         speak_text(bot_response)
                         console.informationsucc(f"Réponse de l'IA: {bot_response}")
                         speak_text("Voulez vous enregistrez le résultat ? Répondez oui ou non")
                         console.information("Voulez vous enregistrez le résultat ? Répondez oui ou non")
                        else :
                         console.informationsucc(f"Réponse de l'IA: {bot_response}")
                         console.information("Voulez vous enregistrez le résultat ?")
                        with sr.Microphone() as source:
                         recognizer = sr.Recognizer()
                         audio = recognizer.listen(source)
                         transcription = recognizer.recognize_google(audio)
                         if transcription.lower() == "oui" and speak==True:
                          console.informationsucc("Vous avez dit oui, la réponses est enregistrer dans le dossier source")
                          bot_response = ""
                          file = open('response.txt','w')
                          file.write(bot_response)
                          file.close()
                         elif transcription.lower() == "oui" and speak==False:
                             file = open('response.txt','w')
                             file.write(bot_response)
                             file.close()
                             bot_response = ""
                             console.informationsucc("Vous avez dit oui, la réponses a bien été enregistré")

                         elif transcription.lower() == "" or transcription.lower() == "non":
                             bot_response = ""
                             console.error("Vous n'avez pas répondu, ou vous avez refusez la sauvegarde")
                        
                        
                                        
                    except Exception as e:
                            console.information("Attend d'être interpeller:{}".format(e))
        
    elif option == '2':
      try:
      
         console.success("Le Rôle actuel est",role)
         if speak == '':
             console.error("La voix n'est pas défini")
         elif speak =='True' or 'False':
           console.success("La voix est elle activé ?",speak)
         if openai.api_key == '':
          console.error("Aucune clé n'est défini")
         else:
          console.success("Votre clé actuel", openai.api_key)
         sleep(1.5)
   
      except speak == '' or role == '':
          console.error("Veuillez définir la clé et la voix..")
          pass

    elif option == '3':
        optionrole = input('Veuillez me donner un nouveau Rôle >>')
        role = optionrole
        console.input("Appuyer sur n'importe qu'elle touche pour continuer")
    elif option == '4':
        console.informationsucc("Votre clé actuel:{}".format(openai.api_key))
        console.information('1.Modifier la clef')
        console.information('2.Conserver la clef')
        optionkey = input('Choisissez une option >>')
        if optionkey == '1':
            inputkey = input('Saisissez votre clé API >>')
            openai.api_key = inputkey
            console.input("Appuyer sur n'importe qu'elle touche pour continuer")
        elif optionkey == '2':
            pass    
    elif option == '5':
        console.information('1.Voix Activer')
        console.information('2.Voix Desactiver')
        optionVoix = input('Choisissez une option >>')
        if optionVoix== '1':
            speak=True
        elif optionVoix=='2':
            speak=False
    elif option == '6':
          break

