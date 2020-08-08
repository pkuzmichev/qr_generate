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


def inline_cached_photo(update, context):
    qr = QuickResponseCode()

    query = update.inline_query.query
    qr.generate_qr_code(query)

    if query:
        info_photo = bot.send_photo(chat_id='1158323636', photo=open('qr_code/qr_code.png.png', 'rb'), caption=query)
        thumb_photo = info_photo['photo'][0]['file_id']
        original_photo = info_photo['photo'][-1]['file_id']
        results = [
            InlineQueryResultCachedPhoto(
                id=uuid4(),
                title=query,
                photo_file_id=original_photo,)
            ]
        update.inline_query.answer(results)


if __name__ == '__main__':
    bot.infinity_polling()
