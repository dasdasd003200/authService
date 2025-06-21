from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TCommand = TypeVar("TCommand")
TResult = TypeVar("TResult")


class BaseUseCase(ABC, Generic[TCommand, TResult]):
    """Base use case interface"""

    @abstractmethod
    async def execute(self, command: TCommand) -> TResult:
        """Execute the use case"""
        pass
