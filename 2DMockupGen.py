import os
import cv2
import glob


class LogoTransfer(object):

    def __init__(self):
        self.__resource_folder = r"D:\Projects\ProductRocks\RnD\Resources\Products"
        self.__resource_names = ["IphoneCaseWhite", "Pillow", "TanktopWhite"]
        self.__resource_files = [os.path.join(self.__resource_folder, _ + ".jpg") for _ in self.__resource_names]
        self.__resource_masks = [os.path.join(self.__resource_folder, _ + "_Mask.jpg") for _ in self.__resource_names]
        self.__logos_jpg = glob.glob(os.path.join(r"D:\Projects\ProductRocks\RnD\Resources\Images for products",
                                                  "*.jpg"))
        self.__logos_jpg.extend(glob.glob(os.path.join(r"D:\Projects\ProductRocks\RnD\Resources\Images for products",
                                                       "*.jpeg")))
        self.__logos_png = (glob.glob(os.path.join(r"D:\Projects\ProductRocks\RnD\Resources\Images for products",
                                                   "*.png")))
        self.__resource_shapes = [cv2.imread(_, cv2.CV_LOAD_IMAGE_UNCHANGED).shape for _ in self.__resource_files]

    def resize_images(self):
        pass

lt = LogoTransfer()
print lt
# for _ in self.__resource_masks:
        #     im = cv2.imread(_, cv2.CV_LOAD_IMAGE_UNCHANGED)
        #     cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        #     cv2.imshow("Image", im)
        #     cv2.waitKey(0)
