import os
import cv2
import glob
import numpy

from blend_modes import blend_modes

from Logger import MFLogger
from utils import io_functions


class MockupGen(object):
    def __init__(self, debug_dir, name):
        """
        :Description: MockupGen is a 2d mock up generator object designed for 2d storefront generation
        :param debug_dir: directory where logs and debug files will be kept
        :type debug_dir: str
        :param name: instance name - store name
        :type name: str
        """
        self.__log = MFLogger.MFLogger(debug_dir, name)
        self.__log.info("MF instance initializing..")
        self.__name = name
        self.__prod_file_names = ["BabyBodySuit.jpg", "IphoneCase.jpg", "LadiesTank.jpg",
                                  "t-shirt.png", "PillowSquare.jpg", "Socks.jpg",
                                  "Sweatshirt.jpg", "ToteBag.jpg"]
        self.__prod_dir = os.path.join(r"D:\Dev\Resources", "Products")
        self.__prod_mask_dir = os.path.join(self.__prod_dir, "Masks")
        self.__logos_dir = os.path.join(r"D:\Dev\Resources", "Images for products")
        self.__logo_arr = []
        self.__product_arr = []
        self.__product_mask_arr = []
        self.__log.info("MF instance initialized.")

    def logo_loader(self):
        self.__log.info("Logo loader started..")
        logo_filenames = glob.glob(os.path.join(self.__logos_dir, "*.jpg"))
        logo_filenames.extend(glob.glob(os.path.join(self.__logos_dir, "*.jpeg")))
        logo_filenames.extend(glob.glob(os.path.join(self.__logos_dir, "*.png")))
        self.__log.info("Loading %d logos from %s" % (len(logo_filenames), self.__logos_dir))
        self.__logo_arr = [None for _ in range(len(logo_filenames))]
        self.__logo_arr = io_functions.load_img_array(logo_filenames, threads=6)
        self.__log.info("Logos loaded")

    def product_loader(self):
        self.__log.info("Product loader started..")
        prod_filenames = []
        prod_filenames.extend(glob.glob(os.path.join(self.__prod_dir, _)) for _ in self.__prod_file_names)
        prod_filenames = [_[0] for _ in prod_filenames]
        self.__log.info("Loading %d products from %s" % (len(prod_filenames), self.__logos_dir))
        self.__product_arr = [None for _ in range(len(prod_filenames))]
        self.__product_arr = io_functions.load_img_array(prod_filenames, load_mode=cv2.CV_LOAD_IMAGE_UNCHANGED, threads=6)
        self.__log.info("Products loaded")

    def product_mask_loader(self):
        self.__log.info("Mask loader started..")
        mask_filenames = glob.glob(os.path.join(self.__prod_mask_dir, "*.png"))
        self.__log.info("Loading %d masks from %s" % (len(mask_filenames), self.__logos_dir))
        self.__product_mask_arr = [None for _ in range(len(mask_filenames))]
        self.__product_mask_arr = io_functions.load_img_array(mask_filenames, threads=6)
        self.__log.info("Masks loaded")

    def apply_logo(self, logo_idx, prod_idx):

        self.__log.info("Applying logo #%d to product %d" % (logo_idx, prod_idx))
        prod = self.__product_arr[prod_idx].astype(numpy.float32)
        prod_mask = self.__product_mask_arr[prod_idx].astype(numpy.float)
        logo = self.__logo_arr[logo_idx].astype(numpy.float)
        logo = cv2.resize(logo, prod.shape[:-1][::-1])

        alpha = numpy.full(prod.shape[:-1], 255.0, dtype=numpy.float)
        alpha = alpha[:, :, numpy.newaxis]
        if not prod.shape[2] == 4:
            prod = numpy.concatenate((prod, alpha), axis=-1)
        # if not prod_mask.shape[2] == 4:
        #     prod_mask = numpy.concatenate((prod_mask, alpha), axis=-1)
        if not logo.shape[2] == 4:
            logo = numpy.concatenate((logo, alpha), axis=-1)

        blended = blend_modes.multiply(prod_mask, logo, 1.0)
        # blended = blend_modes.multiply(prod, blended, 0.8)
        blended = blend_modes.multiply(prod, blended, 1.0)
        # added = blend_modes.addition(no_shirt, blended, 1.0)

        if 1:
            curr_dir = os.path.join(r"D:\Dev\Resources\Tests", "%d" % logo_idx)
            if not os.path.exists(curr_dir):
                os.mkdir(curr_dir)

            cv2.imwrite(os.path.join(curr_dir, "%d_%d.jpg" % (logo_idx, prod_idx)), blended.astype(numpy.uint8))

            # cv2.namedWindow("window", cv2.WINDOW_NORMAL)
            # cv2.imshow('window', blended.astype(numpy.uint8))
            # cv2.waitKey()

        self.__log.info("Done applying logo #%d to product %d" % (logo_idx, prod_idx))

    def apply_logo_with_shadows(self, logo_idx, prod_idx):

        self.__log.info("Applying logo #%d to product %d" % (logo_idx, prod_idx))
        prod = self.__product_arr[prod_idx].astype(numpy.float32)
        prod_mask = self.__product_mask_arr[prod_idx].astype(numpy.float)
        shadows = cv2.imread(r"D:\Dev\Resources\Products\Shadows\t-shirt.png", cv2.CV_LOAD_IMAGE_UNCHANGED)
        logo = self.__logo_arr[logo_idx].astype(numpy.float)

        first_row = numpy.transpose(prod_mask[:, :, 3].nonzero())[0][0]
        last_row = numpy.transpose(prod_mask[:, :, 3].nonzero())[-1][0]

        new_height = last_row - first_row
        height_aspect = int(new_height / logo.shape[0])
        new_width = int(logo.shape[1] * height_aspect)

        logo = cv2.resize(logo, prod.shape[:-1][::-1])

        alpha = numpy.full(prod.shape[:-1], 255.0, dtype=numpy.float)
        alpha = alpha[:, :, numpy.newaxis]
        if not prod.shape[2] == 4:
            prod = numpy.concatenate((prod, alpha), axis=-1)
        # if not prod_mask.shape[2] == 4:
        #     prod_mask = numpy.concatenate((prod_mask, alpha), axis=-1)
        if not logo.shape[2] == 4:
            logo = numpy.concatenate((logo, alpha), axis=-1)

        blended = blend_modes.multiply(prod_mask, logo, 1.0)
        # blended = blend_modes.multiply(prod, blended, 0.8)
        blended = blend_modes.multiply(prod, blended, 1.0)
        # added = blend_modes.addition(no_shirt, blended, 1.0)

        if 1:
            curr_dir = os.path.join(r"D:\Dev\Resources\Tests", "%d" % logo_idx)
            if not os.path.exists(curr_dir):
                os.mkdir(curr_dir)

            cv2.imwrite(os.path.join(curr_dir, "%d_%d.jpg" % (logo_idx, prod_idx)), blended.astype(numpy.uint8))

            # cv2.namedWindow("window", cv2.WINDOW_NORMAL)
            # cv2.imshow('window', blended.astype(numpy.uint8))
            # cv2.waitKey()

        self.__log.info("Done applying logo #%d to product %d" % (logo_idx, prod_idx))

    def run_factory(self):
        self.__log.info("Applying %d logos to %d products (%d operations)" % (len(self.__logo_arr),
                                                                              len(self.__product_arr),
                                                                              len(self.__logo_arr) *
                                                                              len(self.__product_arr)
                                                                              ))
        # for logo_idx in range(len(self.__logo_arr)):
        #     for prod_idx in range(len(self.__product_arr)):
        #         self.apply_logo(logo_idx, prod_idx)

        self.__log.info("Done applying all logos to all products!")
