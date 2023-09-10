import requests
import time

class QuestionAnswerer:
    def get_question_and_answer(self, question: str, context, train_model:str):
        question = f"Нахожусь в вагоне {train_model}, возник вопрос: {question}"
        context.append(question)
        try:
            t1 = time.time()
            res = requests.post("http://127.0.0.1:5130/model", json={"dialog_history": context})
            print(time.time() - t1)
            if (not res.json()):
                answer = "Хм, мне не удалось найти ответ. Похоже, один из моих компонентов вышел из строя."
            else:
                answer = res.json()["response"]
        except Exception:
            answer = "Хм, мне не удалось найти ответ. Похоже, один из моих компонентов вышел из строя."
            
        return question, answer