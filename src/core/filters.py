import numpy as np
from scipy.fft import fft, fftfreq
from src.config.ir_config import FilterType


class Filters:
    def __init__(self, filter_type: FilterType):
        self.filter = filter_type

    def get_fourier_filter(self, size):
        n = np.concatenate(
            (np.arange(1, size / 2 + 1, 2, dtype=int),
             np.arange(size / 2 - 1, 0, -2, dtype=int))
            )
        f = np.zeros(size)
        f[0] = 0.25
        f[1::2] = -1 / (np.pi * n) ** 2

        fourier_filter = 2 * np.real(fft(f))  # ramp filter
        match self.filter:
            case FilterType.RAMP:
                pass
            case FilterType.SHEPP:
                omega = np.pi * fftfreq(size)[1:]
                fourier_filter[1:] *= np.sin(omega) / omega
            case FilterType.NONE:
                fourier_filter[:] = 1
            case _:
                raise ValueError(f"Unknown filter type: {self.filter}")

        return fourier_filter[:, np.newaxis]
