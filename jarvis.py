import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import subprocess, sys
import smtplib
from googlesearch import search
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0 ].id) 

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def GreetMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning boss")
    elif hour >=12 and hour < 18:
        speak("Good afternoon boss")
    else:
        speak("Good evening boss")
    speak("Jarvis activated! How may I help you boss?")

def ListenCmd():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print ("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-us')
        print(f"Boss's command: {query}\n")

    except Exception as e:
        print("error report: ", e)
        print("Please repeat that again")
        return"None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('Enter your Email id here', 'Enter your password here')
    server.sendmail('Enter your email id ', to, content)
    """
    please enter the detalis before running, this allows your voice 
    assistant to send an email with whatever content you ask it to type.
    PLEASE TURN ON LESS SECURE APPS IN YOUR GMAIL for using this feature. 
    """
    server.close()

def searchGoogle(search_query):
    for url in search(search_query, tld = 'com', num = 1, stop=1, pause = 2):
        webbrowser.open_new(url)

def mkDir(p_dir, dir):
    
    path = os.path.join(p_dir, dir)
    os.mkdir(path)

def crtTextfile(filename):
    extension = ".txt"
    global file_1
    file_1 = filename + extension
def wrtTextfile(data):
    saved_path = "Enter the path where you want to save the file."
    #please enter the email id before using this feature.
    completeName = os.path.join(saved_path, file_1)
    f = open(completeName,"w+")
    f.write(f"{data}")
    f.close()

def turnoff(turnoff_query):
    if(turnoff_query == 'shutdown'):
        os.system("shutdown /s /t 1")
    if(turnoff_query == 'restart'):   
        os.system("shutdown /r /t 1")  

if __name__ == "__main__":
    GreetMe()
    while True:
        query = ListenCmd().lower()

        if "wikipedia" in query:
            speak("Searching wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(results)
            print(results)
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Boss, time is {strTime}")

        elif 'open code' in query:
            subprocess.call(['code'])

        elif 'open email' in query:
            try:
                speak('What should I send')
                content = ListenCmd()
                to = "Enter the email id you want to send"
                #please enter the email id before using this feature.
                sendEmail(to,content)
                speak("Boss, Email sent succesfully.")
            except Exception as e:
                print(e)
                speak("Boss, failed to send email")

        elif 'open google' in query:
            try:
                speak('What should I browse for you?')
                search_query = ListenCmd()
                speak("Boss, here's what you asked for.")
                searchGoogle(search_query)
            except Exception as e:
                print(e)
                speak("Boss, search failed, please repeat it again.")

        elif 'thank you' in query:
            speak("It's my pleasure to serve you Boss")
        
        elif 'create a folder' in query:
            try:
                speak("By what name do you want to create Boss?")
                dir = ListenCmd()
                p_dir = "Enter the path before running."
                #give the complete path where you want to create this directory to p_dir
                mkDir(p_dir, dir)
                speak(f"Created {dir} folder succesfully!")
            except Exception as e:
                print(e)
                speak("Failed to create! Please try again Boss")
        
        elif 'create and write a text file' in query:
            try:
                speak("What should I name the file Boss?")
                filename = ListenCmd()
                crtTextfile(filename)
                speak(f"created a text file named {filename}")
                speak(f"What do you want me to write in {filename} file")
                data = ListenCmd()
                wrtTextfile(data)
                speak("Written succesfully!")
            except Exception as e:
                print(e)
                speak("Failed to create! Please try again Boss")

        elif 'turn off' in query:
            try:
                speak('Should I shutdown, restart or sleep?')
                turnoff_query = ListenCmd()
                turnoff(turnoff_query)
                
            except Exception as e:
                print(e)
                speak("Please speak again Boss") 
        elif 'close' in query:
            break
