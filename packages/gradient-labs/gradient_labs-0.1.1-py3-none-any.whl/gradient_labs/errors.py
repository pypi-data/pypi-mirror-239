class ResponseError(Exception):
    def __init__(self, response):
        super().__init__()

        self.status_code = response.status_code
        self.message = response.json()["message"]

    def __str__(self):
        return f"HTTP {self.status_code}: {self.message}"
