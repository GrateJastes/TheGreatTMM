import cv2.aruco
from cv2 import cv2

from src.cv_module import consts
from src.cv_module.cv_utils.aruco_utils import find_aruco_origin
from src.cv_module.HSV_settings.HSV_settings import hsv_settings
from src.cv_module.cv_utils import *
from src import common
from src.exceptions.cv_exceptions import *
from src.cv_module.cv_utils.geometry import ellipse_area


class Link:
    is_initial = bool
    points = [common.Point]

    def __init__(self, color, points, is_initial=False):
        self.color = color
        self.points = points
        self.is_initial = is_initial

        self.color_bounds = consts.get_bound_colors(color)

    def research_link(self, start_frame, origin, omega=None):
        research_ok = True
        frame = prepare_frame(start_frame, self.color_bounds)
        contours, _ = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            research_ok = False
            return research_ok, None

        signatures = find_marker_signatures(contours)
        if not signatures:
            research_ok = False
            return research_ok, None

        signatures.sort(key=ellipse_area, reverse=True)

        if self.is_initial:
            marker = traverse_coordinates((int(signatures[0][0][0]), int(signatures[0][0][1])), origin)
            found_omega = find_omega(marker)
            self.points[0].path.append(marker, found_omega)
            return research_ok, found_omega

        markers = [traverse_coordinates((int(ellipse[0][0]), int(ellipse[0][1])), origin) for ellipse in signatures]
        last_dots = [point.path.last_dot for point in self.points]
        matches, rest_markers = self.__find_matches(last_dots, markers)
        if len(matches) + len(rest_markers) < len(self.points):
            research_ok = False

        rest_markers_iter = iter(rest_markers)

        for point in self.points:
            if point.path.last_dot is None:
                research_ok = False
                try:
                    point.path.append(next(rest_markers_iter), omega)
                    research_ok = True
                except StopIteration:
                    continue
            if point.path.last_dot in matches.keys():
                point.path.append(matches[point.path.last_dot], omega)
                research_ok = True

        return research_ok, None

    def __find_matches(self, last_dots, markers):
        markers_to_dots_closests = {}
        dots_to_markers_closests = {}
        final_matches = {}  # markers to dots

        for last_dot in last_dots:
            if last_dot is None:
                continue

            closest_marker = find_closest(last_dot, markers)
            markers_to_dots_closests[last_dot] = closest_marker
        for marker in markers:
            closest_dot = find_closest(marker, last_dots)
            dots_to_markers_closests[marker] = closest_dot
        for last_dot in markers_to_dots_closests:
            marker_candidate = markers_to_dots_closests[last_dot]
            if dots_to_markers_closests[marker_candidate] == last_dot:
                final_matches[last_dot] = marker_candidate
                markers.remove(marker_candidate)
                last_dots.remove(last_dot)

        return final_matches, markers


# noinspection PyTypeChecker
class Mechanism:
    links = []
    initial_link = Link

    def __init__(self, path_to_file, debug_mode=consts.DebugMode.DEBUG_OFF):
        self.debug_mode = debug_mode
        if debug_mode != consts.DebugMode.DEBUG_OFF:
            cv2.namedWindow('debug')

        self.aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        self.aruco_parameters = cv2.aruco.DetectorParameters_create()

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

    def set_new_link(self, link_color, points, is_initial):
        link = Link(link_color, points, is_initial)
        if is_initial:
            self.initial_link = link
        else:
            self.links.append(link)

    def research_input(self):
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

            initial_ok, omega = self.initial_link.research_link(start_frame, origin)
            if not initial_ok or not omega:
                missed_in_a_row += 1
                missed_total += 1

                if self.debug_mode == consts.DebugMode.DEBUG_FULL:
                    hsv_settings(start_frame, self.initial_link.color_bounds)
                continue

            for link in self.links:
                link_ok, _ = link.research_link(start_frame, origin, omega)
                if not link_ok:
                    missed_in_a_row += 1
                    missed_total += 1
                    if self.debug_mode == consts.DebugMode.DEBUG_FULL:
                        hsv_settings(start_frame, link.color_bounds)

            if missed_in_a_row > max_missed:
                max_missed = missed_in_a_row
            missed_in_a_row = 0

            if self.debug_mode != consts.DebugMode.DEBUG_OFF:
                cv2.imshow('debug', start_frame)
                ch = cv2.waitKey(consts.TIME_TO_READ_INPUT)
                if ch == consts.ESC_KEY_CODE:
                    break

        if self.debug_mode != consts.DebugMode.DEBUG_OFF:
            print('frames: ', frames_num)
            print('final dots: ', len(self.initial_link.points[0].path.dots))
            print('total missed: ', missed_total)
            print('missed by aruco: ', missed_by_aruco)
