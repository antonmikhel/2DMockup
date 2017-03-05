import cv2
import numpy
from blend_modes import blend_modes

img_1 = cv2.imread(r"D:\Dev\Resources\Products\BabyBodySuit.jpg",
                   cv2.CV_LOAD_IMAGE_UNCHANGED).astype(numpy.float)
img_1_mask = cv2.imread(r"D:\Dev\Resources\Products\Masks\BabyBodySuit.png",
                        cv2.CV_LOAD_IMAGE_UNCHANGED).astype(numpy.float)
img_1_logo = cv2.imread(r"D:\Dev\Resources\Images for products\o-JILL-GREENBERG-facebook.jpg",
                        cv2.CV_LOAD_IMAGE_UNCHANGED).astype(numpy.float)
img_1_logo = cv2.resize(img_1_logo, img_1_mask.shape[:-1][::-1])

alpha = numpy.full(img_1.shape[:-1], 255.0, dtype=numpy.float)
alpha = alpha[:, :, numpy.newaxis]
img_1 = numpy.concatenate((img_1, alpha), axis=-1)
# img_1_mask = numpy.concatenate((img_1_mask, alpha), axis=-1)
img_1_logo = numpy.concatenate((img_1_logo, alpha), axis=-1)

blended = blend_modes.multiply(img_1_mask, img_1_logo, 1.0)
# blended = blend_modes.multiply(img_1, blended, 0.8)
blended = blend_modes.multiply(img_1, blended, 1.0)
# added = blend_modes.addition(no_shirt, blended, 1.0)
cv2.imwrite(r"D:\Dev\Resources\Tests\horse_BabySuit.jpg", blended.astype(numpy.uint8))
cv2.namedWindow("window", cv2.WINDOW_NORMAL)
cv2.imshow('window', blended.astype(numpy.uint8))
cv2.waitKey()
