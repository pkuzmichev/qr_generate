import json
import os
import telebot
import requests
from telebot import types
from telebot.types import InlineQueryResultPhoto

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
def query_text(query):
    try:
        qr = QuickResponseCode()
        qr.generate_qr_code(query.query)

        url = 'https://api.telegram.org/bot' + os.environ.get('BOT_API') + '/sendPhoto'
        #  'description': 'Bad Request: chat_id is empty

        files = {'photo': open('qr_code/qr_code.png', 'rb')}

        print('!!! query: ' + str(query))

        print('!!! CHAT ID: ' + str(query.from_user.id))

        data = {'chat_id': str(query.from_user.id)}

        print('!!! data: ' + str(data))

        r = requests.post(url, files=files, data=data)

        print('!!! r: ' + str(r.text))

        # KEK {'ok': False, 'error_code': 400, 'description': 'Bad Request: chat not found'}
        # print('KEK ' + str(r.json()))

        # with open('qr_code/qr_code.png', 'rb') as f:
        #     contents = f.read()

        payload = json.loads(r.text)

        print(str(payload['result']['photo'][0]['file_id']))

        r_sum = InlineQueryResultPhoto(
            id='1', title='Create QR Code',
            description='Input text or link and I generate QR code for you!',
            # photo_file_id='AgACAgIAAxkDAAIHlF8m83tslnW8zlGk_w3oUmFxYQpoAAIkrzEbWwEpScLfCFpWghZoUx_rkS4AAwEAAwIAA20AA_oaBQABGgQ',
            photo_url='https://www.kek.jp/ja/media/KEKLogo01.png',
            thumb_url='https://i.pinimg.com/originals/60/77/0d/60770d776e885f077e898dae54132b66.jpg'
        )

        bot.answer_inline_query(query.id, r_sum)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


if __name__ == '__main__':
    bot.infinity_polling()
