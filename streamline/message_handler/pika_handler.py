import aio_pika


class PikaHandler:
    def __init__(self, uri):
        self.uri = uri