import logging
import requests

from django.conf import settings


class WEBSMS(object):
    """Сервис по отправке смс."""

    def __init__(self):
        self.username = settings.WEBSMS_LOGIN
        self.password = settings.WEBSMS_PASSWORD
        self.from_name = "Granelle"
        self.url = settings.WEBSMS_BASE_URL

    def send_sms(self, phone, message):
        if self.username == '' or self.password == '':
            logging.exception('Login or password is empty')
            return False
        elif message == '':
            logging.exception('You cannot send empty message')
            return False
        elif phone == '':
            logging.exception('Non-empty list of recipients requires')
            return False
        else:
            message = message.encode('windows-1251')
            params = {
                'http_username': self.username,
                'http_password': self.password,
                'fromPhone': self.from_name,
                'Message': message,
                'Phone_list': phone,
                'format': 'XML',
                'mode': 'SMS',
            }
            requests.get(self.url, params=params)
