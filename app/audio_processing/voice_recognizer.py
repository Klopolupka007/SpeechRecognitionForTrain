from vosk import KaldiRecognizer, Model, SetLogLevel
import json


RATE = 16000

SetLogLevel(-1)

class VoiceRecognizer:
    def __init__(self, rate):
        model = Model(r"../vosk_small_ru_updated")
        self.rec = KaldiRecognizer(model, rate)
        self.rec.SetWords(True)


    def __process_text(self, text):
        with open('../map_1.json', 'r', encoding="utf-8") as fp:
            abbr_map = json.load(fp)
            
        text = text.split()
        result = ""
        for i, word in enumerate(text):
            word = word.strip()
            if (word in abbr_map.keys()):
                word = abbr_map[word]
            result += word + " "
                
        return result.rstrip()

    
    def recognize_frames(self, frames):
        result = ""
        for frame in frames:
            if len(frame) == 0:
                break
            
            elif not self.rec.AcceptWaveform(frame):
                result = self.rec.PartialResult()
                result = json.loads(result)["partial"]

        self.rec.Reset()
        
        result = self.__process_text(str(result))

        return result