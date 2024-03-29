import requests
import telebot
from telebot import types
import random
import os

runed = True #флаг на появление старта/стопа

bot = telebot.TeleBot('MeTeleBotToken')

@bot.message_handler(commands=['start'])
def button_message(message):
    global runed
    runed = True 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Аудио")
    item2 = types.KeyboardButton("Изображение")
    item3 = types.KeyboardButton("Репозиторий")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Выберите один из предложенных вариантов: фото, музыка, код, стоп', reply_markup=markup)

@bot.message_handler(commands=['stop'])
def button_message(message):
    global runed
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    runed = False 
    bot.send_message(message.chat.id, 'Бот остановлен', reply_markup=markup)
    #завершения работы бота

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if runed:
        if message.text.lower() == "изображение" or message.text.lower() == "фото":
            image = requests.get('https://api.thedogapi.com/v1/images/search')
            data = image.json()
            url = data[0]['url']
            bot.send_photo(message.chat.id, photo=url, caption="Милота подоспела 🥹🐶")
        elif message.text.lower() == "аудио" or message.text.lower() == "музыка":
            audio_files = os.listdir('output')
            if audio_files:
                # audio_file = random.choice(audio_files)
                # audio_path = os.path.join('output', audio_file)
                index = random.randrange(0, len(audio_files))
                audio_path = os.path.join('output', audio_files[index])
                audio = open(audio_path, 'rb') #режим открытия файла read binary
                bot.send_audio(message.chat.id, audio, timeout=3, caption="Музычка для рингтонов, наслаждайтесь 🎶")
                audio.close()
            else:
                bot.send_message(message.chat.id, 'В папке "output" нет аудиофайлов.')
        elif message.text.lower() == "репозиторий" or message.text.lower() == "код":
            bot.send_message(message.chat.id, 'https://github.com/axmedova01/telebot')

bot.polling(none_stop=True, interval=0)
