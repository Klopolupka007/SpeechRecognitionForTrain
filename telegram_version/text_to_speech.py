import time

import pyttsx3


class TextToSpeech():
    def __init__(self):
        self.engine = pyttsx3.init()


    def get_audio(self, text, answer_file):
        self.engine.save_to_file(text, answer_file)
        self.engine.runAndWait()