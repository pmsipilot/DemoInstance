# coding=utf-8
from auth import DemoAuth


class AuthFake(DemoAuth):
    def __init__(self, config):
        self.config = config
        users = self.config['user'].split(',')
        self.users = {}
        for users_info in users:
            user_info = users_info.split(':')
            self.users[user_info[0]] = user_info[1]

    def check_auth(self, user, password):
        if user in self.users:
            if password == self.users[user]:
                return user
        return False

    def is_admin(self, user):
        if user in self.config['admin'].split(','):
            return True
        return False
