from dataclasses import dataclass
from typing import Dict, Any, TYPE_CHECKING

# Usar TYPE_CHECKING para evitar circular imports
if TYPE_CHECKING:
    from ..inputs.create import UserCreateInput
    from ..inputs.update import UserUpdateInput


@dataclass
class UserCreateCommand:
    input: "UserCreateInput"
    user_context: Dict[str, Any]


@dataclass
class UserUpdateCommand:
    input: "UserUpdateInput"
    user_context: Dict[str, Any]


@dataclass
class UserDeleteCommand:
    user_id: str
    user_context: Dict[str, Any]

