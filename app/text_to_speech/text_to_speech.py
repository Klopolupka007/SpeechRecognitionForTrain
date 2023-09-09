import os
import torch


class TextToSpeech():
    def __init__(self):
        self.AUDIO_TEMP_FILE = "./text_to_speech/answer_temp.wav"
        self.LOCAL_FILE = './text_to_speech/model.pt'
        if not os.path.isfile(self.LOCAL_FILE):
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt', self.LOCAL_FILE)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.SAMPLE_RATE = 8000
        self.SPEAKER = 'aidar'
        self.PUT_ACCENT=False
        self.PUT_YO=True

        self.model = torch.package.PackageImporter(self.LOCAL_FILE).load_pickle("tts_models", "model")
        self.model.to(device)


    def get_audio(self, text):
        answer_path = self.model.save_wav(
            text=text,
            speaker=self.SPEAKER,
            sample_rate=self.SAMPLE_RATE,
            audio_path=self.AUDIO_TEMP_FILE,
            put_accent=self.PUT_ACCENT
        )
        return answer_path