import speech_recognition as sr
from icecream import ic

def recognize_text(filename: str):
    ic("Starting recognizing")
    r = sr.Recognizer()
    audio_file = sr.AudioFile(filename)
    with audio_file as source:
        audio = r.record(source)
        text = r.recognize_google(audio, language="ru")
        ic("Finished recognition", text)
        return text