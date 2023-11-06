from enum import Enum
from typing import Type, Union

class EnumUtils(Enum):
    @classmethod
    def get_all_values(cls) -> list[Union[Enum, Type]]: ...
