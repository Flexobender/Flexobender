# -*- coding: utf-8 -*-
import telebot
from transitions import Machine


TOKEN = '2100387942:AAH4g9wkTGYvLKmoXa-FY8zT_bJM1Y-gw6E'
bot = telebot.TeleBot(token=TOKEN)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
