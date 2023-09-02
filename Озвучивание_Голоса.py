import pyttsx3

engine = pyttsx3.init()     # инициализация движка

# зададим свойства
engine.setProperty('rate', 180) # Скорость воспроизведения
engine.setProperty('volume', 1)   # громкость (0-1)

engine.say("Текущая скорость электропоезда – 60 км/ч")      # запись фразы в очередь

# очистка очереди и воспроизведение текста
engine.runAndWait()