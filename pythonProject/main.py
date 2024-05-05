import telebot
from telebot import types
import os
import pickle
# from PIL import Image
import arduino as ar
import time

token='6593393824:AAG4Q2W_KycnBpSYh4QYy8jWUbswqkuNKFk'
bot=telebot.TeleBot(token)

full_dir = os.path.abspath('voltage.dat')
with open(full_dir, 'rb') as filehandle:
    voltage = pickle.load(filehandle)

def create_markup(message, msg, texts, callbacks, rw=3, edit=False, markup_=True):
    markup = types.InlineKeyboardMarkup(row_width=rw)
    for i in range(len(texts)):
        item = types.InlineKeyboardButton(text=texts[i], callback_data=str(callbacks[i]))
        markup.add(item)
    print(edit)
    print(markup_)
    if edit == False:
        bot.send_message(message.chat.id, msg, reply_markup=markup)
    elif edit == True and markup_ == True:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=msg, reply_markup=markup)
    elif edit == True and markup_ == False:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=msg, reply_markup=markup)
    else:
        print('f')

@bot.message_handler(commands=['start'])
def button_message(message):
    create_markup(message, 'Приветствуем в боте!', ['Меню', 'Настройки'], ['меню','настройки'], rw = 1)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global voltage
    if call.data == 'меню':
        create_markup(call.message, 'Запуск и выключение электрофитнеса', ['Старт', 'Настройки'],['старт', 'настройки'], rw = 1)

    if call.data == 'настройки':
        A = 'Настройки подачи питания\nНапряжение нужно указать в диапазоне от 20 до 90 Вольт\nТекушее напряжение: '+ str(voltage)
        create_markup(call.message, A,
        ["+1 Вольт", '-1 Вольт', 'меню'], ['вольт+', 'вольт-', 'меню'], rw=2)

    if call.data == 'старт':
        ar.start()
        create_markup(call.message, 'Запуск и выключение электрофитнеса', ['Стоп', 'Настройки'], ['стоп', 'настройки'], rw = 1, edit=True)

    if call.data == 'стоп':
        ar.stop()
        create_markup(call.message, 'Запуск и выключение электрофитнеса', ['Старт', 'Настройки'],['старт', 'настройки'], rw = 1, edit=True)

    if call.data == 'вольт+':
        voltage += 1
        with open(full_dir, 'wb') as filehandle:
            pickle.dump(voltage, filehandle)
        create_markup(call.message,
                      'Настройки подачи питания\nНапряжение нужно указать в диапазоне от 20 до 90 Вольт\nТекушее напряжение: ' + str(voltage),
                      ["+1 Вольт", '-1 Вольт', 'меню'], ['вольт+', 'вольт-', 'меню'], rw=2, edit=True)

    if call.data == 'вольт-':
        voltage -= 1
        with open(full_dir, 'wb') as filehandle:
            pickle.dump(voltage, filehandle)
        create_markup(call.message,
                      'Настройки подачи питания\nНапряжение нужно указать в диапазоне от 20 до 90 Вольт\nТекушее напряжение: ' + str(voltage)/,
                      ["+1 Вольт", '-1 Вольт', 'меню'], ['вольт+', 'вольт-', 'меню'], rw=2, edit=True)

while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(1)