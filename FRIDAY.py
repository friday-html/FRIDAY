
'''
        Supported commands :

        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
        4. Tell a joke/another joke : Says a random dad joke.
        5. Current weather in {cityname} : Tells you the current condition and temperture
        7. Hello
        8. play me a video : Plays song in your VLC media player
        9. change wallpaper : Change desktop wallpaper
        10. news for today : reads top news of today
        11. time : Current system time
        12. top stories from google news (RSS feeds)
        13. tell me about xyz : tells you about xyz
'''

import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import urllib2
import json
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
import wikipedia
import random
from time import strftime


def fridayResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def assistant(command):
    "if statements for executing commands"

    #open subreddit Reddit
    if 'open reddit friday' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        fridayResponse('The Reddit content has been opened for you Sir.')

    elif 'shutdown friday' in command:
        fridayResponse('Bye bye Sir. Have a nice day')
        sys.exit()

    #open website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            fridayResponse('The website you have requested has been opened for you Sir.')
        else:
            pass

    #greetings
    elif 'hello friday' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            fridayResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            fridayResponse('Hello Sir. Good afternoon')
        else:
            fridayResponse('Hello Sir. Good evening')

    elif 'help me friday' in command:
        fridayResponse("""
        You can use these commands and I'll help you out:

        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
        4. Tell a joke/another joke : Says a random dad joke.
        5. Current weather in {cityname} : Tells you the current condition and temperture
        7. Greetings
        8. play me a video : Plays song in your VLC media player
        9. change wallpaper : Change desktop wallpaper
        10. news for today : reads top news of today
        11. time : Current system time
        12. top stories from google news (RSS feeds)
        13. tell me about xyz : tells you about xyz
        """)


    #top stories from google news
    elif 'news for today friday' in command:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:15]:
                fridayResponse(news.title.text.encode('utf-8'))
        except Exception as e:
                print(e)

    #current weather
    elif 'give me the current weather friday' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='*****************')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            fridayResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

    #time
    elif 'whats the time' in command:
        import datetime
        now = datetime.datetime.now()
        fridayResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    #send email
    elif 'email friday' in command:
        fridayResponse('Who is the recipient?')
        recipient = myCommand()
        if 'owen' in recipient:
            sofiaResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('savirselagan@gmail.com', '*************')
            mail.sendmail('savirselagan@gmail.com', 'cheno947@gmail.com', content)
            mail.close()
            fridayResponse('Email has been sent successfuly. You can check your inbox.')
        else:
            fridayResponse('I don\'t know what you mean!')

    #launch any application
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)

        fridayResponse('I have launched the desired application')

    #play youtube song
    elif 'play me a song friday' in command:
        path = '/Users/savirselagan/Documents/videos/'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        fridayResponse('What song shall I play Sir?')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urllib2.urlopen(url)
            html = response.read()
            soup1 = soup(html,"lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)

            url = url_list[0]
            ydl_opts = {}

            os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            vlc.play(path)

            if flag == 0:
                fridayResponse('I have not found anything in Youtube ')

    #change wallpaper
    elif 'change wallpaper' in command:
        folder = '/Users/savirselagan/Documents/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = '***************'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key #pic from unspalsh.com
        f = urllib2.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urllib.urlretrieve(photo, "/Users/savirselagan/Documents/wallpaper/a") # Location where we download the image to.
        subprocess.call(["killall Dock"], shell=True)
        fridayResponse('wallpaper changed successfully')

    #ask me anything
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                fridayResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
                print(e)
                sofiaResponse(e)

fridayResponse('Hi User, I am FRIDAY and I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
