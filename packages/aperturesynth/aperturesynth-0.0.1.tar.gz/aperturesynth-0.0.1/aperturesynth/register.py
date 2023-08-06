import numpy as np
from skimage import transform
from skimage.feature import match_template
from skimage.color import rgb2gray


def find_max_correlation(image, template):
    """Find the location of the maximum correlation between the template and
    the image.

    Parameters
    ----------

    image: M, N  ndarray
        The image to search within for the template. Colour images must first
        be converted to a channel.
    template: m, n ndarray
        The template image to search for. Must be single channel.

    Returns
    -------
    (x,y): tuple of x and y coordinates in the image.

    """
    score = match_template(image, template)
    ij = np.unravel_index(np.argmax(score), score.shape)
    x, y = ij[::-1]
    return x, y


def extract_patches(image, windows, pad=0):
    """Extract grayscale patches from the image at the given locations.

    Parameters
    ----------

    image: M,N,3 ndarray
        The three channel image to extract the windows from.
    windows: n_windows*2,2 ndarray
        X,Y coordinates of starting and finishing points of each rectangular
        window.
    pad: integer (default=0)
        The amount to pad the window size from the given locations.

    Returns
    -------
    patches: list of ndarrays
        The patches extracted from the image.

    """
    patches = []
    coords = []
    max_rows, max_cols = image.shape[:2]
    n_windows = int(windows.shape[0] / 2)
    for i in range(n_windows):
        rows = windows[i*2:(i*2 + 2), 0] + [-pad, pad]
        cols = windows[i*2:(i*2 + 2), 1] + [-pad, pad]
        rows[rows < 0] = 0
        rows[rows > max_rows] = max_rows
        cols[cols < 0] = 0
        cols[cols > max_cols] = max_cols
        this_patch = image[rows[0]:rows[1], cols[0]:cols[1]]
        patches.append(rgb2gray(this_patch))
        coords.append(np.vstack((rows, cols)).T)
    if pad > 0:
        return patches, np.vstack(coords)
    else:
        return patches


class Registrator(object):
    """Transform a reference image to match a baseline image.

    Parameters
    ----------

    windows: (n_windows*2),2 ndarray
        x,y coordinates for focal points.
    base_image: M,N,3 ndarray
        Baseline image to match other images to.
    pad: integer (default=400)
        Size of search space outside the defined window in images to be
        registered.

    """
    def __init__(self, windows, base_image, pad=400):
        self.windows = windows
        self.pad = pad
        self.templates = extract_patches(base_image, windows)

    def match(self, image):
        """Matches an image to the baseline image.

        Parameters
        ----------

        image: M,N,3 ndarray
            Image to be matched.

        Returns
        -------

        transformed_image: M,N,3 ndarray
            The input image transformed to match the baseline image at the
            selected points.

        """
        search_windows, search_coords = extract_patches(image,
                                                        self.windows,
                                                        pad=self.pad)
        shifts = []
        for window, template in zip(search_windows, self.templates):
            shifts.append(find_max_correlation(window, template))
        shifts = np.vstack(shifts)
        # Convert coordinates from padded windows to absolute position
        delta = search_coords[::2, [1, 0]] - self.windows[::2, [1, 0]]
        points1 = self.windows[::2, [1, 0]]
        points2 = points1 - shifts - delta

        match_tform = transform.estimate_transform('affine',
                                                   points2,
                                                   points1)
        return (transform.warp(image, match_tform).astype('float32'),
                match_tform)

    def __call__(self, image):
        return self.match(image)
