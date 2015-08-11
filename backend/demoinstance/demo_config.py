import ConfigParser
import os
from copy import copy
from demo_exception import *

IMAGE_CONF_PREFIX = 'IMAGE_'
IMAGE_INT_PARAM = [
    'time_default', 'max_instance', 'time_max', 'time_default', 'pool'
]


class DemoConfig():
    config_file = './config.ini'

    def __init__(self):
        if not os.path.isfile(DemoConfig.config_file):
            raise DemoExceptionConfigNotFound()
        self.config = ConfigParser.ConfigParser()
        self.config.read(DemoConfig.config_file)

        # Default
        self.log_level = self.config.get("DEFAULT", "log_level")
        self.security_type = self.config.get("DEFAULT", "security_type")
        if self.security_type not in ('open', 'email')\
                and not self.security_type.startswith('auth_'):
            raise DemoExceptionBadConfigValue(
                'security_type',
                self.security_type
            )
        self.provider = self.config.get("DEFAULT", "provider")

        if self.config.has_option("DEFAULT", "dev"):
            self.dev = self.config.getboolean("DEFAULT", "dev")
        else:
            self.dev = False

        # HTTP
        self.http_port = self.config.getint("HTTP", "port")

        # Database
        self.database_connection = self.config.get("DATABASE", "connection")

        # EMAIL CONF
        if self.security_type == 'email':
            self.mail_host = self.config.get("MAIL", "host")
            if self.config.has_option("MAIL", "port"):
                self.mail_port = self.config.getint("MAIL", "port")
            else:
                self.mail_port = 25

            if self.config.has_option("MAIL", "from"):
                self.mail_from = self.config.get("MAIL", "from")
            else:
                self.mail_from = 'demoinstance@localhost'

            if self.config.has_option("MAIL", "user"):
                self.mail_user = self.config.get("MAIL", "user")
            else:
                self.mail_user = None

            if self.config.has_option("MAIL", "password"):
                self.mail_password = self.config.get("MAIL", "password")
            else:
                self.mail_password = None

            if self.config.has_option("MAIL", "tls"):
                self.mail_tls = self.config.getboolean("MAIL", "tls")
            else:
                self.mail_tls = False

        # Auth Conf
        if self.security_type.startswith('auth_'):
            self.auth = {}
            section = self.security_type.upper()
            if self.config.has_section(section):
                for name, value in self.config.items(section):
                    self.auth[name] = value

        # Prov Conf
        self.provider_data = {}
        section = 'PROV_'+self.provider.upper()
        if self.config.has_section(section):
            for name, value in self.config.items(section):
                self.provider_data[name] = value

        # IMAGE CONF
        self.images = {}
        template_image = self.get_image_by_section('IMAGE')
        for section in self.config.sections():
            if not section.startswith(IMAGE_CONF_PREFIX):
                continue
            image = self.get_image_by_section(
                section,
                template_image=template_image
            )
            key_name = section[len(IMAGE_CONF_PREFIX):]
            self.check_image(image)
            self.images[key_name] = image

    def get_image_by_section(self, section, template_image=None):
        if template_image is None:
            image = {'img': ''}
        else:
            image = copy(template_image)
        for name, value in self.config.items(section):
            if name in IMAGE_INT_PARAM:
                value = int(value)
            image[name] = value
        return image

    def check_image(self, image):
        if 'name' not in image:
            raise DemoExceptionInvalidImage('name')
        if 'soft_url' not in image:
            raise DemoExceptionInvalidImage('soft_url')
        if 'time_default' not in image:
            raise DemoExceptionInvalidImage('time_default')
        return True
