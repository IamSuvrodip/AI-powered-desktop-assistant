import speech_recognition as sr
import pyttsx3

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = "open ai key"

import openai
openai.api_key = OPENAI_KEY

def SpekText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
r = sr.Recognizer()
def record_text():
    while(1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("listenig..")

                audio2 = r.listen(source2)

                MyText = r.recognize_google(audio2)

                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")


def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=100, # 256
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


messages = [{"role": "user", "content": "Please act like jarvis from Iron man."}]
while (1):
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    SpekText(response)
    print(response)