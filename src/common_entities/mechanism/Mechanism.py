import numpy as np
from PyQt5.QtWidgets import QProgressBar
from cv2 import cv2
import cv2.aruco

from src.cv_module import consts
from .Link import Link

# noinspection PyTypeChecker
from .. import Dot
from ...cv_module.cv_utils import distance, minimize, remove_jumps


class Mechanism:
    def __init__(self, path_to_file):
        self.video = cv2.VideoCapture(path_to_file)
        self.initial_link = None
        self.links = []
        self.origin = None
        self.demonstration_frame = None
        self.demonstration_frame_num = None
        self.preview_image = None
        self.hsv_settings_window = None
        self.hsv_preview_window = None
        self.current_hsv_frame = None

    def __del__(self):
        self.video.release()

    # Add link to the Mechanism. Can be used before research, on the configuring stage.
    def set_new_link(self, link_color, points, is_initial, link_id=0):
        link = Link(link_color, points, is_initial, link_id)
        if is_initial:
            self.initial_link = link
        else:
            self.links.append(link)

    # Researches provided video input after mechanism is configured and ready to go. This method returns nothing,
    # but it affects on Mechanism's inner instances and makes it real to work with Link's data arrays
    def research_input(
            self,
            progress_bar: QProgressBar = None,
            hsv_settings_window=None,
            hsv_preview_window=None,
    ):
        self.process_video_input(progress_bar)
        self.find_origin(self.first_circle_dots())
        self.traverse_all_coordinates()
        self.find_all_omegas()
        self.hsv_preview_window = hsv_preview_window
        self.hsv_settings_window = hsv_settings_window

        if consts.DEBUG:
            self.start_hsv_settings()

        # remove_jumps(self.initial_link.points[0].path.dots)

        for link in self.links:
            for point in link.points:
                remove_jumps(point.path.dots)

        if progress_bar is not None:
            progress_bar.setValue(consts.PROGRESS_BAR_MAX)

    def research_analogs(self):
        initial_point = self.initial_link.points[0]
        initial_point.point_analysis(initial_point)

        for link in self.links:
            for point in link.points:
                point.point_analysis(initial_point)

    def process_video_input(self, progress_bar: QProgressBar = None):
        total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_per_percent = int(total_frames / consts.PROGRESS_BAR_MAX)
        frame_num = 0

        demonstration_frame_ready = False
        while True:
            frame_is_full = True

            frame_read, start_frame = self.video.read()
            if not frame_read:
                break

            # First we are researching the initial link. It has it's own property in the Mechanism class and is needed
            # to be researched to extract omega angle to further processing
            initial_ok = self.initial_link.research_link(start_frame)
            if not initial_ok:
                self.initial_link.miss_frame()
                frame_is_full = False

            # Then we are researching the other links one by one
            for link in self.links:
                link_ok = link.research_link(start_frame)
                if not link_ok:
                    link.miss_frame()
                    frame_is_full = False

            if not demonstration_frame_ready and frame_is_full:
                self.demonstration_frame = start_frame
                self.demonstration_frame_num = frame_num
                frame_is_full = True

            frame_num += 1
            if frame_num % (frame_per_percent + 1) == 0 and progress_bar is not None:
                progress_bar.setValue(frame_num / frame_per_percent)

        self.preview_image = self.get_preview_image()

    def first_circle_dots(self) -> list[Dot]:
        movement_started = False
        circle_started = False
        finish_started = False

        dots_after_finish = consts.DOTS_AFTER_CIRCLE
        initial_dots = self.initial_link.points[0].path.dots
        first_dot = None
        result_dots = []

        for dot in initial_dots:
            if dot.x is not None:
                first_dot = dot
                result_dots.append(first_dot)
                break

        for i, dot in enumerate(initial_dots):
            if dot.x is None:
                continue
            if not movement_started and distance(dot, first_dot) < consts.MIN_DIST_TO_MOVE:
                continue

            if not movement_started:
                movement_started = True
                continue

            if distance(dot, first_dot) < consts.MIN_DIST_TO_START and not circle_started:
                continue

            if not circle_started:
                circle_started = True
                continue

            if distance(dot, first_dot) < consts.MIN_CLOSURE_DIST or finish_started:
                if not finish_started:
                    finish_started = True
                if dots_after_finish == 0:
                    break

                dots_after_finish -= 1

            result_dots.append(dot)

        return result_dots

    def find_origin(self, first_circle_dots: list[Dot]):
        # initial_dots = self.initial_link.points[0].path.dots
        initial_dots = first_circle_dots

        sumX = 0
        sumY = 0

        missedDots = 0

        for dot in initial_dots:
            if dot.x is None:
                missedDots += 1
                continue

            sumX += dot.x
            sumY += dot.y

        foundDots = (len(initial_dots) - missedDots)
        originX = sumX / foundDots
        originY = sumY / foundDots

        self.origin = (int(originX), int(originY))

    def traverse_all_coordinates(self):
        for dot in self.initial_link.points[0].path.dots:
            dot.traverse_coords(self.origin)

        for link in self.links:
            for point in link.points:
                for dot in point.path.dots:
                    dot.traverse_coords(self.origin)

    def find_all_omegas(self):
        for dot in self.initial_link.points[0].path.dots:
            dot.set_self_omega()

        for link in self.links:
            for point in link.points:
                for i, dot in enumerate(point.path.dots):
                    dot.omega = self.initial_link.points[0].path.dots[i].omega

    def get_preview_image(self):
        self.initial_link.draw_on_frame(self.demonstration_frame, self.demonstration_frame_num)

        for link in self.links:
            link.draw_on_frame(self.demonstration_frame, self.demonstration_frame_num)

        return minimize(self.demonstration_frame, consts.PREVIEW_MINIMIZATION_SCALE)

    def update_hsv_settings(self, hsv):
        trackers_info = self.hsv_settings_window.get_trackers_info()
        lower = (trackers_info['h1'], trackers_info['s1'], trackers_info['v1'])
        upper = (trackers_info['h2'], trackers_info['s2'], trackers_info['v2'])
        h_min = np.array(lower, np.uint8)
        h_max = np.array(upper, np.uint8)

        thresh = cv2.inRange(hsv, h_min, h_max)

        self.hsv_preview_window.show_image(thresh)

    def setup_hsv_settings_frame(self, frame, color_bounds):
        self.hsv_settings_window.set_trackers_values(color_bounds)
        self.current_hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.update_hsv_settings(self.current_hsv_frame)

    def get_frame(self, frame_num):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_num - 1)
        _, frame = self.video.read()

        return frame

    def start_hsv_settings(self):
        link = self.links[0]

        window_set_up = False
        color_bounds = consts.get_bound_colors(link.color)
        for idx, dot in enumerate(link.points[0].path.dots):
            if not window_set_up and dot.x is None:
                self.setup_hsv_settings_frame(self.get_frame(idx), color_bounds)
                break

    @staticmethod
    def video_fits(filename: str) -> bool:
        video = cv2.VideoCapture(filename)
        try:
            if not video.isOpened():
                return False

            fps = video.get(cv2.CAP_PROP_FPS)
            if fps < consts.MIN_FPS_REQUIRED:
                return False

            total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            if total_frames < consts.MIN_FRAMES_COUNT:
                return False

            return True
        finally:
            video.release()
