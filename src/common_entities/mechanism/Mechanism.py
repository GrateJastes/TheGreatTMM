from __future__ import annotations

import numpy as np
from scipy.optimize import fmin
from scipy.spatial.distance import cdist
from PyQt5.QtWidgets import QProgressBar

from cv2 import cv2
import cv2.aruco

from src.cv_module import consts
from .Link import Link

# noinspection PyTypeChecker
from .. import Dot, Point
from ...cv_module.cv_utils import distance, minimize, rescale


class Mechanism:
    video: cv2.VideoCapture
    initial_link: Link
    links: list[Link]
    origin: tuple[int, int]
    demo_frame: np.ndarray
    demo_frame_index: int
    preview_image: np.ndarray

    aruco_dict: cv2.aruco_Dictionary
    aruco_params: cv2.aruco_DetectorParameters
    last_scale: float
    first_scale: float
    demo_frame_scale: float

    def __init__(self, path_to_file):
        self.video = cv2.VideoCapture(path_to_file)
        self.links = []

        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters_create()

    def __del__(self):
        self.video.release()

    # Add link to the Mechanism. Can be used before research, on the configuring stage.
    def set_new_link(self,
                     link_color: tuple[int, int, int],
                     points: list[Point],
                     is_initial: bool,
                     link_id=0) -> None:
        link = Link(link_color, points, is_initial, link_id)
        if is_initial:
            self.initial_link = link
        else:
            self.links.append(link)

    # Researches provided video input after mechanism is configured and ready to go. This method returns nothing,
    # but it affects on Mechanism's inner instances and makes it real to work with Link's data arrays
    def research_input(self, progress_bar: QProgressBar = None) -> None:
        self.process_video_input(progress_bar)
        self.find_origin(self.first_circle_dots())
        self.traverse_all_coordinates()
        # self.peaks_removing()
        self.points_optimization()
        self.find_all_omegas()

        if progress_bar is not None:
            progress_bar.setValue(consts.PROGRESS_BAR_MAX)

    def research_analogs(self) -> None:
        initial_point = self.initial_link.points[0]
        initial_point.point_analysis(initial_point)

        for link in self.links:
            for point in link.points:
                point.point_analysis(initial_point)

    def process_video_input(self, progress_bar: QProgressBar = None):
        scale_found = False
        scaling_start_index = 0

        total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_per_percent = int(total_frames / consts.PROGRESS_BAR_MAX)
        frame_index = -1

        demo_frame_ready = False
        while True:
            frame_is_full = True

            frame_read, start_frame = self.video.read()
            if not frame_read:
                break
            frame_index += 1

            self.refresh_scale(start_frame)
            if self.last_scale is not None and not scale_found:
                scale_found = True
                self.first_scale = self.last_scale
                scaling_start_index = frame_index

            # First we are researching the initial link. It has it's own property in the Mechanism class and is needed
            # to be researched to extract omega angle to further processing
            initial_ok = self.initial_link.research_link(start_frame, self.last_scale)
            if not initial_ok:
                self.initial_link.miss_frame()
                frame_is_full = False

            # Then we are researching the other links one by one
            for link in self.links:
                link_ok = link.research_link(start_frame, self.last_scale)
                if not link_ok:
                    link.miss_frame()
                    frame_is_full = False

            if not demo_frame_ready and frame_is_full:
                self.demo_frame = start_frame
                self.demo_frame_index = frame_index
                self.demo_frame_scale = self.last_scale

            if frame_index % (frame_per_percent + 1) == 0 and progress_bar is not None:
                progress_bar.setValue(frame_index / frame_per_percent)

        self.preview_image = self.get_preview_image()
        self.rescale_links(scaling_start_index)

    def rescale_links(self, scaling_start_index: int) -> None:
        if self.first_scale is None or scaling_start_index == 0:
            return

        for i in range(scaling_start_index + 1):
            base_dot = self.initial_link.points[0].path.dots[i]
            new_base_coords = rescale((base_dot.x, base_dot.y), self.first_scale)
            base_dot.x = new_base_coords[0]
            base_dot.y = new_base_coords[1]

            for link in self.links:
                for point in link.points:
                    dot = point.path.dots[i]
                    new_coords = rescale((dot.x, dot.y), self.first_scale)
                    dot.x = new_coords[0]
                    dot.y = new_coords[1]

    def refresh_scale(self, frame: np.ndarray) -> None:
        markerCorners, markerIds, rejectedCandidates = \
            cv2.aruco.detectMarkers(frame, self.aruco_dict, parameters=self.aruco_params)

        if markerIds is None:
            return

        x = Dot(markerCorners[0][0][0][0], markerCorners[0][0][0][1])
        y = Dot(markerCorners[0][0][2][0], markerCorners[0][0][2][1])

        self.last_scale = consts.ARUCO_SCALING_DIAG_MM / distance(x, y)

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

    def find_origin(self, first_circle_dots: list[Dot]) -> None:
        initial_dots = first_circle_dots
        x = np.array([dot.x for dot in initial_dots])
        y = np.array([dot.y for dot in initial_dots])

        xm = x.mean()
        ym = y.mean()

        cm = np.array([xm, ym]).reshape(1, 2)
        rm = cdist(cm, np.array([x, y]).T).mean()

        def err(average_values):
            pts = [np.linalg.norm([x0 - average_values[0],
                                   y0 - average_values[1]])
                   - average_values[2] for x0, y0 in zip(x, y)]
            return (np.array(pts) ** 2).sum()

        xf, yf, rf = fmin(err, x0=[xm, ym, rm], disp=False)

        self.origin = (int(xf), int(yf))

    def traverse_all_coordinates(self) -> None:
        for dot in self.initial_link.points[0].path.dots:
            dot.traverse_coords(self.origin)

        for link in self.links:
            for point in link.points:
                for dot in point.path.dots:
                    dot.traverse_coords(self.origin)

    def find_all_omegas(self) -> None:
        for dot in self.initial_link.points[0].path.dots:
            dot.set_self_omega()

        for link in self.links:
            for point in link.points:
                for i, dot in enumerate(point.path.dots):
                    dot.omega = self.initial_link.points[0].path.dots[i].omega

    def get_preview_image(self) -> np.ndarray:
        self.initial_link.draw_on_frame(self.demo_frame, self.demo_frame_index, self.demo_frame_scale)

        for link in self.links:
            link.draw_on_frame(self.demo_frame, self.demo_frame_index, self.demo_frame_scale)

        width = self.video.get(3)
        height = self.video.get(4)

        minimize_index = round(max([width / consts.PREVIEW_WINDOW_W, height / consts.PREVIEW_WINDOW_H]))
        if minimize_index == 0:
            minimize_index = 1

        return minimize(self.demo_frame, min([3, minimize_index]))
        # return self.demo_frame

    @staticmethod
    def video_fits(filename: str) -> bool:
        return True
        # video = cv2.VideoCapture(filename)
        # try:
        #     if not video.isOpened():
        #         return False
        #
        #     fps = video.get(cv2.CAP_PROP_FPS)
        #     if fps < consts.MIN_FPS_REQUIRED:
        #         return False
        #
        #     total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        #     if total_frames < consts.MIN_FRAMES_COUNT:
        #         return False
        #
        #     return True
        # finally:
        #     video.release()

    def peaks_removing(self):
        self.initial_link.points[0].restore_dots()
        self.initial_link.points[0].remove_dot_repeat()
        data = self.initial_link.points[0].path.dots
        for prevdot, dot, nextdot in zip(data, data[1:], data[2:]):
            ax, ay = nextdot.x - dot.x, nextdot.y - dot.y
            bx, by = prevdot.x - dot.x, prevdot.y - dot.y
            len_a, len_b = np.sqrt(ax ** 2 + ay ** 2), np.sqrt(bx ** 2 + by ** 2)
            cos_ab = (ax * bx + ay * by) / (len_a * len_b)
            angle = np.arccos(cos_ab)
            if angle <= consts.MIN_ANGLE:
                self.initial_link.points[0].path.dots.remove(dot)
        for link in self.links:
            for point in link.points:
                data = point.path.dots
                for prevdot, dot, nextdot in zip(data, data[1:], data[2:]):
                    ax, ay = nextdot.x - dot.x, nextdot.y - dot.y
                    bx, by = prevdot.x - dot.x, prevdot.y - dot.y
                    len_a, len_b = np.sqrt(ax ** 2 + ay ** 2), np.sqrt(bx ** 2 + by ** 2)
                    cos_ab = (ax * bx + ay * by) / (len_a * len_b)
                    angle = np.arccos(cos_ab)
                    if angle <= consts.MIN_ANGLE:
                        dot.x, dot.y = None, None

    def points_optimization(self):
        for link in self.links:
            for point in link.points:
                if len(point.path.dots) != len(self.initial_link.points[0].path.dots):
                    print('path of different lengths:', point.name, self.initial_link.points[0].name)
        self.initial_link.points[0].restore_dots()
        self.initial_link.points[0].remove_dot_repeat()
        for link in self.links:
            for point in link.points:
                point.restore_dots()
                point.remove_dot_repeat()
