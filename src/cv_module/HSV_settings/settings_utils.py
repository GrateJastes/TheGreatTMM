from cv2 import cv2


def noop(*arg):
    pass


def create_trackers(window_name):
    cv2.createTrackbar('h1', window_name, 0, 255, noop)
    cv2.createTrackbar('s1', window_name, 0, 255, noop)
    cv2.createTrackbar('v1', window_name, 0, 255, noop)
    cv2.createTrackbar('h2', window_name, 255, 255, noop)
    cv2.createTrackbar('s2', window_name, 255, 255, noop)
    cv2.createTrackbar('v2', window_name, 255, 255, noop)


def get_trackers_info(window_name):
    h1 = cv2.getTrackbarPos('h1', window_name)
    s1 = cv2.getTrackbarPos('s1', window_name)
    v1 = cv2.getTrackbarPos('v1', window_name)
    h2 = cv2.getTrackbarPos('h2', window_name)
    s2 = cv2.getTrackbarPos('s2', window_name)
    v2 = cv2.getTrackbarPos('v2', window_name)

    return h1, s1, v1, h2, s2, v2
