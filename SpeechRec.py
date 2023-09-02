from vosk import Model, KaldiRecognizer

import json
import wave
import pyaudio

# read audio and convert from stereo mode to mono
from pydub import AudioSegment
sound = AudioSegment.from_wav("./audio/noisy/audio_1.wav")
sound = sound.set_channels(1)
sound.export("./audio/noisy_mono/audio_1_mono.wav", format="wav")

wf = wave.open(r'./audio/noisy_mono/audio_1_mono.wav', "rb")

results = ""
textResults = []


model = Model(r"vosk-model-small")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

while True:
    data = wf.readframes(8000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        recognizerResult = rec.Result()
        results = results + recognizerResult
        # convert the recognizerResult string into a dictionary
        resultDict = json.loads(recognizerResult)
        # save the 'text' value from the dictionary into a list
        textResults.append(resultDict.get("text", ""))

'''
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()
'''

# process "final" result
results = results + rec.FinalResult()
resultDict = json.loads(rec.FinalResult())
textResults.append(resultDict.get("text", ""))
print(textResults)

