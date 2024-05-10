import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import requests
from bs4 import BeautifulSoup
import pywhatkit
import pyautogui
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am David, how may I help you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please.....")
        return "None"
    return query


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'search' in query:
            query = query.replace("search", "")
            keywords = "+".join(query.split())
            webbrowser.open(f"https://www.google.com/search?q={keywords}")
            time.sleep(2)  # Delay after opening the browser

        elif any(word in query for word in ['name', 'about']):
            speak("Hi! My name is David. I am an AI-based Virtual Voice Assistant capable of performing all your daily tasks!")

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("https://www.stackoverflow.com")

        elif 'time' in query:
            currentTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {currentTime}")

        elif 'date' in query:
            currentDate = datetime.datetime.now().strftime("%D:%M:%Y")
            speak(f"The date is {currentDate}")

        elif any(word in query for word in ['up', 'increase']):
            pyautogui.press("volumeup")

        elif any(word in query for word in ['down', 'decrease']):
            pyautogui.press("volumedown")

        elif 'mute' in query:
            pyautogui.press("volumemute")

        elif 'play' in query:
            query = query.replace("play", "")
            keywords = "+".join(query.split())
            speak(f"Playing... {query}")
            pywhatkit.playonyt(keywords)

        elif 'temperature' in query:
            city = "Chennai"
            search = f"temperature in {city}"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            try:
                temperature = soup.find("div", class_="BNeawe").text
                speak(f"Current {search} is {temperature}")
            except AttributeError:
                speak(f"Sorry, I couldn't find the temperature for {city}")

        elif 'screenshot' in query:
            im = pyautogui.screenshot()
            speak("Taking screenshot")
            im.save("ss.jpg")

        elif 'picture' in query:
            pyautogui.press("super")
            pyautogui.typewrite("camera")
            pyautogui.press("enter")
            pyautogui.sleep(2)  # Giving time to open camera app
            speak("Smile!")
            pyautogui.press("enter")

        elif any(word in query for word in ['quit', 'exit']):
            speak("Have a nice day!")
            exit()
