import cv2.aruco
from cv2 import cv2

from src.cv_module import consts
from src.cv_module.cv_utils.aruco_utils import find_aruco_origin
from src.cv_module.HSV_settings.HSV_settings import hsv_settings
from src.cv_module.cv_utils import *
from src.exceptions.cv_exceptions import *
from .Link import Link


# noinspection PyTypeChecker
class Mechanism:
    links = []
    initial_link = Link

    def __init__(self, path_to_file, debug_mode=consts.DebugMode.DEBUG_OFF):
        self.debug_mode = debug_mode
        if debug_mode != consts.DebugMode.DEBUG_OFF:
            cv2.namedWindow('debug')

        # Initiating some constant parameters to operate ArUco
        self.aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        self.aruco_parameters = cv2.aruco.DetectorParameters_create()

        # Checking if the video meets our requirements
        self.video = cv2.VideoCapture(path_to_file)
        if not self.video.isOpened():
            raise FailedToOpenVideo

        fps = self.video.get(cv2.CAP_PROP_FPS)
        if fps < consts.MIN_FPS_REQUIRED:
            raise LowFPSVideo

        total_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        if total_frames < consts.MIN_FRAMES_COUNT:
            raise TooShortVideo

    def __del__(self):
        self.video.release()

    # Add link to the Mechanism. Can be used before research, on the configuring stage.
    def set_new_link(self, link_color, points, is_initial):
        link = Link(link_color, points, is_initial)
        if is_initial:
            self.initial_link = link
        else:
            self.links.append(link)

    # Researches provided video input after mechanism is configured and ready to go. This method returns nothing,
    # but it affects on Mechanism's inner instances and makes it real to work with Link's data arrays
    def research_input(self):
        # Some debugging-purpose vars.
        missed_in_a_row = 0
        max_missed = 0
        missed_total = 0
        frames_num = 0
        missed_by_aruco = 0

        while True:
            frame_read, start_frame = self.video.read()
            frames_num += 1
            if not frame_read:
                break

            origin = find_aruco_origin(start_frame, self.aruco_dictionary, self.aruco_parameters)
            if not origin:
                missed_in_a_row += 1
                missed_by_aruco += 1
                missed_total += 1
                if self.debug_mode == consts.DebugMode.DEBUG_FULL:
                    show('debug', start_frame)
                continue

            # First we are researching the initial link. It has it's own property in the Mechanism class and is needed
            # to be researched to extract omega angle to further processing
            initial_ok, omega = self.initial_link.research_link(start_frame, origin)
            if not initial_ok or not omega:
                missed_in_a_row += 1
                missed_total += 1

                # If the full debugging mode is ON, we are able to correct HSV bounds settings, testing it on
                # the current frame
                if self.debug_mode == consts.DebugMode.DEBUG_FULL:
                    hsv_settings(start_frame, self.initial_link.color_bounds)
                continue

            # Then we are researching the other links one by one
            for link in self.links:
                link_ok, _ = link.research_link(start_frame, origin, omega)
                if not link_ok:
                    missed_in_a_row += 1
                    missed_total += 1
                    if self.debug_mode == consts.DebugMode.DEBUG_FULL:
                        hsv_settings(start_frame, link.color_bounds)

            # Debugging statistics collecting again
            if missed_in_a_row > max_missed:
                max_missed = missed_in_a_row
            missed_in_a_row = 0

            # Debugging video show frame by frame while processing them
            if self.debug_mode != consts.DebugMode.DEBUG_OFF:
                cv2.imshow('debug', start_frame)
                ch = cv2.waitKey(consts.TIME_TO_READ_INPUT)
                if ch == consts.ESC_KEY_CODE:
                    break

        # Debugging info again.
        if self.debug_mode != consts.DebugMode.DEBUG_OFF:
            print('frames: ', frames_num)
            print('final dots: ', len(self.initial_link.points[0].path.dots))
            print('total missed: ', missed_total)
            print('missed by aruco: ', missed_by_aruco)
