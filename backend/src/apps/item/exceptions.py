from settings.exceptions import ServiceException


class ItemNotFoundError(ServiceException):
    def __init__(self, sku: str) -> None:
        self.sku = sku
        super().__init__("Item not found")
