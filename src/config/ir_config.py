from enum import Enum

class FilterType(Enum):
    NONE = 1
    RAMP = 2
    SHEPP = 3
    COSINE = 4
    HAMMING = 5
    HANN = 6

class InterpolationType(Enum):
    LINEAR = 1
    NEAREST = 2
    CUBIC = 3