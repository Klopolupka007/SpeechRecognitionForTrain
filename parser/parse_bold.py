import re
import docx

# Открываем документ
doc = docx.Document('tech.docx')

bold_words = []

for paragraph in doc.paragraphs:
    for run in paragraph.runs:
        if run.bold:
            bold_words.append(run.text)

words = [word.split() for word in bold_words]

# Создание плоского списка и уникализация
flat_list = list(set([item for sublist in words for item in sublist]))
with open('terms.txt', 'w', encoding='utf-8') as file:
    for i in flat_list:
        file.write(i + '\n')

print(flat_list)
