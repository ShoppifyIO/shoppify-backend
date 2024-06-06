from typing import Dict, TypeVar, Any, List

from rest.common.exceptions.bad_param_type_exception import BadParamTypeException
from rest.common.exceptions.missing_param_exception import MissingParamException


class Extractor:
    dictionary: Dict[str, any]

    def __init__(self, dictionary: Dict[str, any]):
        self.dictionary = dictionary

    def str_required(self, param_name: str) -> str:
        try:
            param = self.dictionary.get(param_name)
            Extractor.__ensure_is_str(param_name, param)
            return param
        except KeyError:
            raise MissingParamException(param_name)

    def str_optional(self, param_name: str, default: str | None = None) -> str | None:
        try:
            param = self.dictionary.get(param_name)
            Extractor.__ensure_is_str(param_name, param, True)
            return param
        except KeyError:
            return default

    def int_required(self, param_name: str) -> int:
        try:
            param = self.dictionary.get(param_name)
            Extractor.__ensure_is_int(param_name, param)
            return param
        except KeyError:
            raise MissingParamException(param_name)

    def int_optional(self, param_name: str, default: int | None = None) -> int | None:
        try:
            param = self.dictionary.get(param_name)
            Extractor.__ensure_is_int(param_name, param, True)
            return param
        except KeyError:
            return default

    def array_required(self, array_name: str) -> List[Any]:
        try:
            array = self.dictionary.get(array_name)
            Extractor.__ensure_is_array(array_name, array)
            return array
        except KeyError:
            raise MissingParamException(array_name)

    def array_optional(self, array_name: str) -> List[Any]:
        try:
            array = self.dictionary.get(array_name)
            Extractor.__ensure_is_array(array_name, array, True)
            return array if array is not None else []
        except KeyError:
            return []

    @staticmethod
    def __ensure_is_str(param_name: str, param: any, none_allowed: bool = False) -> None:
        if param is None and none_allowed:
            return

        if not isinstance(param, str):
            raise BadParamTypeException(param_name)

    @staticmethod
    def __ensure_is_int(param_name: str, param: any, none_allowed: bool = False) -> None:
        if param is None and none_allowed:
            return

        if not isinstance(param, int):
            raise BadParamTypeException(param_name)

    @staticmethod
    def __ensure_is_array(param_name: str, param: any, none_allowed: bool = False) -> None:
        if param is None and none_allowed:
            return

        if not isinstance(param, list):
            raise BadParamTypeException(param_name)
