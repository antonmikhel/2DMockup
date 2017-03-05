import cv2
import numpy
import multiprocessing

from multiprocessing.dummy import Pool

CORES = multiprocessing.cpu_count()
IO_THREADS = 4


def load_img_grayscale(img_path):
    """
    :Description: This function loads images in grayscale mode
    :param img_path: Path where image resides
    :type img_path: str
    :return: image
    :rtype: numpy.ndarray
    """

    return cv2.imread(img_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)


def load_img_color(img_path):
    """
    :Description: This function loads images in color (3ch mode) mode
    :param img_path: Path where image resides
    :type img_path: str
    :return: image
    :rtype: numpy.ndarray
    """

    return cv2.imread(img_path, cv2.CV_LOAD_IMAGE_COLOR)


def load_img_unchanged(img_path):
    """
    :Description: This function loads images in unchanged mode
    :param img_path: Path where image resides
    :type img_path: str
    :return: image
    :rtype: numpy.ndarray
    """

    return cv2.imread(img_path, cv2.CV_LOAD_IMAGE_UNCHANGED)


def load_img_array(img_paths, load_mode=-1, threads=IO_THREADS):
    """
    :Description: This function loads images from given paths and returns an array of images.
    :param img_paths: list of image paths
    :type img_paths: list
    :param load_mode: mode to load images in. default is unchanged. uses cv2 load image flags
    :type load_mode: int
    :param threads: number of threads to use for io operation, default is 4
    :type threads: int
    :return:
    """
    """
    CV_LOAD_IMAGE_COLOR = 1
    CV_LOAD_IMAGE_GRAYSCALE = 0
    CV_LOAD_IMAGE_UNCHANGED = -1
    """

    pool = Pool(threads)
    img_array = None

    if load_mode == 0:
        img_array = pool.map(load_img_grayscale, img_paths)
    elif load_mode == 1:
        img_array = pool.map(load_img_color, img_paths)
    elif load_mode == -1:
        img_array = pool.map(load_img_unchanged, img_paths)

    return img_array


