import re
import speech_recognition as sr
import pyaudio
import os
import fnmatch
import random
from PIL import Image

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Rozpocznij mówienie...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

        try:
            print("Rozpoznawanie...")
            #text = "Adam Jankowiak"
            #print("Rozpoznano: {}".format(text))
            #return text
            # TUTAJ
            text = recognizer.recognize_google(audio, language="pl-PL")
            print("Rozpoznano: {}".format(text))
            return text
        except sr.UnknownValueError:
            print("Nie rozpoznano mowy")
            return None
        except sr.RequestError as e:
            print("Błąd podczas żądania do Google Speech Recognition service; {0}".format(e))
            return None


def find_similar_files(directory, search_string):

    matching_files = []

    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return matching_files

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if fnmatch.fnmatch(file_name, f"*{search_string}*"):
                matching_files.append(os.path.join(root, file_name))

    if matching_files:
        random_file = random.choice(matching_files)
        return random_file

    return None

def display_image(image_path):
    try:
        img = Image.open(image_path)
        img.show()
    except Exception as e:
        print(f"Error displaying image: {e}")

def get_photo_speech(text, directory_to_search):
    result = find_similar_files(directory_to_search, text)
    return result


