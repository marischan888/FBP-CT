from skimage._shared.utils import convert_to_float
from scipy.interpolate import interp1d
import numpy as np
from scipy.fft import fft, ifft, fftfreq, fftshift
from filters import _get_fourier_filter
from src.config.filter_type import FilterType

class FBP:

    def __init__(self, sinogram, theta=None, filter=FilterType.NONE, output_size=None):
        self.sinogram = sinogram
        self.theta = theta
        self.filter = filter
        self.output_size = output_size


    def backprojection(self, interval=None):
        if self.theta is None:
            theta = np.linspace(0, 180, self.sinogram.shape[1], endpoint=False)

        sinogram = convert_to_float(self.sinogram, preserve_range=True)

        if self.output_size is None:
            output_size = int(np.floor(np.sqrt((sinogram.shape[0]) ** 2 / 2.0)))  # shape of output
        img_shape = sinogram.shape[0]

        if filter not in FilterType:
            raise ValueError(f"Unknown filter: {filter}")
        else:
            fourier_filter = _get_fourier_filter(img_shape, filter)
            projection = fft(sinogram, axis=0) * fourier_filter
            sinogram = np.real(ifft(projection, axis=0)[:img_shape, :])

        reconstructed = np.zeros((output_size, output_size),
                                 dtype=sinogram.dtype)
        radius = output_size // 2
        xpr, ypr = np.mgrid[:output_size, :output_size] - radius
        x = np.arange(img_shape) - img_shape // 2

        for col_idx, angle in zip(range(0, len(theta), interval), np.deg2rad(theta[::interval])):
            col = sinogram[:, col_idx]
            t = ypr * np.cos(angle) - xpr * np.sin(angle)

            interpolant = interp1d(x, col, kind='linear',
                                   bounds_error=False, fill_value=0)
            reconstructed += interpolant(t)

        return sinogram, reconstructed * np.pi / (2 * len(theta))

    



