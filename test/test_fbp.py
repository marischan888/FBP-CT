import numpy as np
import pytest
from src.core.fbp import FBP
from src.config.ir_config import FilterType

def test_fbp_valid_reconstruction():
    dummy_sinogram = np.ones((64, 180))
    fbp = FBP(dummy_sinogram, theta=180, filter_type=FilterType.RAMP)
    result = fbp.iradon()
    assert result.shape[0] == result.shape[1]

def test_fbp_invalid_shape():
    with pytest.raises(ValueError):
        FBP(np.ones((64, 64, 3)), theta=180).iradon()
