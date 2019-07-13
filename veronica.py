import pyttsx3
import datetime
import wikipedia
import webbrowser
import random
import os
import time
import requests
import json
import calendar
import smtplib
import speech_recognition as sr
import urllib.request


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    '''
    Takes string message to speak it out 
    '''
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    '''
    Based on hour of the day wishes
    '''
    wishes = ["How you doing?", "How are you Boss?", "Good to see you again."]
    hour = datetime.datetime.now().hour
    if hour in range(0, 12):
        speak("Good Morning!")
    elif hour in range(12, 18):
        speak("Good Afternoon!!")
    elif hour in range(18, 23):
        speak("Good Evening!")
    else:
        speak("Good Night!")
    speak(random.choice(wishes))
    speak("I am Veronica!. Tell me Boss How Can I Help you?")

def read_news(top):
    '''
    This uses to news api and shows the news as many as inputed by user in "top" variaable
    '''
    news_list = list()
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=in&'
       'apiKey=a94c6e5849344ac49fa7dcb140785c18')
    response = requests.get(url)
    data = json.loads(response.text)
    if top == 0:
        return 
    for count in range(0, top):
        news_dict = dict()
        news_dict['title'] = data['articles'][count]['title']
        news_dict['content'] = data['articles'][count]['content']
        news_dict['source'] = data['articles'][count]['source']['name']
        news_list.append(news_dict)
    return news_list

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)    
        print("Say that again please...")  
        return "None"
    return query

# Registering webbrowser
chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))

def play_song(music_dir, songs):
    '''Playing songs or any other file from the directory passed as first argument and the list of songs as second
    argument.
    '''
    index = random.randint(0, len(songs) + 1)
    song = songs[index]
    pieces = (song.split('.'))[0]
    song_info = pieces.split('-')
    speak(f"Playing {song_info[1]} by {song_info[0]}")
    os.startfile(os.path.join(music_dir, song))

def sendEmali(to, content):
    fh = open('info.txt')
    email_id = (fh.readline()).strip()
    password = (fh.readline()).strip()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_id, password)
    server.sendmail(email_id, to, content)
    server.close()

def weather(city):
    '''Gives information about temperature, weather condition and humidity of a place'''
    
    api_add = "https://api.openweathermap.org/data/2.5/weather?appid=4de9ba341d3f25525a22293e10380c85&q="
    url = api_add + city
    print(url)
    data = (urllib.request.urlopen(url).read()).decode("utf-8")
    json_data = json.loads(data)
    weather_description = json_data["weather"][0]['description']
    temperature = (json_data["main"]["temp"] - 273.15)
    humidity = json_data["main"]['humidity']
    speak(f"{weather_description}")
    speak("Temperature is {0:.2f} degree celcius".format(temperature))
    speak(f"Himidity is {humidity}")


if __name__ == "__main__":
    # speak("Karan is a awesome Guy!!")
    wishMe()
    while True:
        query = input("Enter query: ").lower()
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", '')
            results = wikipedia.summary(query, sentences=2)
            print(results)
            speak("According to the wikipedia...")
            speak(results)
        elif 'open youtube' in query:
            speak("Opening Youtube..")
            webbrowser.get("chrome").open('youtube.com')
        elif 'open google' in query:
            speak("Opening google...")
            webbrowser.get("chrome").open("google.com")
        elif 'open stackoverflow' in query:
            speak("Opening stackoverflow...")
            webbrowser.get("chrome").open("stackoverflow.com")
        elif 'open gmail' in query:
            speak("Opening gmail...")
            webbrowser.get("chrome").open("gmail.com")
        elif 'open facebook' in query:
            speak("Opening facebook")
            webbrowser.get("chrome").open("facebook.com")
        elif 'play music' in query:
            music_dir = "E:\\English Songs"
            songs = os.listdir(music_dir)
            play_song(music_dir, songs)
        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Boss, the time is {strTime}")
        elif "show calendar" in query:
            speak("Which year's calendar you want to see?")
            year = int(input())
            speak ("Any Specific month?")
            month = input().lower()
            months = {'january' : 1, 'february' : 2, 'march' : 3, "april" : 4,
            "may" : 5, "june" : 6, "july" : 7, "august" : 8, "september" : 9, "october" : 10, "november" : 11, "december" : 12}
            speak("Here is you calendar...")
            if month not in months:
                print(calendar.calendar(year))
            else:
                print(calendar.month(year, months[month]))
        elif "open code" in query:
            path = "E:\\Downoads\\softwares\\VSCode-win32-x64-1.32.1\\Code.exe"
            speak("Opening Visual Studio Code...")
            os.startfile(path)
        elif "open chrome" in query:
            path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            speak("Opening Google Chrome...")
            os.startfile(path)
        elif "open codeblocks" in query:
            path = "C:\\Program Files (x86)\\CodeBlocks\\codeblocks.exe"
            speak("Opening Codeblocks...")
            os.startfile(path)
        elif "open whatsapp" in query:
            path = "C:\\Users\\karan\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
            speak("Opening Whatsapp...")
            os.startfile(path)
        elif "send email " in query:
            try:
                speak("Whom you want to send?")
                to = input()
                speak("What you want to say?")
                content = input()
                sendEmali(to, content)
                speak("Okay Boss, Email has been sent!!")
            except Exception as e:
                print(e)
                speak("Sory Boss, Email Couldn't be sent!!")
        elif "read news" in query:
            speak("How many news you want me to read")
            top = int(input())
            if top != 0:
                speak(f"Reading top {top} news")
                news = read_news(top)
                for item in news:
                    print(f"Reading {item['title']} from {item['source']}")
                    speak(f"Reading {item['title']} from {item['source']}")
                    print(item['content'])
                    speak(item['content'])
                    time.sleep(3)
        elif "open ums" in query:
            speak("Opening UMS...")
            webbrowser.get("chrome").open("ums.lpu.in/lpuums")
        elif "weather" in query:
            speak("Which city?")
            city = input()
            try:
                weather(city) 
            except Exception as e:
                print(e)
                speak("Couldn't find weather! Check city name and try again...")
                city = input()
        elif "quit" in query:
            speak("Have a great time.")
            speak("See you soon!")
            break
        else:
            speak("I am sorry!I don't understand.")
