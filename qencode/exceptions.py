class QencodeException(Exception):
    def __init__(self, message, *args):
        super(QencodeException, self).__init__(message, *args)
        self.error = message
        self.arg = [i for i in args]


class QencodeClientException(QencodeException):
    def __init__(self, message, *args):
        super(QencodeClientException, self).__init__(message, *args)


class QencodeTaskException(QencodeException):
    def __init__(self, message, *args):
        super(QencodeTaskException, self).__init__(message, *args)
