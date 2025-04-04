import numpy as np
from skimage._shared.utils import convert_to_float
from skimage.transform import warp


class SinoGen:
    def __init__(self, image, theta=None, preserve_range=False):
        """
        :param image: ndarray
            The rotation axis of detector will be located in the center
            pixel of image.
        :param theta: int
             Projection angles (in degrees).  If `None`, the value is set to 180.
        :param preserve_range: boolean
            Whether to keep the original range of values.
        """
        self.image = image
        self.theta = theta
        self.preserve_range = preserve_range

    def radon(self):
        """
        :return: ndarray
             Radon transform (sinogram).
        """
        if self.image.ndim != 2:
            raise ValueError('The input image must be 2-D')
        if self.theta is None:
            self.theta = np.arange(180)
        elif isinstance(self.theta, (int, float)):
            self.theta = np.linspace(
                0, self.theta, int(self.theta), endpoint=False
                )

        image = convert_to_float(self.image, self.preserve_range)

        # Padding and centering the image, so it won’t get cropped during
        # rotation. When you rotate an image, the corners can stick out of
        # frame unless the image is padded to fully contain any rotation.
        diagonal = np.sqrt() * max(image.shape)

        # For each dimension (height, width), compute how much padding is
        # needed to reach that diagonal size.
        pad = [int(np.ceil(diagonal - s)) for s in image.shape]

        # center of old and padded image
        new_center = [(s + p) // 2 for s, p in zip(image.shape, pad)]
        old_center = [s // 2 for s in image.shape]

        # Figures out how much padding to apply before and after the image,
        # so the image stays centered.
        pad_before = [nc - oc for oc, nc in zip(old_center, new_center)]
        pad_width = [(pb, p - pb) for pb, p in zip(pad_before, pad)]

        # Applies the padding with zeros. This ensures:
        # No loss of content during Radon projection (rotation)
        padded_image = np.pad(
            image, pad_width, mode='constant', constant_values=0
            )

        # padded_image is always square, This prevents distortion during
        # rotation.
        if padded_image.shape[0] != padded_image.shape[1]:
            raise ValueError('padded_image must be a square')
        center = padded_image.shape[0] // 2
        # Preallocate the sinogram
        radon_image = np.zeros(
            (padded_image.shape[0], len(self.theta)), dtype=image.dtype
            )

        # For each angle, rotate and project:
        for i, angle in enumerate(np.deg2rad(self.theta)):
            cos_a, sin_a = np.cos(angle), np.sin(angle)

            # Compute the rotation matrix R (KEY to SIMULATE)
            # rotating the object around center to collect projections from
            # each angle.
            R = np.array(
                [
                    [cos_a, sin_a, -center * (cos_a + sin_a - 1)],
                    [-sin_a, cos_a, -center * (cos_a - sin_a - 1)],
                    [0, 0, 1],
                ]
            )

            #  warp(): rotates the image using interpolation with R
            rotated = warp(padded_image, R, clip=False)

            # Sum over rows (axis=0) to simulate X-ray beams passing through
            # the object.
            radon_image[:, i] = rotated.sum(0)
        return radon_image
