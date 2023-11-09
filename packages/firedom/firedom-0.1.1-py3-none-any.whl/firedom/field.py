from google.cloud.firestore_v1 import FieldFilter
from typing import Any


class Field:
    def __init__(self, name: str, field_type: type, default_value: any = None) -> None:
        self.name = name
        self.field_type = field_type
        self.default_value = default_value

    def __eq__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '==', value)

    def __ne__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '!=', value)

    def __lt__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '<', value)

    def __le__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '<=', value)

    def __gt__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '>', value)

    def __ge__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '>=', value)

    def __hash__(self) -> None:
        pass

    def is_in(self, values: list[any]) -> FieldFilter:
        return FieldFilter(self.name, 'in', values)

    def is_not_in(self, values: list[any]) -> FieldFilter:
        return FieldFilter(self.name, 'not-in', values)
