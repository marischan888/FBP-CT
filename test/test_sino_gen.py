import numpy as np
import pytest
from src.core.sino_gen import SinoGen


def test_sinogen_invalid_input():
    with pytest.raises(ValueError):
        SinoGen(np.ones((64, 64, 3))).radon()
