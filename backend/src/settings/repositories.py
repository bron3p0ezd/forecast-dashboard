from abc import ABC, abstractmethod
from typing import Generic, Optional, Type

from settings.database import MODEL_TYPE


class Repository(ABC):
    @abstractmethod
    def __init__(self, **kwargs) -> None: ...


class ORMRepository(Repository, Generic[MODEL_TYPE]):
    cls_model: Optional[Type[MODEL_TYPE]] = None

    @abstractmethod
    def __init__(self, **kwargs) -> None: ...
