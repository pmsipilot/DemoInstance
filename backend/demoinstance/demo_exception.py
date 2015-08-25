class DemoException(Exception):
    def __init__(self):
        self.value = "ERROR DEMO"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionBadConfigValue(DemoException):
    def __init__(self, config, value):
        self.value = "Bad config value for %s : %s" % (config, value)
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionToMuchInstanceImage(DemoException):
    def __init__(self):
        self.value = "To much instances"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionInstanceNotFound(DemoException):
    def __init__(self):
        self.value = "Instance not found"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionUserAlreadyHaveInstanceImage(DemoException):
    def __init__(self):
        self.value = "User Already have instance"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionInvalidEmail(DemoException):
    def __init__(self, email):
        self.value = "Email is invalid : %s" % email
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionInvalidImage(Exception):
    def __init__(self, image_var):
        self.value = "Image Invalid %s" % image_var
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionInvalidImageTime(Exception):
    def __init__(self, time):
        self.value = "Invalid Time %s" % time
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionInvalidOwner(Exception):
    def __init__(self):
        self.value = "Invalid Owner"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionUserInstanceTypeAlreadyExist(Exception):
    def __init__(self, time):
        self.value = "User already have an instance of this type"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionNonUpdatableInstance(Exception):
    def __init__(self):
        self.value = "You can't update this instance"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionUserTokenInvalid(Exception):
    def __init__(self, time):
        self.value = "User token is invalid"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionErrorAuth(Exception):
    def __init__(self):
        self.value = "Invalid user/password"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionConfigNotFound(Exception):
    def __init__(self):
        self.value = "Invalid config file"
        self.message = self.value

    def __str__(self):
        return repr(self.value)
