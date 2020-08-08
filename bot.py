import os

import telebot
from telebot import types

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


@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultPhoto(id='1',
                                         photo_url='https://lh3.googleusercontent.com/proxy'
                                                   '/bzmuSZlyE6zF3bdR6Rgi03mk3C09HfjId5Cq_qzojEfFb1N4H'
                                                   '-TSrwnYMORc68msvC_Oa_IQAYFx3_TgiU-1UpxgOJpBxcRAKpO-sz4',
                                         thumb_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fforum.f1news.ru'
                                                   '%2Ftopic%2F67672-lukoil-racing-team%2F%3Fpage%3D3&psig'
                                                   '=AOvVaw24atOlyR2u1g4M5p99hSL9&ust=1596992218721000&source=images'
                                                   '&cd=vfe&ved=0CAIQjRxqFwoTCKDK3-GJjOsCFQAAAAAdAAAAABAD '
                                         )
        bot.answer_inline_query(inline_query.id, r)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    bot.infinity_polling()
