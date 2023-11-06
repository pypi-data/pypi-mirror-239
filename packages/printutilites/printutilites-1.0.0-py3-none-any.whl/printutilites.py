class PrintManager:

    def __init__(self, message: str, count: int = 1):
        self.message = message
        self.count = count

    def print(self):
        for i in range(self.count):
            print(self.message)
