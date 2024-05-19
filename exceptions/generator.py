class XmlFileError(Exception):
    def __init__(self, message='Input Xml file does not exist.'):
        super(XmlFileError, self).__init__(message)
        self.message = message


class ParserError(Exception):
    def __init__(self, message='Syntax error in Xml'):
        super(ParserError, self).__init__(message)
        self.message = message


class NotSupportedError(Exception):
    def __init__(self, message='Not identified error'):
        super(NotSupportedError, self).__init__(message)
        self.message = message
