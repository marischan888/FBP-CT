import numpy as np
from skimage._shared.utils import convert_to_float
from skimage.transform import warp


class SinoGen:
    def __init__(self, image, theta=None, preserve_range=False):
        self.image = image
        self.theta = theta
        self.preserve_range = preserve_range

    def radon(self):
        if self.image.ndim != 2:
            raise ValueError('The input image must be 2-D')
        if self.theta is None:
            self.theta = np.arange(180)
        elif isinstance(self.theta, (int, float)):
            self.theta = np.linspace(
                0, self.theta, int(self.theta), endpoint=False
                )

        image = convert_to_float(self.image, self.preserve_range)

        diagonal = np.sqrt(2) * max(image.shape)
        pad = [int(np.ceil(diagonal - s)) for s in image.shape]
        new_center = [(s + p) // 2 for s, p in zip(image.shape, pad)]
        old_center = [s // 2 for s in image.shape]
        pad_before = [nc - oc for oc, nc in zip(old_center, new_center)]
        pad_width = [(pb, p - pb) for pb, p in zip(pad_before, pad)]
        padded_image = np.pad(
            image, pad_width, mode='constant', constant_values=0
            )

        # padded_image is always square
        if padded_image.shape[0] != padded_image.shape[1]:
            raise ValueError('padded_image must be a square')
        center = padded_image.shape[0] // 2
        radon_image = np.zeros(
            (padded_image.shape[0], len(self.theta)), dtype=image.dtype
            )

        for i, angle in enumerate(np.deg2rad(self.theta)):
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            R = np.array(
                [
                    [cos_a, sin_a, -center * (cos_a + sin_a - 1)],
                    [-sin_a, cos_a, -center * (cos_a - sin_a - 1)],
                    [0, 0, 1],
                ]
            )
            rotated = warp(padded_image, R, clip=False)
            radon_image[:, i] = rotated.sum(0)
        return radon_image
