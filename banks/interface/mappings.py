class BaseMapping:
    def __init__(self, payload: dict):
        self._payload = payload


class BankMapping(BaseMapping):
    @property
    def ispb(self) -> str:
        return self._payload.get("ispb")

    @property
    def name(self) -> str:
        return self._payload.get("name")
