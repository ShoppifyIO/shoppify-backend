from typing import Dict, TypeVar

from rest.common.exceptions.bad_param_type_exception import BadParamTypeException
from rest.common.exceptions.missing_param_exception import MissingParamException


class Extractor:
    dictionary: Dict[str, any]

    def __init__(self, dictionary: Dict[str, any]):
        self.dictionary = dictionary

    def str_required(self, param_name: str) -> str:
        try:
            param = self.dictionary.get(param_name)
            Extractor.__ensure_is_str(param)
            return param
        except KeyError:
            raise MissingParamException(param_name)

    def str_optional(self, param_name: str, default: str | None = None) -> str | None:
        try:
            param = self.dictionary.get(param_name)
            Extractor.__ensure_is_str(param)
            return param
        except KeyError:
            return default

    def int_required(self, param_name: str) -> int:
        try:
            param = self.dictionary.get(param_name)
            Extractor.__ensure_is_int(param)
            return param
        except KeyError:
            raise MissingParamException(param_name)

    def int_optional(self, param_name: str, default: int | None = None) -> int | None:
        try:
            param = self.dictionary.get(param_name)
            Extractor.__ensure_is_int(param)
            return param
        except KeyError:
            return default

    @staticmethod
    def __ensure_is_str(param: any) -> None:
        if not isinstance(param, str):
            raise BadParamTypeException(param)

    @staticmethod
    def __ensure_is_int(param: any) -> None:
        if not isinstance(param, int):
            raise BadParamTypeException(param)
