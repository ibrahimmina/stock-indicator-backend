class CustomException(Exception):
    def __init__(self, message, response_code):
        super().__init__(message)
        self.response_code = response_code