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


# @bot.inline_handler(func=lambda query: len(query.query) > 0)
# # def query_text(query):
# #     hint = 'Input text or link and I generate QR code for you!'
# #     r = types.InlineQueryResultArticle(
# #         id='1',
# #         title='QR Bot',
# #         description=hint,
# #         input_message_content=types.InputTextMessageContent(
# #             message_text='No data :('
# #         )
# #     )
# #     bot.answer_inline_query(query.id, [r])


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    # try:
    # matches = re.match(digits_pattern, query.query)
    # Вылавливаем ошибку, если вдруг юзер ввёл чушь
    # или задумался после ввода первого числа
    # except AttributeError as ex:
    #     return
    # В этом месте мы уже уверены, что всё хорошо,
    # поэтому достаем числа
    # num1, num2 = matches.group().split()
    try:
        # m_sum = int(num1) + int(num2)
        qr = QuickResponseCode()
        qr.generate_qr_code(query.query)
        with open('qr_code/qr_code.png', 'rb') as f:
            contents = f.read()
        r_sum = types.InlineQueryResultArticle(
            id='1', title='Create QR Code',
            # Описание отображается в подсказке,
            # message_text - то, что будет отправлено в виде сообщения
            description='Input text or link and I generate QR code for you!',
            input_message_content=types.InputMediaPhoto(
                media=contents
            )
            # Указываем ссылку на превью и его размеры
        )
        # Учтем деление на ноль и подготовим 2 варианта развития событий

        # В нашем случае, результаты вычислений не изменятся даже через долгие годы, НО!
        # если где-то допущена ошибка и cache_time уже выставлен большим, то это уже никак не исправить (наверное)
        # Для справки: 2147483646 секунд - это 68 с копейками лет :)
        bot.answer_inline_query(query.id, [r_sum], cache_time=2147483646)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


if __name__ == '__main__':
    bot.infinity_polling()
