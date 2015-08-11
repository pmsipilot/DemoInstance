# -*- coding: utf-8 -*-
import smtplib
import logging
import re
from demo_exception import DemoExceptionInvalidEmail


class DemoMail():
    def __init__(self, host, port=25, from_mail='demoinstance@localhost',
                 user=None, password=None, tls=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.from_mail = from_mail
        self.tls = tls

    def connect(self):
        logging.debug('Connection SMTP : %s on %s', self.host, self.port)
        smtp_server = smtplib.SMTP(self.host, self.port)
        smtp_server.ehlo()
        if self.tls:
            logging.debug('Connection SMTP SSL')
            smtp_server.starttls()
            smtp_server.ehlo()
        logging.debug('User:%s', self.user)
        smtp_server.login(self.user, self.password)
        return smtp_server

    def send_token_mail(self, mail, token, url):
        logging.debug('Send token mail to %s with token %s', mail, token)
        # Email is valid
        if not DemoMail.check_email(mail):
            raise DemoExceptionInvalidEmail(mail)

        header = str('To:' + mail + '\n' +
                     'From: ' + self.from_mail + '\n' +
                     'Subject:testing \n')
        body = self.get_token_mail_body(token, url)
        msg = header + '\n' + body + '\n\n'
        smtp_server = self.connect()
        smtp_server.sendmail(self.user, mail, msg)
        smtp_server.close()

    def get_token_mail_body(self, token, url):
        body = "Bonjour\n" \
               "Voici le lien qui vous permettra"\
               "d'accéder à vos instances de démonstrations\n"\
               + url + "#/login/" + token.encode("utf-8")
        return body

    @staticmethod
    def check_email(email):
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(pattern, email):
            return True
        return False
