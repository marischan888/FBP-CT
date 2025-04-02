import numpy as np
import pytest
from src.core.filters import Filters
from src.config.ir_config import FilterType  # adjust if needed

def test_filters_ramp():
    f = Filters(FilterType.RAMP)
    result = f.get_fourier_filter(64)
    assert result.shape == (64, 1)

def test_filters_shepp():
    f = Filters(FilterType.SHEPP)
    result = f.get_fourier_filter(64)
    assert result.shape == (64, 1)

def test_filters_none():
    f = Filters(FilterType.NONE)
    result = f.get_fourier_filter(64)
    assert np.all(result == 1)

def test_filters_invalid():
    with pytest.raises(ValueError):
        Filters("invalid").get_fourier_filter(64)
