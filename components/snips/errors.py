class FormatError(Exception):
    """
    Exception raised when a string doesn't match the command format
    """

    def __init__(self, message):
        self.message = message

class CommandError(Exception):
    """
    Exception raised when a command occurs on an inappropriate channel
    """

    def __init__(self, message):
        self.message = message
