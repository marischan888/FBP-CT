import numpy as np
from scipy.fft import fft, ifft, fftfreq, fftshift
from src.config.ir_config import FilterType


class Filters:
    def __init__(self, filter_type: FilterType):
        """
        :param filter_type: FilterType enum
            ramp, shepp-logan, cosine, hamming, hann.
        """
        self.filter = filter_type

    def get_fourier_filter(self, size):
        """
        :param size: int
            filter size.
        :return: ndarray
            The computed Fourier filter.
        """

        # generate a symmetric odd-numbered index pattern to compute filter
        # coefficients
        # like: [1, 3, 5, ..., 5, 3, 1]
        n = np.concatenate(
            (np.arange(1, size / 2 + 1, 2, dtype=int),
             np.arange(size / 2 - 1, 0, -2, dtype=int))
            )
        # generate ramp filter with center coefficient is 0.25
        f = np.zeros(size)
        f[0] = 0.25
        # decay filter shape, part of ramp filter
        f[1::2] = -1 / (np.pi * n) ** 2
        fourier_filter = 2 * np.real(fft(f))  # ramp filter
        match self.filter:
            case FilterType.RAMP:
                pass
            case FilterType.SHEPP:
                omega = np.pi * fftfreq(size)[1:]
                fourier_filter[1:] *= np.sin(omega) / omega
            case FilterType.COSINE:
                freq = np.linspace(0, np.pi, size, endpoint=False)
                cosine_filter = fftshift(np.sin(freq))
                fourier_filter *= cosine_filter
            case FilterType.HAMMING:
                fourier_filter *= fftshift(np.hamming(size))
            case FilterType.HANN:
                fourier_filter *= fftshift(np.hanning(size))
            case FilterType.NONE:
                fourier_filter[:] = 1
            case _:
                raise ValueError(f"Unknown filter type: {self.filter}")

        # Reshape the output from 1D to 2D for following multiplication
        return fourier_filter[:, np.newaxis]
