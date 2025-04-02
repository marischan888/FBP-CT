from src.utils.io_handler import load_file
from src.core.sino_gen import SinoGen
from src.core.fbp import FBP


def simulate_from_file(
        path,
        theta,
        preserve_range=True
        ):
    file = load_file(path)
    sinogram = SinoGen(file, theta, preserve_range).radon()

    return sinogram


def reconstruct_from_file(
        path,
        theta,
        filter_type,
        output_size,
        interpolation,
        preserve_range=True
        ):
    file = load_file(path)

    image = FBP(
        file,
        theta,
        filter_type,
        output_size,
        interpolation,
        preserve_range
        ).iradon()
    return image
