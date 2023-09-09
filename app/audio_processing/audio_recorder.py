import pyaudio
import sounddevice as sd


RATE = 16000
RECORD_SECONDS = 5

class AudioRecorder:
    def __init__(self, rate, max_record_seconds):
        self.CHANNELS = 1
        self.FORMAT = pyaudio.paInt16
        
        self.CHUNK = 1024
        self.rate = rate
        self.max_record_seconds = max_record_seconds
        
        self.is_recording = False

    
    def start_recording(self):
        p = pyaudio.PyAudio()

        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        frames = []
        self.is_recording = True

        while self.is_recording:
            data = stream.read(self.CHUNK)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        return frames
    
    
    def stop_recording(self):
        self.is_recording = False