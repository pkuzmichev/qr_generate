import unittest
from pathlib import Path

from ddt import ddt, data

from quick_response_code import QuickResponseCode


@ddt
class TestQuickResponseCode(unittest.TestCase):

    @data('', 'https://www.youtube.com', 'кек', 'kek', '/start')
    def test_create_qr_code(self, value):
        qr_code = QuickResponseCode()
        qr_code.generate_qr_code(value, '../qr_code/qr_code.png')

        my_file = Path('../qr_code/qr_code.png')
        self.assertTrue(my_file.is_file(), 'file with qr code was no created')


if __name__ == '__main__':
    unittest.main()
