from vosk import KaldiRecognizer, Model, SetLogLevel
import json


RATE = 16000

SetLogLevel(-1)

class VoiceRecognizer:
    def __init__(self, rate):
        model = Model(r"../vosk_small_ru_updated")
        self.rec = KaldiRecognizer(model, rate)
        self.rec.SetWords(True)

    
    def recognize_frames(self, frames):
        result = ""
        for frame in frames:
            if len(frame) == 0:
                break
            
            elif not self.rec.AcceptWaveform(frame):
                result = self.rec.PartialResult()
                result = json.loads(result)["partial"]

        self.rec.Reset()

        return result