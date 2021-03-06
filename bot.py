import json
import os
from uuid import uuid4

import telebot
from telebot import types
from telebot.types import InlineQueryResultCachedPhoto

from quick_response_code import QuickResponseCode

bot = telebot.TeleBot(os.environ.get('BOT_API'), parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Hi! Input text or link and I generate QR code for you!')


@bot.message_handler(content_types=['text', 'photo'])
def send_qr(message):
    qr = QuickResponseCode()
    qr.generate_qr_code(message.text)
    with open('qr_code/qr_code.png', 'rb') as f:
        contents = f.read()
        bot.send_photo(chat_id=message.chat.id, photo=contents, caption=message.text)


@bot.inline_handler(func=lambda query: True)
def inline_cached_photo(query):
    global info_photo, empty_photo
    qr = QuickResponseCode()

    if query.query:
        qr.generate_qr_code(query.query)
        info_photo = bot.send_photo(chat_id=query.from_user.id,
                                    photo=open('qr_code/qr_code.png', 'rb'),
                                    caption=query.query)
        results = [
            InlineQueryResultCachedPhoto(
                id='1',
                title=query.query,
                photo_file_id=info_photo.json['photo'][0]['file_id'])
        ]
        bot.answer_inline_query(query.id, results)

    else:
        empty_photo = bot.send_photo(chat_id=query.from_user.id,
                                     photo=open('qr_code/empty.png', 'rb'),
                                     caption=query.query)
        empty_results = [
            InlineQueryResultCachedPhoto(
                id='2',
                title=query.query,
                photo_file_id=empty_photo.json['photo'][0]['file_id'])
        ]
        bot.answer_inline_query(query.id, empty_results)


@bot.channel_post_handler(commands=["getchannelid"])
def chat_id(message):
    bot.reply_to(message, 'channel_id = {!s}'.format(message.chat.id))


if __name__ == '__main__':
    bot.infinity_polling()
