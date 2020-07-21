import qrcode
import logging


class QuickResponseCode:

    def generate_qr_code(self, data='kek', path='qr_code/qr_code.png'):
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        logging.info('qr_code init')

        qr_code.add_data(data)
        logging.info('qr_code add data')

        qr_code.make(fit=True)

        img = qr_code.make_image(fill_color="black", back_color="white")
        logging.info('qr_code make image')
        img.save(path)
        logging.info('qr_code save image to qr_code/qr_code.png')
