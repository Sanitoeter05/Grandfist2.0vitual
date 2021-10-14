import datetime  # importing Lib`S
import time
import calendar
import pyjokes
import requests
import speech_recognition as sr
import pyttsx3
import wikipedia
import wolframalpha
import webbrowser
from deep_translator import GoogleTranslator
from googleapiclient.discovery import build
from tqdm import tqdm

engine = pyttsx3.init('sapi5')            # speak engine and voice Probity
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[1].id')
engine.setProperty('rate', 200)


class GrandfistSdk:
    def __init__(self, file):             # Probity :file given to the class
        self.file = file

    def speak(self, text):                # Definite the speak variable
        engine.say(text)
        engine.runAndWait()

    def __writeSpeakPrint(self, msg):     # Make a Methode that speak a text, Print the text in the console and
        self.file.write(msg)              # Write the text in a File
        self.speak(msg)
        print(msg)

    def __writePrint(self, msg):          # Print a text in the console and write it in a file
        self.file.write(msg)
        print(msg)

    def __write(self, msg):               # Write a text in a file
        self.file.write(msg)

    def Loading(self):                    # Initial Loading
        self.__writeSpeakPrint("Lädt deinen Smart Assistent!\n")
        for i in tqdm(range(100), desc="loading", colour="green"):      # A Loading bar with some parameters
            time.sleep(0.010)

    def howcanihelpyou(self):             # Asks you "How can i help you? Sir! "
        self.__writeSpeakPrint("Wie kann ich ihnen helfen sir?\n")

    def __god_morning(self, date_time):   # Say "Good morning" and the current time
        self.__writeSpeakPrint(f"Guten morgen Sir es ist {date_time}\n")

    def __god_day(self, date_time):       # Say "Good day" and the current time
        self.__writeSpeakPrint(f"Guten Tag, Sir! es ist {date_time}\n")

    def __god_night(self, date_time):     # Say "Good evening" and the current time
        self.__writeSpeakPrint(f"Guten abend sir! es ist {date_time}\n")

    def date_time(self):                  # Definite the current time and date withe the `datetime` Package
        return datetime.datetime.now().strftime("%H:%M:%S")

    def welcomeMessage(self):             # Decide what time is it and what Welcome massage its brought to you
        stunde = datetime.datetime.now().hour       # declare what an hour is
        date_time = self.date_time()
        if stunde <= stunde < 12:                   # decide, is it Morning?
            self.__god_morning(date_time)
        elif 12 <= stunde < 18:                     # decide, is it mid-day?
            self.__god_day(date_time)
        else:                                       # else it's night!
            self.__god_night(date_time)

    def takeCommand(self):                 # take the command and print it in the command shell
        r = sr.Recognizer()
        with sr.Microphone() as source:    # Declare that the Speaker source from your microphone  is
            self.__writePrint("hört zu...\n")
            audio = r.listen(source)

            try:                           # Try to Listen to the audio and understand it
                statement = r.recognize_google(audio, language='de')
                self.__writePrint(f"Benutzer sagt:{statement}\n")

            except Exception as e:         # if he doesn't understood it, the n he speak that he doesn't understood it
                err = "ich habe dies nicht Verstanden, Bitte wählen sie eine aktion für mich aus!"
                self.__writeSpeakPrint(err + "\n")
                return "None"
            return statement

    def is_yt_search(self):             # Aks you in the command shell, if you wand to open the GUI
        try:
            is_open_gui = input("Möchten sie es über ein GUI öffnen? (y|n)... ")

            if is_open_gui == "y":      # If you answers y, then he use the WindowMode command
                self.windowedMode()
            elif is_open_gui == "n":    # If you answers n, then he use the consoleMode command
                self.consoleMode()
            else:                       # if you answers something else then he print something in the command shell
                print('Falsche Eingabe, du noob... und tschüss!')
                exit()

        except KeyError:
            pass

    def youtube_search(self, search_term): # declare for the Api what there search for
        api_key = 'AIzaSyAw5WFwcp2I8Y9AVsujc916vDBigUi3IRk'
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            part="snippet",
            maxResults=3,
            q=search_term,
            type="video"
        )
        response = request.execute()
        return response

    def openVideo(self, watch_id):         # open the video in a new browser tab with the link below
        webbrowser.open_new_tab("youtube.com/watch?v=" + watch_id)

    def consoleMode(self):                 # declares the 'consoleMode' command

        search_term = input("nach welchen video wird gesucht?\n")

        videos = self.youtube_search(search_term)

        # print results to console
        i = 1
        for video in videos["items"]:
            print(f'{i}: {video["snippet"]["title"]}')
            i += 1

        # ask for chosen result
        try:
            title_number = int(input("bitte geben sie die zahl des richtigen titels an: "))
        except ValueError:
            print("Bitte eime gültige Eingabe eingeben")
            pass

        item = videos["items"][title_number - 1]
        self.openVideo(item["id"]["videoId"])

        print("nun spielt: " + item["snippet"]["title"] + " von " + item["snippet"]["channelTitle"])

    def windowedMode(self):         # declare ijn the future that its open a GUI
        pass

    def generateVideoButtons(self, search_term):        # Generate video titels + list in the server conole
        videos = self.youtube_search(search_term)       # Declare Videos for the Function

        i = 1
        for item in videos["items"]:                    # list three items of the from the list
            title = item["snippet"]["title"]
            print(f'{i}: {title}')
            i += 1

    def wiki_search(self, statement):                  # declares the "wiki_search" command
        try:
            wikipedia.set_lang('de')                   # Set the Wiki Language
            say = 'sucht in wikipedia'
            self.__writeSpeakPrint(f"{say}..... ")
            statement = statement.replace("suche auf wikipedia nach", "")
            statement = statement.replace("suche in wikipedia nach", "")
            results = wikipedia.summary(statement, sentences=3)                 # the results saved in a variable
            say_results = f"Den ergebnissen entsprechend... {results}"
            self.__writeSpeakPrint(say_results)
        except wikipedia.exceptions.PageError:
            self.__writeSpeakPrint("Diesen Suchbefehl konnte leider kein Ergebnis zugeordnet werden!")

    def open_gmail(self):                              # open Gmail
        webbrowser.open_new_tab('https://www.gmail.com')                        # open new tab
        self.__writeSpeakPrint("Gmail wurde erfolgreich geeöfnet!\n")
        time.sleep(2)

    def open_new_tab(self):                            # open a new Google tab
        webbrowser.open_new_tab('https://google.com')
        self.__writeSpeakPrint("Ein neues Fenster wurde erfolgreich geöfnet!\n")
        time.sleep(2)

    def say_the_time(self):                            # say the current time in Hours, Minutes, Seconds
        str_time = datetime.datetime.now().strftime("%H:%M:%S")                 # save the time in a Variable
        self.__writeSpeakPrint(f"Die uhrzeit ist {str_time}")
        time.sleep(2)

    def pause(self):                                   # Pause the script for one minuit and 8 seconds
        self.__writeSpeakPrint("Ich bin jetzt für 1 Minute und 8 sekunden pausiert!\n")
        for i in tqdm(range(100), desc="Pause", colour="green"):                # time-Pause-Bar
            time.sleep(0.66666666667)

    def news(self):                                    # open a newspaper in the web
        webbrowser.open_new_tab("https://www.haz.de")
        self.__writeSpeakPrint("Nachrichtenseite wurde Erfolgreich geöfnet, viel spaß bei den Nachrichten!\n")
        time.sleep(2)

    def searchongoogle(self, statement):               # Search Something on google
        statement = statement.replace("suche", "")
        statement = statement.replace("suche nach", "")
        webbrowser.open_new_tab(f'https://www.google.com/search?q={statement}')
        self.__writeSpeakPrint("suche erfolgreich!\n")
        time.sleep(2)

    def qa_api_wolfram(self):                           # API for information's about some towns
        try:
            self.__writeSpeakPrint('ich kann Geografische fragen beantwoten, welche Frage möchtest du mir stellen?\n')
            Frage = self.takeCommand()
            app_id = "LHP5VA-ALEJ9AJ4K5"                # API key
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(Frage)                   # a request from the user
            antwort = next(res.results).text            # results from the request
            antwortEnt = GoogleTranslator(source='auto', target='de').translate(antwort)        # the final answer
            self.__writeSpeakPrint(f"hier die antworten auf deine Frage! {antwortEnt}\n")
            time.sleep(2)
        except StopIteration:                           # if its get an error or something, its an error fang
            self.__writeSpeakPrint("Fehler Bitte Versuchen sie es ein anderes mal!\n ")

            time.sleep(2)

    def who_am_i(self):                                 # "who am i" function, tells you more about the program
        self.__writeSpeakPrint(
            "ich bin Grandfist 2.0 dein persönlicher Assistent, ich wurde programmiert auf ferschiedenste anweisungen "
            "wie "
            "Öffnen von youtube, öffnen von gmail und suche in wikipedia, und noch viele weitere funktionen!\n")
        time.sleep(2)

    def who_made_me(self):                             # "who made me" a functions that tells you more about the DEV
        self.__writeSpeakPrint("Der Programierer Sanitoeter05 hatt mich am 25.6.2021 ins leben gerufen! \n")

    def weather_in(self):                       # a functions that tells you facts about the current weather in a town
        api_key = "f3542b5362066c1a7ab2a409ea70b55d"   # Api key

        base_url = "http://api.openweathermap.org/data/2.5/weather?"    # a base URL
        city_name = input("Gebe den Stadt namen ein : ")

        self.__write("Geben sie den stadt Namen via Tastatur ein: \n")
        self.__write(f"eingabe = {city_name}")

        complete_url = base_url + "appid=" + api_key + "&q=" + city_name

        response = requests.get(complete_url)                           # request the URL

        res = response.json()

        if res["cod"] != "404":                                         # an error fang for 404

            resg = res["main"]

            current_temperature = resg["temp"] - 273.15

            current_pressure = resg["pressure"]

            current_humidity = resg["humidity"]

            z = res["weather"]

            weather_description_en = z[0]["description"]
            weather_description_de = GoogleTranslator(source='auto', target='de').translate(weather_description_en)
            current_temperature_round = round(current_temperature, 1)
            self.__writeSpeakPrint(" Temperatur (in Grad) = " +
                                   str(current_temperature_round) +
                                   "grad Celsius"
                                   "\n Druck (in hPa einheit) = " +
                                   str(current_pressure) +
                                   "\n Feuchtigkeit (in prozent) = " +
                                   str(current_humidity) + "%"
                                                           "\n Beschreibung = " +
                                   str(weather_description_de))

        else:
            self.__writePrint("Error, City not found")

    def callender(self):                                            # calender of the current month
        what_current_date = datetime.datetime.now()                 # define the current date
        current_year = int(what_current_date.strftime("%Y"))        # request the year
        current_month = int(what_current_date.strftime("%m"))       # request the month

        callender_month = calendar.TextCalendar(calendar.MONDAY)
        output = callender_month.formatmonth(current_year, current_month)
        print(output)

    def Joking(self):                               # a method for jokes
        self.__writeSpeakPrint(pyjokes.get_joke("de"))

    def good_bye(self, file):                                       # say good bye
        self.__writeSpeakPrint("Dein Persönlicher assistent, Grandfist, fährt runter!\n")
        file.close()
