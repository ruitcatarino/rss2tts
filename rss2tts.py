from langdetect import detect
import feedparser
import html2text
import pyttsx3
import sys
import re
import os

"""
clear cleans the terminal.
""" 
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

"""
change_voice changes the TTS language.

:param engine: Engine from TTS
:param language: language of the article
""" 
def change_voice(engine, language):
    for voice in engine.getProperty('voices'):
        lg = voice.id.split("\\")
        lg = lg[6].split("_")
        lg = lg[2]
        if language == lg:
            engine.setProperty('voice', voice.id)
            return True

    print("Language '{}' not found. Set to default.".format(language))

"""
end_voice clears the engine.

:param engine: Engine from TTS
""" 
def end_voice(engine):
    engine.stop()

"""
tts reads the article.

:param engine: Engine from TTS
:param toread: text to read
:param language: language of the article
""" 
def tts(engine,toread,language):
    change_voice(engine,language)

    engine.say(toread)

    engine.runAndWait()

"""
detect_language detects the language from the article.

:param toread: text to read
:return: the language from the article
""" 
def detect_language(toread):
    language = detect(toread)

    if language == "pt":
        print("Texto em Português!")
        return "PT-BR"
    else:
        print("Text in English!")
        return "EN-US"

"""
rsstotext reads article and converts it to plain text.

:param url: URL of RSS
:param pos: position of the article
:return: plaintext from article
""" 
def rsstotext(url,pos):
    NewsFeed = feedparser.parse(url)
    entry = NewsFeed.entries[pos]

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.body_width = 0

    toread = text_maker.handle(entry.summary)
    toread = toread.split("![](")
    toread = ''.join(toread)
    toread = re.sub(r'http\S+', '', toread)
    print(toread)

    return toread

"""
change_rate change reading rate of TTS.

:param engine: Engine from TTS
""" 
def change_rate(engine):
    clear()
    print("Default rate: 175 | (slow:100, fast:200)\n\nYou want to change the rate too:")
    rate = int(input())
    engine.setProperty('rate', rate)

"""
url_input reads URL inputed from user.

:return: URL inputed from user
""" 
def url_input():
    clear()
    print("Insert a RSS URL feed: ")
    return input()

"""
read_rss detects laguage of article selected and reads it using TTS.

:param engine: Engine from TTS
:param url: URL of RSS
:param pos: position of the article
""" 
def read_rss(engine,url,pos):
    toread = rsstotext(url,pos)

    language = detect_language(toread)

    tts(engine,toread,language)


"""
load_rss grabs articles from RSS.

:param engine: Engine from TTS
:param url: URL of RSS
""" 
def load_rss(engine,url):

    text = "Choose one:\n{}. {}\n{}. {}\n{}. {}\nN. Next page\nB. Previous page\n0. Exit"

    text_inv = text + "\nPlease Input one of the avaliable options!\n"

    pos = 0

    NewsFeed = feedparser.parse(url)

    while 1:

        ops = [str(pos+1),str(pos+2),str(pos+3),"N","B","0"]

        clear()
        print(text.format(pos+1,NewsFeed.entries[pos].title,pos+2,NewsFeed.entries[pos+1].title,pos+3,NewsFeed.entries[pos+2].title))
        choice = input()

        while choice not in ops:
            clear()
            print(text_inv.format(pos+1,NewsFeed.entries[pos].title,pos+2,NewsFeed.entries[pos+1].title,pos+3,NewsFeed.entries[pos+2].title))
            choice = input()

        if choice == str(pos+1):
            read_rss(engine,url,pos)
        elif choice == str(pos+2):
            read_rss(engine,url,pos+1)
        elif choice == str(pos+3):
            read_rss(engine,url,pos+2)
        elif choice == "N":
            if pos + 6 <= len(NewsFeed.entries):
                pos += 3
        elif choice == "B":
            if pos - 3 >= 0:
                pos -= 3
        elif choice == "0":
            break

"""
main_menu: displays the Main menu and its options

:param engine: Engine from TTS
:param url: URL of RSS
""" 
def main_menu(engine,url="None"):

    text = "RSS URL feed: {}\n\nOptions:\n1. Load RSS feed\n2. Change URL of RSS feed\n3. Change TTS rate\n0. Exit\n"

    text_inv = text + "\nPlease Input one of the avaliable options!\n"

    ops = ["0","1","2","3"]

    while 1:

        if url == "None":
            url = url_input()

        clear()
        print(text.format(url))
        choice = input()

        while choice not in ops:
            clear()
            print(text_inv.format(url))
            choice = input()

        if choice == "1":
            load_rss(engine,url)
            #read_rss(engine,url,1)
        elif choice == "2":
            url = url_input()
        elif choice == "3":
            change_rate(engine)
        elif choice == "0":
            clear()
            sys.exit("Goodbye!")


if __name__ == "__main__":
    #Create object (voice)
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)

    main_menu(engine)

    end_voice(engine)
