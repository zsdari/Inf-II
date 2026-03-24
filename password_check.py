import getpass
import json
import logging
import signal
import sys
import datetime
from typing import Protocol


class FilterProtocol(Protocol):
    def validate(self, password: str) -> list:
        raise NotImplementedError("Filter must have a implemented validate function!")


class Config:
    _instance = None

    @classmethod
    def get_instance(cls, filter: FilterProtocol = None) -> "Config":
        if cls._instance is None:
            if filter is None:
                raise Exception("Filter need initialise first with filter!")
            cls._instance = Config(filter)
        return cls._instance

    def __init__(self, filter: FilterProtocol):
        self.filter = filter


class MinFilterBase(FilterProtocol):
    def __init__(self, min: int = 1):
        self.min = min

    def validate(self, password: str) -> list:
        raise NotImplementedError("Filter must have a implemented validate function!")


class CharMethodFilter(MinFilterBase):
    def __init__(self, min, method_name):
        super().__init__(min)
        self.method_name = method_name
        try:
            s = "abf"
            for c in s:
                getattr(c, method_name)
        except AttributeError:
            raise AttributeError(f"{method_name} not existing method in {type(c)}")

    def validate(self, password: str) -> list:
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
        super().__init__(min, "isupper")


class LowerCharFilter(CharMethodFilter):
    def __init__(self, min: int = 1):
        super().__init__(min, "islower")


class NumericCharFilter(CharMethodFilter):
    def __init__(self, min: int = 1):
        super().__init__(min, "isnumeric")


class LengthFilter(MinFilterBase):
    def __init__(self, min: int = 4, max: int = None):
        super().__init__(min)
        self.max = max

    def validate(self, password: str) -> list:
        errors = []
        if len(password) < self.min:
            errors.append(f"Password length is smaller than the min({self.min})!")
        if self.max is not None and len(password) > self.max:
            errors.append(f"Password length is bigger than the max({self.max})!")
        return errors


class SpecialCharFilter(MinFilterBase):
    def __init__(self, special_chars=[".", ",", "*"], min=1):
        super().__init__(min)
        self.special_chars = special_chars

    def validate(self, password: str) -> list:
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

    def validate(self, password: str) -> list:
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
            if "filters" not in data["args"]:
                raise ValueError("AndFilter must have filters!")
            filters = []
            for filter_data in data["args"]["filters"]:
                filters.append(FilterFactory.from_dict(filter_data))
            return AndFilter(filters)
        else:
            FilterClass = globals().get(data["type"])
            if FilterClass is None:
                raise ValueError(f"Filter type '{data['type']}' not found!")
            return FilterClass(**data["args"])


class ConfigLoader:
    @staticmethod
    def load_from_file_byname(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            return ConfigLoader.load_from_file(f)

    @staticmethod
    def load_from_file(file):
        data = file.read()
        return ConfigLoader.from_json_str(data)

    @staticmethod
    def from_json_str(json_str):
        d = json.loads(json_str)
        return ConfigLoader.from_dict(d)

    @staticmethod
    def from_dict(d):
        if "filter" not in d:
            raise ValueError("Config file must contain filter")
        filter = FilterFactory.from_dict(d["filter"])
        config = Config.get_instance(filter)
        return config


def signal_handler(signum, frame):
    if signum == 2:
        print("\nCtrl+C pressed, exiting...")
        sys.exit(0)

class JsonFormater(logging.Formatter):
    def format(self, record):

        log_entry = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        if hasattr(record, "extradata"):
            log_entry["extra_data"] = record.extra_data
        return json.dumps(log_entry, ensure_ascii=False)

if __name__ == "__main__":
    logger = logging.getLogger("PasswordChecker")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("password_check.jsonl", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    signal.signal(signal.SIGINT, signal_handler)

    logger.debug("Starting password check...")

    try:
        config = ConfigLoader.load_from_file_byname("config.json")
        print("Password checker started successfully!")

        while True:
            password = getpass.getpass("\nCheck password: ")
            errors = config.filter.validate(password)

            if len(errors) == 0:
                print("✓ Password is OK")
                logger.info("Password validation successful")
            else:
                print("✗ Password errors:")
                for error in errors:
                    print(f"  - {error}")
                logger.warning(f"Password validation failed: {errors}")

    except FileNotFoundError:
        print("Error: config.json file not found!")
        logger.error("config.json file not found")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        logger.error(f"Invalid JSON in config file: {e}")
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"Unexpected error: {e}")