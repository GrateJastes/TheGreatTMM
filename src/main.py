from cv2 import cv2
import numpy as np


def minimize(img, scale):
    return cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)), cv2.INTER_AREA)


def find_red_marker(image):
    blurred = cv2.GaussianBlur(image, (3, 3), 0)


def show(header, img):
    cv2.imshow(header, img)
    cv2.waitKey(0)


def main():
    img = cv2.imread('../assets/test2.jpg', cv2.IMREAD_COLOR)
    img = minimize(img, 2.5)
    # cropped = img[182:545, 60:470]
    show('start', img)

    result = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 200, 0])
    upper_red = np.array([10, 255, 255])
    mask_red = cv2.inRange(img, lower_red, upper_red)
    # result = cv2.bitwise_and(src=result, mask=mask)
    lower_blue = np.array([110, 150, 0])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(img, lower_blue, upper_blue)

    show('mask red', mask_red)
    show('mask blue', mask_blue)
    # show('result', result)


    # b, g, r = cv2.split(cropped)
    #
    # _, thresh_b = cv2.threshold(b, 70, 255, cv2.THRESH_BINARY)
    # _, thresh_g = cv2.threshold(g, 70, 255, cv2.THRESH_BINARY)
    # _, thresh_r = cv2.threshold(r, 100, 255, cv2.THRESH_BINARY)
    #
    # show('r', r)
    # show('thresh_r', thresh_r)
    # # show('g', g)
    # # show('b', b)
    # # show('thresh_b', thresh_b)
    # # show('thresh_g', thresh_g)
    #
    # merged = cv2.merge([b, g, thresh_r])
    # _, _, only_red = cv2.split(merged)
    # _, red_marker = cv2.threshold(only_red, 254, 255, cv2.THRESH_BINARY_INV)
    #
    # show('merged', merged)
    # show('only red', only_red)


main()
