import config, telebot
from quick_response_code import QuickResponseCode

bot = telebot.TeleBot(config.BOT_API, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Hi! Input text or link and I generate QR code for you!')


@bot.message_handler(content_types=['text'])
def send_qr(message):
    qr = QuickResponseCode()
    qr.generate_qr_code(message)
    bot.send_photo(chat_id=message.chat.id, photo='qr_code/qr_code.png', caption=message)


if __name__ == '__main__':
    bot.infinity_polling()
