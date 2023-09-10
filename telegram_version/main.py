import os
import subprocess
from dataclasses import dataclass

import telebot
from app_wrapper import AppWrapper, AppWrapperTextOnly
from telebot import types
from users_dialogue_datamodule import UsersDialogueModel
from users_train_datamodel import UsersTrainDataModel

TOKEN = "6616731554:AAHYGpqdTs0Om546J-47ZCNaoIs8MZ-fAaM"
bot = telebot.TeleBot(TOKEN)


user_train_input_required = []
user_wants_to_set_train = []

func_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Выбрать поезд")
item2 = types.KeyboardButton("Список моделей поездов")
func_menu_markup.add(item1)
func_menu_markup.add(item2)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Вас приветствует интеллектуальный ассистент машиниста!")
    bot.send_message(message.chat.id, "Напишите модель поезда, после чего начните общение с ботом голосовыми сообщениями.", reply_markup=func_menu_markup)
    

@bot.message_handler(content_types=['voice'])
def message_reply(message):
    chat_id_str = message.chat.id
    
    users_train_data_model = UsersTrainDataModel()
    train_model = users_train_data_model.get_current_train_of_user(chat_id_str)
    if (not train_model):
        user_train_input_required.append(chat_id_str)
        bot.send_message(message.chat.id, "Нет информации о вашем поезде. Введите название модели поезда.", reply_markup=func_menu_markup)
        return
        
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    out_fname = f'./telegram_version/original_voice_message{chat_id_str}.ogg'
    out_fname_wav = f'./telegram_version/prepared_voice_message{chat_id_str}.wav'
    
    with open(out_fname, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    process = subprocess.run(['ffmpeg', '-y', '-i', out_fname, '-ac', '1', '-ar', "16000", '-acodec', "pcm_s16le", out_fname_wav], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if process.returncode != 0:
        raise Exception("Something went wrong")
    
    users_dialogue_model = UsersDialogueModel()
    context_of_user = get_context(users_dialogue_model.get_dialogue(chat_id_str))
    recognized_question, answer, answer_file = app_wrapper.get_question_and_answer(out_fname_wav, train_model, context_of_user)
    users_dialogue_model.insert_qa(chat_id_str, recognized_question, answer)
    
    os.remove(out_fname)
    os.remove(out_fname_wav)
    
    print(f"User #{chat_id_str} says: {recognized_question}")
    print(f"The answer for user #{chat_id_str} is: {answer}")
    
    bot.send_message(message.chat.id, "Вы сказали: " + recognized_question, reply_markup=func_menu_markup)
    bot.send_message(message.chat.id, answer, reply_markup=func_menu_markup)
    with open(answer_file, 'rb') as voice:
        bot.send_voice(message.chat.id, voice)
    
    os.remove(answer_file)
    

@bot.message_handler(content_types=['text'])
def message_reply(message):
    chat_id_str = message.chat.id
    message_text = message.text.strip()
    
    if (message_text == "Список моделей поездов"):
        bot.send_message(message.chat.id, "\n".join(train_names), reply_markup=func_menu_markup)
        return
    
    elif (message_text == "Выбрать поезд"):
        user_wants_to_set_train.append(chat_id_str)
        bot.send_message(message.chat.id, "Хорошо, введите название модели поезда", reply_markup=func_menu_markup)
        return
    
    users_train_data_model = UsersTrainDataModel()
    is_user_exists = users_train_data_model.is_user_exists(chat_id_str)
    print("User exsists?", is_user_exists)
    
    print(user_train_input_required)
    
    if (chat_id_str in user_train_input_required or chat_id_str in user_wants_to_set_train):
        print(message_text not in train_names)
        
        if (message_text not in train_names):
            bot.send_message(message.chat.id, "Хм, не похоже на название поезда", reply_markup=func_menu_markup)
            
        else:
            users_train_data_model = UsersTrainDataModel()
            users_train_data_model.insert_train(chat_id_str, message_text)
            
            if (chat_id_str in user_train_input_required):
                user_train_input_required.remove(chat_id_str)
            
            if (chat_id_str in user_wants_to_set_train):
                user_wants_to_set_train.remove(chat_id_str)
            bot.send_message(message.chat.id, f"Отлично! Ваш поезд - {message_text}.\nЕсли захотите поменять модель поезда - нажмите на кнопку \"Выбор модели поезда\"", reply_markup=func_menu_markup)
            
            users_dialogue_model = UsersDialogueModel()
            users_dialogue_model.clear_dialogue(chat_id_str)
    
    elif not is_user_exists:
        user_train_input_required.append(chat_id_str)
        bot.send_message(message.chat.id, "Кажется, вы еще не выбирали модель поезда, напишите модель поезда", reply_markup=func_menu_markup)
            
    else:
        users_train_data_model = UsersTrainDataModel()
        train_model = users_train_data_model.get_current_train_of_user(chat_id_str)
        out_fname = f'./telegram_version/original_voice_message{chat_id_str}'
        app_wrapper_txt_only = AppWrapperTextOnly()
        
        users_dialogue_model = UsersDialogueModel()
        context_of_user = get_context(users_dialogue_model.get_dialogue(chat_id_str))
        
        question, answer, answer_file = app_wrapper_txt_only.get_question_and_answer(message_text, out_fname, train_model, context_of_user)
        print(f"User #{chat_id_str} says: {message_text}")
        print(f"The answer for user #{chat_id_str} is: {answer}")
        print(f"Context of user #{chat_id_str} is: {context_of_user}")
        
        users_dialogue_model.insert_qa(chat_id_str, question, answer)
    
        bot.send_message(message.chat.id, answer, reply_markup=func_menu_markup)
        with open(answer_file, 'rb') as voice:
            bot.send_voice(message.chat.id, voice)
    
        os.remove(answer_file)
        #bot.send_message(message.chat.id, f"Отправьте голосовое сообщение, мне будет приятно услышать Ваш голос =)", reply_markup=func_menu_markup)
        

def get_context(list_of_rows):
    res = []
    for item in list_of_rows:
        res.extend([item.question, item.answer])
        
    return res


if __name__ == "__main__":
    train_names = ['2М62', '2М62У', '2ТЭ10М', '2ТЭ10МК', '2ТЭ10У', '2ТЭ10УК', '2ТЭ25А', '2ТЭ25КМ', '2ТЭ70', '2ТЭ116', '2ТЭ116УД', '2ЭС4К', '2ЭС5К', '3ЭС5К', '2ЭС6', '2ЭС7', '2ЭС10', 'ВЛ10', 'ВЛ10У', 'ВЛ10К', 'ВЛ11', 'ВЛ11М', 'ВЛ11М', 'ВЛ15', 'ВЛ65', 'ВЛ80Р', 'ВЛ80С', 'ВЛ80Т', 'ВЛ85', 'ТЭМ2', 'ТЭМ7А', 'ТЭМ14', 'ТЭМ18Д', 'ТЭМ18ДМ', 'ТЭП70', 'ТЭП70БС', 'ЧМЭ3', 'ЧС2', 'ЧС2К', 'ЧС2Т', 'ЧС4Т', 'ЧС6', 'ЧС200', 'ЧС7', 'ЧС8', 'ЭП1', 'ЭП1М', 'ЭП2К', 'ЭП10', 'ЭП20']
    app_wrapper = AppWrapper()
    bot.infinity_polling()