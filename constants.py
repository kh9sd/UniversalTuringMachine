from enum import Enum


class HaltedException(Exception):
    pass


class Move(Enum):
    LEFT = "L"
    RIGHT = "R"
    STAY = "N"
