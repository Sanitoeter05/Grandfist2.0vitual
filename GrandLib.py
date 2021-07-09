import datetime
import time
import calendar

import requests
import speech_recognition as sr
import pyttsx3
import wikipedia
import wolframalpha
import webbrowser
from deep_translator import GoogleTranslator
from googleapiclient.discovery import build
from tqdm import tqdm

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[1].id')
engine.setProperty('rate', 200)


# klassen: tutorial anschauen ;)
class GrandfistSdk:
    def __init__(self, file):
        # statt die ganze Zeit `file` mit zu übergeben, können wir es der Klasse geben, die es sich in ihrem eigenen
        # Kontext merkt
        self.file = file

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

        # private methode, die nur innerhalb der Klasse genutzt werden kann
        # wird mit `__` double underscore definiert
        # konzept nennt sich encapsulation (glaube ich xD)
        # https://www.geeksforgeeks.org/private-methods-in-python/ bitte lesen

    def __writeSpeakPrint(self, msg):
        # auf klassen variablen kannst du dann mit `self.XXX` zugreifen
        self.file.write(msg)
        self.speak(msg)
        print(msg)

    def __writePrint(self, msg):
        self.file.write(msg)
        print(msg)

    def __write(self, msg):
        self.file.write(msg)

    def startup(self):
        self.__writeSpeakPrint("Lädt deinen Smart Assistent!\n")
        for i in tqdm(range(100), desc="loading", colour="green"):
            time.sleep(0.010)

    def howcanihelpyou(self):
        self.__writeSpeakPrint("Wie kann ich ihnen helfen sir?\n")

    def __god_morning(self, date_time):
        # statt jedes mal write, speak und print separat aufzurufen
        # habe ich das in eine funktion gepackt
        self.__writeSpeakPrint(f"Guten morgen Sir es ist {date_time}\n")

    def __god_day(self, date_time):
        self.__writeSpeakPrint(f"Guten Tag, Sir! es ist {date_time}\n")

    def __god_night(self, date_time):
        # hier und alles danach muss zu __writeSpeakPrint refactored
        # werden
        self.__writeSpeakPrint(f"Guten abend sir! es ist {date_time}\n")

    def date_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def welcomeMessage(self):
        stunde = datetime.datetime.now().hour
        date_time = self.date_time()
        if stunde <= stunde < 12:
            self.__god_morning(date_time)
        elif 12 <= stunde < 18:
            self.__god_day(date_time)
        else:
            self.__god_night(date_time)

    # sehr nice vom code <3
    # ggf. findest du noch einen besseren Ausdruck als takeCommand ;)
    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.__writePrint("hört zu...\n")
            audio = r.listen(source)

            try:
                statement = r.recognize_google(audio, language='de')
                self.__writePrint(f"Benutzer sagt:{statement}\n")

            except Exception as e:
                err = "ich habe dies nicht Verstanden, Bitte wählen sie eine aktion für mich aus!"
                self.__writeSpeakPrint(err + "\n")
                return "None"
            return statement

    def is_yt_search(self):
        try:
            is_open_gui = input("Möchten sie es über ein GUI öffnen? (y|n)... ")

            if is_open_gui == "y":
                self.windowedMode()
            elif is_open_gui == "n":
                self.consoleMode()
            else:
                print('Falsche Eingabe, du noob... und tschüss!')
                exit()

        except KeyError:
            pass

    def youtube_search(self, search_term):
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

    def openVideo(self, watch_id):
        webbrowser.open_new_tab("youtube.com/watch?v=" + watch_id)

    def consoleMode(self):

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

    def windowedMode(self):
        pass

    def generateVideoButtons(self, search_term):
        videos = self.youtube_search(search_term)

        i = 1
        for item in videos["items"]:
            title = item["snippet"]["title"]
            print(f'{i}: {title}')
            i += 1

    def wiki_search(self, statement):
        try:
            wikipedia.set_lang('de')
            say = 'sucht in wikipedia'
            self.__writeSpeakPrint(f"{say}..... ")
            statement = statement.replace("suche auf wikipedia nach", "")
            statement = statement.replace("suche in wikipedia nach", "")
            results = wikipedia.summary(statement, sentences=3)
            say_results = f"Den ergebnissen entsprechend... {results}"
            self.__writeSpeakPrint(say_results)
        except wikipedia.exceptions.PageError:
            self.__writeSpeakPrint("Diesen Suchbefehl konnte leider kein Ergebnis zugeordnet werden!")

    def open_gmail(self):
        webbrowser.open_new_tab('https://www.gmail.com')
        self.__writeSpeakPrint("Gmail wurde erfolgreich geeöfnet!\n")
        time.sleep(2)

    def open_new_tab(self):
        webbrowser.open_new_tab('https://google.com')
        self.__writeSpeakPrint("Ein neues Fenster wurde erfolgreich geöfnet!\n")
        time.sleep(2)

    def say_the_time(self):
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.__writeSpeakPrint(f"Die uhrzeit ist {str_time}")
        time.sleep(2)

    def pause(self):
        self.__writeSpeakPrint("Ich bin jetzt für 1 Minute und 8 sekunden pausiert!\n")
        for i in tqdm(range(100), desc="Pause", colour="green"):
            time.sleep(0.66666666667)

    def news(self):
        webbrowser.open_new_tab("https://www.haz.de")
        self.__writeSpeakPrint("Nachrichtenseite wurde Erfolgreich geöfnet, viel spaß bei den Nachrichten!\n")
        time.sleep(2)

    def searchongoogle(self, statement):
        statement = statement.replace("suche", "")
        statement = statement.replace("suche nach", "")
        webbrowser.open_new_tab(f'https://www.google.com/search?q={statement}')
        self.__writeSpeakPrint("suche erfolgreich!\n")
        time.sleep(2)

    def qa_api_wolfram(self):
        try:
            self.__writeSpeakPrint('ich kann Geografische fragen beantwoten, welche Frage möchtest du mir stellen?\n')
            Frage = self.takeCommand()
            app_id = "LHP5VA-ALEJ9AJ4K5"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(Frage)
            antwort = next(res.results).text
            antwortEnt = GoogleTranslator(source='auto', target='de').translate(antwort)
            self.__writeSpeakPrint(f"hier die antworten auf deine Frage! {antwortEnt}\n")
            time.sleep(2)
        except StopIteration:
            self.__writeSpeakPrint("Fehler Bitte Versuchen sie es ein anderes mal!\n ")

            time.sleep(2)

    def who_am_i(self):
        self.__writeSpeakPrint(
            "ich bin Grandfist 2.0 dein persönlicher Assistent, ich wurde programmiert auf ferschiedenste anweisungen "
            "wie "
            "Öffnen von youtube, öffnen von gmail und suche in wikipedia, und noch viele weitere funktionen!\n")
        time.sleep(2)

    def who_made_me(self):
        self.__writeSpeakPrint("Der Programierer Sanitoeter05 hatt mich am 25.6.2021 ins leben gerufen! \n")

    def weather_in(self):
        api_key = "f3542b5362066c1a7ab2a409ea70b55d"

        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = input("Gebe den Stadt namen ein : ")

        self.__write("Geben sie den stadt Namen via Tastatur ein: \n")
        self.__write(f"eingabe = {city_name}")

        complete_url = base_url + "appid=" + api_key + "&q=" + city_name

        response = requests.get(complete_url)

        res = response.json()

        if res["cod"] != "404":

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

    def callender(self):
        what_current_date = datetime.datetime.now()
        current_year = int(what_current_date.strftime("%Y"))
        current_month = int(what_current_date.strftime("%m"))

        callender_month = calendar.TextCalendar(calendar.MONDAY)
        output = callender_month.formatmonth(current_year, current_month)
        print(output)

    def good_bye(self, file):
        self.__writeSpeakPrint("Dein Persönlicher assistent, Grandfist, fährt runter!\n")
        file.close()
