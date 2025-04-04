import os
import imageio
import h5py
import numpy as np
from matplotlib import pyplot as plt
from skimage.transform import resize


def load_image(path, size=(256, 256)):
    """Load a grayscale image and resize."""
    image = imageio.imread(path, mode='L')
    image = resize(image, size, mode='reflect', anti_aliasing=True)
    return image


def load_h5(path):
    """Load data from .h5 file."""
    with h5py.File(path, 'r') as f:
        data = f['data'][:]
    return data


def load_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg']:
        file = load_image(path)
    elif ext == '.h5':
        file = load_h5(path)
    else:
        raise ValueError(
            'Unsupported file. Use .h5 or image formats like .png'
            )
    return file


def save_image(image: np.ndarray, path: str):
    """Save a NumPy array as a grayscale image."""
    cm = plt.get_cmap('gray')
    image = cm(image / np.max(image))
    image_uint8 = (image * 255.9999).astype(np.uint8)
    imageio.imwrite(path, image_uint8)


def save_result(result: np.ndarray, path: str):
    """Save result as .h5 or .png."""
    ext = os.path.splitext(path)[1].lower()

    if ext == '.h5':
        with h5py.File(path, 'w') as f:
            f.create_dataset('data', data=result)
    elif ext in ['.png', '.jpg', '.jpeg']:
        save_image(result, path)
    else:
        raise ValueError(
            "Unsupported save format. Use .h5 or image formats like .png"
            )
