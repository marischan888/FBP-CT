import numpy as np
import pytest
from src.core.sino_gen import SinoGen

def test_sinogen_valid():
    dummy_image = np.ones((64, 64))
    sg = SinoGen(dummy_image, theta=180)
    result = sg.radon()
    assert result.shape[1] == 180

def test_sinogen_invalid_input():
    with pytest.raises(ValueError):
        SinoGen(np.ones((64, 64, 3))).radon()
