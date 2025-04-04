from skimage._shared.utils import convert_to_float
from scipy.interpolate import interp1d
import numpy as np
from scipy.fft import fft, ifft
from src.core.filters import Filters
from functools import partial
from src.config.ir_config import FilterType, InterpolationType


class FBP:
    def __init__(
            self,
            sinogram,
            theta=None,
            filter_type=FilterType.NONE,
            output_size=None,
            interpolation=InterpolationType.LINEAR,
            preserve_range=True
            ):
        """
        :param sinogram:  ndarray
            Image containing radon transform (sinogram). Each column of
            the image corresponds to a projection along a different
            angle. The tomography rotation axis should lie at the pixel
            index ``radon_image.shape[0] // 2`` along the 0th dimension of
            ``radon_image``.
        :param theta: int
            Reconstruction angles (in degrees). Default: m angles evenly spaced
            between 0 and 180 (if the shape of `radon_image` is (N, M)).
        :param filter_type: str
            Filter used in frequency domain filtering. Ramp filter used by default.
            Filters available: ramp, shepp-logan, cosine, hamming, hann.
            Assign None to use no filter.
        :param output_size: int
            Number of rows and columns in the reconstruction.
        :param interpolation: str
            Interpolation method used in reconstruction. Methods available:
            'linear', 'nearest', and 'cubic' ('cubic' is slow).
        :param preserve_range: bool
            Whether to keep the original range of values. Otherwise, the input
            image is converted according to the conventions of `img_as_float`.
        """
        self.sinogram = sinogram
        self.theta = theta
        self.filter_type = filter_type
        self.output_size = output_size
        self.interpolation = interpolation
        self.preserve_range = preserve_range

    def iradon(self):
        """
        :return: ndarray
            Reconstructed image. The rotation axis will be located in the pixel
            with indices
            ``(reconstructed.shape[0] // 2, reconstructed.shape[1] // 2)``.
        """
        if self.sinogram.ndim != 2:
            raise ValueError('The input image must be 2-D')

        if isinstance(self.theta, (int, float)):
            self.theta = np.linspace(
                0,
                self.theta,
                self.sinogram.shape[1],
                endpoint=False
                )
        else:
            self.theta = np.linspace(
                0, 180, self.sinogram.shape[1], endpoint=False
                )

        angles_count = len(self.theta)

        self.sinogram = convert_to_float(self.sinogram, self.preserve_range)
        dtype = self.sinogram.dtype

        img_shape = self.sinogram.shape[0]
        if self.output_size is None:
            # If output size not specified, estimate from input radon image
            self.output_size = int(np.floor(np.sqrt((img_shape) ** 2 / 2.0)))

        # Resize image to next power of two (but no less than 64) for
        # Fourier analysis; speeds up Fourier and lessens artifacts
        projection_size_padded = max(
            64, int(2 ** np.ceil(np.log2(2 * img_shape)))
            )
        pad_width = ((0, projection_size_padded - img_shape), (0, 0))
        img = np.pad(
            self.sinogram, pad_width, mode='constant', constant_values=0
            )

        # Apply filter in Fourier domain
        fourier_filter = Filters(self.filter_type).get_fourier_filter(
            projection_size_padded
            )

        projection = fft(img, axis=0) * fourier_filter
        radon_filtered = np.real(ifft(projection, axis=0)[:img_shape, :])

        # Reconstruct image by interpolation
        reconstructed = np.zeros(
            (self.output_size, self.output_size), dtype=dtype
            )
        radius = self.output_size // 2
        xpr, ypr = np.mgrid[:self.output_size, :self.output_size] - radius
        x = np.arange(img_shape) - img_shape // 2

        for col, angle in zip(radon_filtered.T, np.deg2rad(self.theta)):
            t = ypr * np.cos(angle) - xpr * np.sin(angle)
            match self.interpolation:
                case InterpolationType.LINEAR:
                    interpolant = partial(
                        np.interp, xp=x, fp=col, left=0, right=0
                        )
                case InterpolationType.CUBIC:
                    interpolant = interp1d(
                        x, col, kind='cubic', bounds_error=False, fill_value=0
                        )
                case InterpolationType.NEAREST:
                    interpolant = interp1d(
                        x, col, kind='nearest', bounds_error=False,
                        fill_value=0
                        )
                case _:
                    raise ValueError(f"Invalid interpolation")

            reconstructed += interpolant(t)

        return reconstructed * np.pi / (2 * angles_count)
