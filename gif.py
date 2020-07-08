import functools
from importlib import import_module
import io

from matplotlib import pyplot as plt
from PIL import Image

try:
    from altair_saver import save as save_alt
    altair_saver_installed = True
except ModuleNotFoundError:
    altair_saver_installed = False


class MissingExtension(Exception):
    pass


def frame(func):
    """
    Decorator for a matplotlib plot function.

    matplotlib Example:
    ```
    @gif.frame
    def plot(x, y):
        plt.figure(figsize=(5, 5))
        plt.scatter(x, y)
        plt.xlim((0, 100))
        plt.ylim((0, 100))
    ```
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        buffer = io.BytesIO()
        plot = func(*args, **kwargs)
        if "altair" in str(type(plot)):
            if not altair_saver_installed:
                raise MissingExtension("pip install gif[altair]")
            save_alt(plot, buffer, fmt="png")
        else:
            plt.savefig(buffer, format="png")
            plt.close()
        buffer.seek(0)
        image = Image.open(buffer)
        return image

    return wrapper


def save(frames, path, duration=100):
    """
    Save decorated frames to an animated gif.

    - frames (list): collection of frames built with the frame decorator
    - path (str): filename with relative or absolute path
    - duration (int): milliseconds between frames
    """
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=duration,
        loop=0,
    )
