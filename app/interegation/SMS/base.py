
class SMSProvider:
    async def send(self, phone: str, message: str) -> None:
        raise NotImplementedError