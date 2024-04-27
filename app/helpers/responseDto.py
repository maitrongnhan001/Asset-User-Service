class ResponseDTO:
    status: int
    message: str
    data: str

    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data