from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import anthropic
# from PIL import Image

import instaloader
import numpy as np
import pyautogui
import requests
# from PyQt5.uic.properties import QtGui
from pywikihow import search_wikihow
from requests import get
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import wikipedia
import webbrowser
import pywhatkit as kit
import sys
import smtplib
import time
import pyjokes
from emailpass import emai, passw
from bs4 import BeautifulSoup

# import subprocess
# import qrcode as qr

# import pytesseract

# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# from object_detect import ObjectDetectionApp
# import twilio
# from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtCore import QTimer, QTime, Qt
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.uic import loadUiType
# from AI import Ui_AI

# import googletrans
# import numpy as np

from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

import openai
openai.api_key = OPENAI_KEY

from gtts import gTTS

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voices', voices[0].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def wish():
    hours = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if 6 <= hours <= 12:
        speak(f"Good Morning Sir...... , Its {tt}")
    elif 12 < hours <= 14:
        speak(f"Good Noon Sir..... , Its {tt}")
    elif 14 < hours <= 17:
        speak(f"Good Afternoon Sir..... , Its {tt}")
    elif 17 < hours <= 19:
        speak(f"Good Evening Sir..... , Its {tt}")
    else:
        speak(f"Good Night Sir..... , Its {tt}")
    speak("I am Your Personal assistant...... Please tell me how can i help you... ")


# def sendEmail():
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=d1b862508ab2499481652560085a9003'
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "five"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")


def camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        cv2.imshow('webcam', img)
        k = cv2.waitKey(1)
        if k == 27 or cv2.getWindowProperty('webcam', cv2.WND_PROP_VISIBLE) < 1:
            break
    cap.release()
    cv2.destroyAllWindows()


def object_detection_function():
    # Load YOLO model
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    # classes = []

    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getUnconnectedOutLayersNames()

    cap = cv2.VideoCapture(0)

    # Increase frame size
    cap.set(3, 1000)
    cap.set(4, 800)

    while True:
        ret, frame = cap.read()

        frame = cv2.resize(frame, (800, 600))

        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(layer_names)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * 800)
                    center_y = int(detection[1] * 600)
                    w = int(detection[2] * 800)
                    h = int(detection[3] * 600)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = (0, 255, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.imshow("Object Detection", frame)

        k = cv2.waitKey(1)
        if k == 27 or cv2.getWindowProperty('Object Detection', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


''' def qr_code_function():
    name = input("Enter User URL or whats you want to make in qr code Here: ")
    filename = input("Whats your file name: ")
    img = qr.make(name)
    img.save(f"./qrcodes/{filename}.png")
    with Image.open(f"./qrcodes/{filename}.png") as img:
        img.show()
    return query'''


def takecommand():
    read = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        read.pause_threshold = 1
        audio = read.listen(source, timeout=10, phrase_time_limit=15)
    try:
        print("Recognizing...")
        query = read.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
    except Exception:
        speak("Say that again please....")
        return "none"
    return query


if __name__ == "__main__":
    try:
        wish()
        while True:
            query = takecommand().lower()
            if "open notepad" in query:
                npath = "C:\\Program Files\\Notepad++\\notepad++.exe"
                os.startfile(npath)
            elif "close notepad" in query:
                speak("okay sir.. , closing notepad")
                os.system("taskkill /f /im notepad++.exe")

            elif "open google chrome" in query:
                gcpath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(gcpath)
            elif "close google chrome" in query:
                speak("okay sir.. , closing google chrome")
                os.system("taskkill /f /im chrome.exe")

            elif "open ms excel" in query:
                expath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
                os.startfile(expath)
            elif "close ms excel" in query:
                speak("okay sir.. , closing ms excel")
                os.system("taskkill /f /im EXCEL.EXE")


            elif "open microsoft edge" in query:
                mepath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
                os.startfile(mepath)
            elif "close microsoft edge" in query:
                speak("okay sir.. , closing microsoft edge")
                os.system("taskkill /f /im msedge.exe")


            elif "open ms word" in query:
                wpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                os.startfile(wpath)
            elif "close ms word" in query:
                speak("okay sir.. , closing ms word")
                os.system("taskkill /f /im WINWORD.EXE")


            elif "open powerpoint" in query:
                ppath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
                os.startfile(ppath)
            elif "close powerpoint" in query:
                speak("okay sir.. , closing powerpoint")
                os.system("taskkill /f /im POWERPNT.EXE")


            elif "open cmd" in query:
                os.system("start cmd")
            elif "close cmd" in query:
                speak("okay sir.. , closing cmd")
                os.system("taskkill /f /im cmd")


            elif "open camera" in query:
                camera()

            elif "stop" in query:
                speak("Thanks for using me sir, have a Good Day....")
                sys.exit()


            elif "play music" in query:
                music_dir = "E:\\music"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, rd))


            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                speak(f"Your ip address is {ip}")

            elif "youtube" in query:
                webbrowser.open("www.youtube.com")
            elif "facebook" in query:
                webbrowser.open("www.facebook.com")
            elif "whatsapp" in query:
                webbrowser.open("www.whatsapp.com")
            elif "spotify" in query:
                webbrowser.open("https://open.spotify.com/")
            elif "linkedin" in query:
                webbrowser.open("www.linkedin.com")
            elif "stack overflow" in query:
                webbrowser.open("www.stackoverflow.com")
            elif "online compiler" in query:
                webbrowser.open("https://www.programiz.com/c-programming/online-compiler/")
            elif "open jis university" in query:
                webbrowser.open("https://www.jisuniversity.ac.in/")
            elif "open google" in query:
                speak("Sir... what should i search on google...")
                cm = takecommand().lower()
                webbrowser.open(f"{cm}")

            elif "send message" in query:
                speak("Sir... Please Tell me what message you want to send...")
                ms = takecommand().lower()
                speak("Sir... Please Tell me that phone number you want to send the message...")
                con = takecommand().lower()
                speak("please, enter the exact time when you want to send the message: ")
                hour = int(input("Enter the hour: "))
                minute = int(input("Enter the minute: "))
                # speak("Sir... Please Tell me the hour...")
                # hou = int(takecommand().lower())
                # speak("Sir... Please Tell me the minutes...")
                # minutes = int(takecommand().lower())
                kit.sendwhatmsg(f"+91{con}", f"{ms}", hour, minute)
                time.sleep(40)

            elif "play video" in query:
                speak("Sir... Please Tell me what is the video's name or what's type of video you want to see...")
                vid = takecommand().lower()
                kit.playonyt(f"{vid}")

            elif "set alarm" in query:
                nn = int(datetime.datetime.now().hour)
                if nn == 22:
                    music_dir = "E:\\music"
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir, songs[0]))


            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            # elif "translate" in query.lower():
            # speak("what ")
            # translator = googletrans.Translator()
            # translation = translator.translate("hello", dest="bn")
            # speak(translation.text)

            elif 'switch the window' in query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "tell me news" in query:
                speak("please wait for few second sir... , fetching the latest news...")
                news()

            elif "send email" in query:
                speak("sir.. What should i say..")
                query = takecommand().lower()
                if "send a file" in query:
                    email = emai
                    password = passw
                    speak("")
                    send_to_email = 'suvrodipchakroborty01@gmail.com'
                    speak("okay sir... what is the subject for this email... ")
                    query = takecommand().lower()
                    subject = query
                    speak("And sir... what is the message for this email... ")
                    query2 = takecommand().lower()
                    message = query2
                    speak("sir.. please enter the correct path of the file into shell.. ")
                    file_location = input("please enter the path here..")

                    speak("please wait.. i am sending email now...")

                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = send_to_email
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    filename = os.path.basename(file_location)
                    attachment = open(file_location, "rb")
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                    msg.attach(part)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(email, password)
                    text = msg.as_string()
                    server.sendmail(email, send_to_email, text)
                    server.quit()
                    speak("Email has been sent to Suvrodip Chakroborty")

                else:
                    email = emai
                    password = passw
                    send_to_email = 'suvrodipchakroborty01@gmail.com'
                    message = query

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(email, password)
                    server.sendmail(email, send_to_email, message)
                    server.quit()
                    speak("Email has been sent to Suvrodip Chakroborty")



            elif "where i am" in query or "where we are" in query:
                speak("wait sir.. let me check")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()

                    city = geo_data['city']

                    country = geo_data['country']
                    speak(f"sir.. i am not sure, but i think you are in {city} city of {country} country")
                except Exception as e:
                    speak("sorry sir.. due to network issue i am not able to find where you are..")
                    pass


            elif "instagram profile" in query or "profile on instagram" in query:
                speak("sir.. please enter the user name correctly..")
                name = input("Enter User name Here: ")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"sir... here is the profile of the user {name}")
                time.sleep(5)
                speak("sir would you like to download profile picture of this account...")
                condition = input("Enter yes for download or no for not download: ")
                if "yes" in condition:
                    mod = instaloader.Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak(
                        "I am done sir.. profile picture is saved in your main folder. now i am redy for another "
                        "command...")
                else:
                    pass

            elif "object detect" in query:
                speak("wait a second sir...")
                object_detection_function()



            elif "activate how to do" in query:
                speak("how to do mode is activated..")
                while True:
                    speak("please tell me what you want to know...")
                    how = takecommand()
                    try:
                        if "exit" in how or "close" in how:
                            speak("okay sir, how to do mode is closed...")
                            break
                        else:
                            max_results = 1
                            how_to = search_wikihow(how, max_results)
                            assert len(how_to) == 1
                            speak(how_to[0].summary)
                    except Exception as e:
                        speak("Sorry sir, i am not able to find this...")

            elif "activate searching mode" in query:
                speak("Searching mode is activated..")
                while True:
                    speak("please tell me what you want to know...")
                    how = takecommand()
                    try:
                        print(f"You asked: {query}")
                        if "exit" in how or "close" in how:
                            speak("okay sir, searching mode is closed...")
                            break
                        else:
                            import google.generativeai as genai

                            genai.configure(api_key="gen ai api key")

                            # Set up the model
                            generation_config = {
                                "temperature": 1,
                                "top_p": 0.95,
                                "top_k": 0,
                                "max_output_tokens": 8192,
                            }

                            safety_settings = [
                                {
                                    "category": "HARM_CATEGORY_HARASSMENT",
                                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                },
                                {
                                    "category": "HARM_CATEGORY_HATE_SPEECH",
                                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                },
                                {
                                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                },
                                {
                                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                },
                            ]

                            model = genai.GenerativeModel(model_name="gemini-1.0-pro",generation_config=generation_config,safety_settings=safety_settings)

                            convo = model.start_chat(history=[
                                {
                                    "role": "user",
                                    "parts": [query]
                                },
                                {
                                    "role": "model",
                                    "parts": []
                                },
                            ])

                            convo.send_message("YOUR_USER_INPUT")
                            print(convo.last.text)

                    except Exception as e:
                        speak("Sorry sir, i am not able to find this...")



            elif "temperature" in query:
                search = "temperature in agarpara"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"current {search} is {temp}")





            elif "send text message" in query:
                speak("sir.. what should i say...")
                msz = takecommand()

                from twilio.rest import Client

                account_sid = 'AC9fe05ae4c6ada278d7f42b50b3108d26'
                auth_token = 'cba8ee71c3f365071e3ef72d902dc0ec'
                client = Client(account_sid, auth_token)

                message = client.messages \
                    .create(
                    body=msz,
                    from_='+18504177209',
                    to='+918167266006'
                )

                print(message.sid)
                speak("sir... message has been sent...")


            elif "make a phone call" in query:
                speak("sir.. wait a second...")

                from twilio.rest import Client

                account_sid = 'AC9fe05ae4c6ada278d7f42b50b3108d26'
                auth_token = 'cba8ee71c3f365071e3ef72d902dc0ec'
                client = Client(account_sid, auth_token)

                message = client.calls \
                    .create(
                    twiml='<Response><Say>This is testing message from personal assistant this side...</Say></Response>',
                    from_='+18504177209',
                    to='+918167266006'
                )

                print(message.sid)



            elif "shut down the system" in query:
                os.system("shutdown /s /t 5")
            elif "restart the system" in query:
                os.system("shutdown /r /t 5")
            elif "sleep the system" in query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")



            elif "what is" or "who is" or "details of" or "defination of" in query:
                speak('Searching....')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Me....")
                # print(results)
                speak(results)
            elif "jis university" or "university" in query:
                speak('Searching....')
                query = query.replace("wikipedia", "jis university in Agarpara")
                results = wikipedia.summary(query, sentences=5)
                speak("According to Me....")
                # print(results)
                speak(results)
            elif "jis college of engineering" in query:
                speak('Searching....')
                query = query.replace("wikipedia", "jis college of engineering in kalyani")
                results = wikipedia.summary(query, sentences=5)
                speak("According to Me....")
                # print(results)
                speak(results)

            speak("sir... Do you have any other work....")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        speak("Sorry, something went wrong. Please try again later.")

'''class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:\\Users\\SUVRODIP\\Downloads\\wallpaper\\ai-loader-opt.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout(self.showTime)
        timer.start(5000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
ai = Main()
ai.show()
sys.exit(app.exec_())'''

'''elif "make QR code" or "one more QR code" in query:
speak("wait a second sir...")
qr_code_function()
time.sleep(10)
pass'''
