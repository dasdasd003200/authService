from dataclasses import dataclass
from typing import TYPE_CHECKING

# Usar TYPE_CHECKING para evitar circular imports
if TYPE_CHECKING:
    from ..inputs.find import UserFindInput
    from ..inputs.find_one import UserFindOneInput


@dataclass
class UserFindQuery:
    input: "UserFindInput"


@dataclass
class UserFindOneQuery:
    input: "UserFindOneInput"

