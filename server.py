from flask import Flask, send_file, request, render_template, send_from_directory

from bot import bot
from quick_response_code import QuickResponseCode

app = Flask(__name__,
            static_url_path='',
            static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/qr', methods=['GET', 'POST'])
def qr_code_generate():
    data = ''
    if request.method == 'POST':
        data = request.form.get('data')

        qr_code = QuickResponseCode()
        qr_code.generate_qr_code(data)

        return send_from_directory('qr_code', 'qr_code.png')


if __name__ == '__main__':
    app.run(port=8000)
    bot.infinity_polling()
