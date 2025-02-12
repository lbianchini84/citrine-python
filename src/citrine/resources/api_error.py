from copy import copy
from typing import Optional, List

from taurus.entity.dict_serializable import DictSerializable


class ValidationError(DictSerializable):
    """A user-facing error message describing why their request was invalid."""

    def __init__(self, failure_message: Optional[str] = None, property: Optional[str] = None,
                 input: Optional[str] = None):
        self.failure_message = failure_message
        self.property = property
        self.input = input


class ApiError(DictSerializable):
    """The engineering API root level error model."""

    def __init__(self, code: int, message: str, validation_errors: List[ValidationError] = None):
        self.code = code
        self.message = message
        self.validation_errors = validation_errors or []

    @classmethod
    def from_dict(cls, d):
        d = copy(d)
        d.pop('debug_stacktrace', None)
        # TODO: deserialize to correct type automatically
        d['validation_errors'] = [ValidationError.from_dict(e) for e in d.get('validation_errors', [])]
        return cls(**d)
