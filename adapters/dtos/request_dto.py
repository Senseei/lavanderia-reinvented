class RequestDTO:
    def __init__(self, body: dict = None, query: dict = None, headers: dict = None):
        self.body = body if body is not None else {}
        self.query = query if query is not None else {}
        self.headers = headers if headers is not None else {}