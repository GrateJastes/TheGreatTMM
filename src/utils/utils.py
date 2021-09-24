from cv2 import cv2


def minimize(img, scale):
    return cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)), cv2.INTER_AREA)


def show(header, img):
    cv2.imshow(header, img)
    cv2.waitKey()
