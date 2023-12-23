from abc import ABC, abstractmethod


class Interface(ABC):

    @abstractmethod
    async def get_channel(self):
        pass

    @abstractmethod
    async def get_ws_url(self):
        pass

    @abstractmethod
    async def start(self, message_handler: callable):
        pass

    @abstractmethod
    async def subscribe(self, *channels):
        pass

    @abstractmethod
    async def unsubscribe(self, *channels):
        pass