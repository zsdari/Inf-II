import getpass
import json
import signal
import sys
from typing import Protocol


class FilterProtocol(Protocol):
    def validate(self,password: str) -> list:
        raise NotImplemented("Filter must have a implemented validate function!")


class Config:
    _instance = None

    @classmethod
    def get_instance(cls, filter: FilterProtocol = None) -> "Config":
        if cls._instance is None:
            if filter is None:
                raise Exception("Filter need initialise first wit filter!")
            cls._instance = Config(filter)
        return cls._instance

    def __init__(self, filter: FilterProtocol):
        self.filter = filter

class MinFilterBase(FilterProtocol):
    def __init__(self, min: int= 1):
        self.min = min

    def validate(self,password: str) -> list:
        raise NotImplemented("Filter must have a implemented validate function!")


class CharMethodFilter(MinFilterBase):
    def __init__(self,min,method_name):
        super().__init__(min)
        self.method_name = method_name
        try:
            s = "abf"
            for c in s:
                getattr(c, method_name)
        except AttributeError:
            raise AttributeError(f"{method_name} not exiting methon in {type(c)}")


    def validate(self,password: str) -> list:
        errors = []
        count = 0
        for c in password:
            method = getattr(c, self.method_name)
            if method():
                count += 1
        if count < self.min:
            errors.append(f"Password must have at least {self.min} {self.method_name} characters!")
        return errors

class UpperCharFilter(CharMethodFilter):
    def __init__(self, min: int = 1):
        super().__init__(min,"isupper")

class LowerCharFilter(CharMethodFilter):
    def __init__(self, min: int = 1):
        super().__init__(min,"islower")

class NumericCharFilter(CharMethodFilter):
    def __init__(self, min: int = 1):
        super().__init__(min, "isnumeric")

class LengthFilter(MinFilterBase):
    def __init__(self, min: int= 4 , max: int = None):
        super().__init__(min)
        self.max = max

    def validate(self,password: str) -> list:
        errors = []
        if len(password) < self.min:
            errors.append(f"Password length is smaller like the min({self.min})!")
        if self.max is not None and len(password) > self.max:
            errors.append(f"Password length is bigger like the max({self.max})!")
        return errors

class SpecialCharFilter(MinFilterBase):
    def __init__(self, special_chars = [".",",","*"], min = 1):
        super().__init__(min)
        self.special_chars = special_chars


    def validate(self,password: str) -> list:
        errors = []
        special_chars = 0
        for char in self.special_chars:
            if char in password:
                special_chars += 1
        if special_chars < self.min:
            errors.append("Password must contain at least one special char!")
        return errors


class AndFilter(FilterProtocol):
    def __init__(self, filters: list):
        self.filters = filters

    def validate(self,password: str) -> list:
        errors = []
        for filter in self.filters:
            _error: list = filter.validate(password)
            errors += _error
        return errors

class FilterFactory:
    @staticmethod
    def from_dict(data: dict):
        if "type" not in data:
            raise ValueError("Filter must have a type!")
        if "args" not in data:
            raise ValueError("Filter must have args!")
        if data["type"] == "AndFilter":
            filters = []
            if "filters" not in data["args"]:
                raise ValueError("AndFilter must have filters!")
            for filter in data["args"]["filters"]:
                filters.append(FilterFactory.from_dict(filter))
            if len(filters) > 0:
                return AndFilter(filters)
        else:
            FilterClass = globals()[data["type"]]
            return FilterClass(**data["args"])


class ConfigLoader:

    @staticmethod
    def load_from_file_byname(file_name):
        filter = None
        with open(file_name, "r", encoding="utf-8") as f:
            data_str = f.read()
            data = json.loads(data_str)
            if "filter" not in data:
                raise ValueError("Config file must contain filter")
            filter = FilterFactory.from_dict(data["filter"])
        config = Config.get_instance(filter)
        return config


def signal_handler(signum, frame):
    if signum == 2:
        print("\nCtrl+C pressed, exiting...")
        sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    config = ConfigLoader.load_from_file_byname("config.json")
    print(Config.get_instance())
    while True:
        password = getpass.getpass("Check: ")
        errors = config.filter.validate(password)
        if len(errors) == 0:
            print("Password is ok")
        else:
            print("Password error:")
            for error in errors:
                print("\t",error)