from langdetect import detect
import feedparser
import html2text
import pyttsx3
import re
import os

class RSSReader:
    """
    RSSReader class for reading RSS feeds using text-to-speech (TTS).

    Attributes:
        engine (pyttsx3.init()): The text-to-speech engine.
        url (str): The URL of the RSS feed.
    """
    def __init__(self):
        """
        Initialize an RSSReader object with a TTS engine and default rate.
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 175)
        self.url = None

    def clear_screen(self):
        """
        Clears the terminal screen (cross-platform).
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def change_voice(self, language):
        """
        Change the TTS voice based on the detected language or set it to default.

        Args:
            language (str): The language for which to set the voice.

        Returns:
            bool: True if the voice is set; otherwise, False.
        """
        for voice in self.engine.getProperty('voices'):
            lg = voice.id.split("\\")[-1].split("_")[2]
            if language == lg:
                self.engine.setProperty('voice', voice.id)
                return True
        print(f"Voice for language '{language}' not found. Using default voice.")

    def end_voice(self):
        """
        Stop the TTS engine.
        """
        self.engine.stop()

    def tts(self, text, language):
        """
        Read the provided text using text-to-speech in the specified language.

        Args:
            text (str): The text to be read.
            language (str): The language for TTS.
        """
        self.change_voice(language)
        self.engine.say(text)
        self.engine.runAndWait()

    def detect_language(self, text):
        """
        Detect the language of the given text.

        Args:
            text (str): The text to detect the language from.

        Returns:
            str: The language code (e.g., 'EN-US' or 'PT-BR').
        """
        language = detect(text)
        print("Text in English!" if language != "pt" else "Texto em Português!")
        return "EN-US" if language != "pt" else "PT-BR"

    def rsstotext(self, url, index):
        """
        Fetch and convert an article from an RSS feed to plain text.
        """
        NewsFeed = feedparser.parse(url)
        entry = NewsFeed.entries[index]

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.body_width = 0

        to_read = text_maker.handle(entry.summary)
        to_read = re.sub(r'http\S+', '', to_read)

        return to_read

    def change_rate(self):
        """
        Change the TTS reading rate based on user input.
        """
        self.clear_screen()
        print("Default rate: 175 | (slow: 100, fast: 200)\n\nEnter the new rate (e.g., 150):")
        rate = int(input())
        self.engine.setProperty('rate', rate)

    def input_url(self):
        """
        Prompt the user to input an RSS feed URL.

        Returns:
            str: The user-inputted URL.
        """
        self.clear_screen()
        print("Enter the RSS URL feed:")
        return input()

    def read_rss(self, pos):
        """
        Read an article from the RSS feed using TTS.

        Args:
            pos (int): The position of the article to read.
        """
        to_read = self.rsstotext(self.url, pos)
        language = self.detect_language(to_read)
        self.tts(to_read, language)

    def load_rss(self):
        """
        Load articles from an RSS feed and provide a menu for selecting and reading them.
        """
        if not self.url:
            self.url = self.input_url()

        pos = 0
        NewsFeed = feedparser.parse(self.url)

        while True:
            options = [pos + i for i in range(1, 4)] + [8, 9, 0]
            self.clear_screen()
            for i in range(3):
                entry_num = pos + i + 1
                if entry_num <= len(NewsFeed.entries):
                    print(f"{entry_num}. {NewsFeed.entries[pos + i].title}")

            print("8. Next page\n9. Previous page\n0. Exit")
            try:
                choice = int(input("Select an option: "))
                if choice in options:
                    if choice == 8:
                        pos = min(pos + 3, len(NewsFeed.entries) - 3)
                    elif choice == 9:
                        pos = max(0, pos - 3)
                    elif choice == 0:
                        break
                    else:
                        selected_entry = pos + choice - 1
                        if selected_entry >= 0:
                            self.read_rss(selected_entry)
                        else:
                            print("Invalid entry number.")
                else:
                    print("Please input a valid option.")
            except ValueError:
                print("Invalid input. Please enter a valid option.")

    def main_menu(self):
        """
        Display the main menu and its options for interacting with the RSS reader.
        """
        while True:
            self.clear_screen()
            if not self.url:
                self.url = self.input_url()

            print(f"RSS URL feed: {self.url}\n\nOptions:")
            print("1. Load RSS feed")
            print("2. Change URL of RSS feed")
            print("3. Change TTS rate")
            print("0. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                self.load_rss()
            elif choice == "2":
                self.url = self.input_url()
            elif choice == "3":
                self.change_rate()
            elif choice == "0":
                self.clear_screen()
                self.end_voice()
                print("Goodbye!")
                break

if __name__ == "__main__":
    reader = RSSReader()
    reader.main_menu()
