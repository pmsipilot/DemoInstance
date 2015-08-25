class DemoAuth:
    def __init__(self, config):
        raise NotImplementedError

    # Must return login if ok or False
    def check_auth(self, user, password):
        raise NotImplementedError

    def is_admin(self, user):
        return False
