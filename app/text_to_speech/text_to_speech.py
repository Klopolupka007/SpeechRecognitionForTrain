import pyttsx3


class TextToSpeech():
    def __init__(self):
        self.AUDIO_TEMP_FILE = "./text_to_speech/answer_temp.wav"
        self.engine = pyttsx3.init()

    def get_audio(self, text):
        self.engine.save_to_file(text, self.AUDIO_TEMP_FILE)
        self.engine.runAndWait()
        return self.AUDIO_TEMP_FILE