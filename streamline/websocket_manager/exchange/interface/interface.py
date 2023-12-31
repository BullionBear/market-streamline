from abc import ABC, abstractmethod


class Interface(ABC):

    @abstractmethod
    async def get_channel(self):
        pass

    @abstractmethod
    async def get_ws_url(self):
        pass

    @abstractmethod
    async def start(self, on_message: callable):
        pass

    @abstractmethod
    async def on_diff(self, base, quote, instrument):
        pass

    @abstractmethod
    async def off_diff(self, base, quote, instrument):
        pass
