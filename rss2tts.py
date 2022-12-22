import pyttsx3
import feedparser
import html2text
import re
from langdetect import detect
import os

#os.system('cls' if os.name == 'nt' else 'clear')

def change_voice(engine, language):
    for voice in engine.getProperty('voices'):
        lg = voice.id.split("\\")
        lg = lg[6].split("_")
        lg = lg[2]
        if language == lg:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' not found".format(language))

def end_voice(engine):
    engine.stop()

def tts(engine,toread,language):
    change_voice(engine,language)

    engine.say(toread)

    engine.runAndWait()

def detect_language(toread):
    language = detect(toread)

    if language == "pt":
        print("Texto em Português!")
        return "PT-BR"
    else:
        print("Text in English!")
        return "EN-US"

def rsstotext(url):
    NewsFeed = feedparser.parse(url)
    entry = NewsFeed.entries[1]

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.body_width = 0

    toread = text_maker.handle(entry.summary)

    toread = toread.split("![](")

    toread = ''.join(toread)

    toread = re.sub(r'http\S+', '', toread)

    print(toread)

    return toread

if __name__ == "__main__":
    
    #Create object (voice)
    engine = pyttsx3.init()

    engine.setProperty('rate', 180)

    toread = rsstotext("https://www.rtp.pt/noticias/rss")

    language = detect_language(toread)

    tts(engine,toread,language)

    end_voice(engine)
