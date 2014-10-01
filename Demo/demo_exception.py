class DemoException(Exception):
    def __init__(self):
        self.value = "ERROR DEMO"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionToMuchInstance(DemoException):
    def __init__(self):
        self.value = "To much instances"
        self.message = self.value

    def __str__(self):
        return repr(self.value)

class DemoExceptionInvalidImage(Exception):
    def __init__(self,image_var):
        self.value = "Image Invalid %s" % image_var
        self.message = self.value

    def __str__(self):
        return repr(self.value)
