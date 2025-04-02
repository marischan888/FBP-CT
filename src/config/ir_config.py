from enum import Enum

class FilterType(Enum):
    NONE = 1
    RAMP = 2
    SHEPP = 3

class InterpolationType(Enum):
    LINEAR = 1
    NEAREST = 2
    CUBIC = 3