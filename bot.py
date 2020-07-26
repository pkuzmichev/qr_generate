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


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    try:
        qr = QuickResponseCode()
        qr.generate_qr_code(query)
        with open('qr_code/qr_code.png', 'rb') as f:
            contents = f.read()
        r_sum = types.InlineQueryResultArticle(
            id='1', title='Create QR Code',
            description='Input text or link and I generate QR code for you!',
            input_message_content=types.InputMediaPhoto(
                media=contents,
                caption=query
            )
        )
        bot.answer_inline_query(query.id, [r_sum], cache_time=2147483646)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


if __name__ == '__main__':
    bot.infinity_polling()
