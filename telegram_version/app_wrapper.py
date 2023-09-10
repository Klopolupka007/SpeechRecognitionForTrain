import sys

import pyaudio

sys.path.insert(1, 'app')

from question_answerer import QuestionAnswerer
from voice_recognizer import VoiceRecognizer
from text_to_speech import TextToSpeech


class AppWrapper:
    def __init__(self):
        self.voice_recognizer = VoiceRecognizer(16000)
        self.question_answerer = QuestionAnswerer()
        self.text_to_speech = TextToSpeech()
    
    def get_question_and_answer(self, fname: str, train_model: str, context):
        recognized_question = self.voice_recognizer.recognize_frames(fname)
        recognized_question, answer = self.question_answerer.get_question_and_answer(recognized_question, context, train_model)
        answer_filename = fname[:-4]+"_answer.wav"
        self.text_to_speech.get_audio(answer, answer_filename)
        
        return recognized_question, answer, answer_filename
    


class AppWrapperTextOnly:
    def __init__(self):
        self.voice_recognizer = VoiceRecognizer(16000)
        self.question_answerer = QuestionAnswerer()
        self.text_to_speech = TextToSpeech()
    
    def get_question_and_answer(self, question: str, fname: str, train_model: str, context):
        question, answer = self.question_answerer.get_question_and_answer(question, context, train_model)
        answer_filename = fname + "_answer.wav"
        self.text_to_speech.get_audio(answer, answer_filename)
        
        return question, answer, answer_filename
        