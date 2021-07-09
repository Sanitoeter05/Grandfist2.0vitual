import codecs
from GrandLib import GrandfistSdk

file = codecs.open("Protokoll.txt", "w", "utf-8")

api_key = 'AIzaSyAw5WFwcp2I8Y9AVsujc916vDBigUi3IRk'

if __name__ == '__main__':
    gfSdk = GrandfistSdk(file)

    gfSdk.startup()
    gfSdk.welcomeMessage()

    while True:
        gfSdk.howcanihelpyou()
        statement = gfSdk.takeCommand().lower()
        if statement == 0:
            continue

        if 'suche auf wikipedia' in statement or 'suche in wikipedia' in statement:
            gfSdk.wiki_search(statement)

        elif 'öffne gmail' in statement:
            gfSdk.open_gmail()

        elif 'öffne neues fenster' in statement:
            gfSdk.open_new_tab()

        elif 'sag mir die zeit' in statement:
            gfSdk.say_the_time()

        elif 'pause' in statement:
            gfSdk.pause()

        elif 'nachrichten' in statement:
            gfSdk.news()

        elif 'suche' in statement or 'suche nach' in statement:
            gfSdk.searchongoogle(statement)

        elif 'frage' in statement or 'ich habe eine frage' in statement:
            gfSdk.qa_api_wolfram()

        elif 'wer bist du' in statement or 'was machst du' in statement:
            gfSdk.who_am_i()

        elif "wer hat dich gemacht" in statement or "wer hat dich er schaffen" in statement or "wer hat dich " \
                                                                                               "programiert" in \
                statement:
            gfSdk.who_made_me()

        elif "spiele auf youtube" in statement:
            gfSdk.is_yt_search()

        elif "wetter" in statement:
            gfSdk.weather_in()

        elif "Kallender" in statement:
            gfSdk.callender()

        if 'auf wiedersehen' in statement:
            gfSdk.good_bye(file)
            break
