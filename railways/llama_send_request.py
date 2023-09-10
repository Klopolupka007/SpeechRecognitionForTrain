import requests

def llama_request(dialog_history, retrieved_line):

    if len(retrieved_line) == 4:
        fault = retrieved_line[1]
        cause = retrieved_line[2]
        solution = retrieved_line[3]
    else:
        fault=""
        cause=""
        solution=""

    res = requests.post(
        "http://127.0.0.1:8129/model",
        json={"dialog_history": dialog_history, "fault": fault, "cause": cause, "solution": solution}
    )
    if res.status_code == 200:
        return res.json()["response"]
    return ""


dialog_history = ["В вагоне 2М62У, я нажимаю кнопку “Пуск дизеля”, а у меня маслопрокачивающий насос не работает.",
                  'Если вы заметили, что предохранитель на 125 А в цепи "ЭД" перегорел, то необходимо заменить его. '
                  "Это поможет устранить неисправность и обеспечит безопасную работу вашей электронной системы.",
                  "В вагоне 2М62У, заметил, что шток у сервомотора не передвигается, а рейки топливных насосов остаются на нулевой подаче"]

res = llama_request(dialog_history, [])
print(res)