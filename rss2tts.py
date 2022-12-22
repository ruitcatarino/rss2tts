import pyttsx3
import feedparser
import html2text

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

def tts(engine,toread):

    print(toread)

    engine.say(toread)

    engine.runAndWait()

if __name__ == "__main__":
    
    #Create object (voice)
    engine = pyttsx3.init()

    change_voice(engine,"PT-BR")
    engine.setProperty('rate', 200)
    
    NewsFeed = feedparser.parse("https://www.rtp.pt/noticias/rss")
    entry = NewsFeed.entries[1]

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.body_width = 0

    tts(engine,text_maker.handle(entry.summary))

    end_voice(engine)