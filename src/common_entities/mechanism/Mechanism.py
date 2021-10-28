from PyQt5.QtWidgets import QProgressBar
from cv2 import cv2
import cv2.aruco

from src.cv_module import consts
from .Link import Link

# noinspection PyTypeChecker
from .. import Dot
from ...cv_module.cv_utils import distance


class Mechanism:
    def __init__(self, path_to_file):
        self.video = cv2.VideoCapture(path_to_file)
        self.initial_link = None
        self.links = []
        self.origin = None

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
    def research_input(self, progress_bar: QProgressBar = None):
        self.process_video_input(progress_bar)
        self.find_origin(self.first_circle_dots())
        self.traverse_all_coordinates()
        self.find_all_omegas()

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
        i = 0

        while True:
            frame_read, start_frame = self.video.read()
            if not frame_read:
                break

            # First we are researching the initial link. It has it's own property in the Mechanism class and is needed
            # to be researched to extract omega angle to further processing
            initial_ok = self.initial_link.research_link(start_frame)
            if not initial_ok:
                self.initial_link.miss_frame()
                print(i)

            # Then we are researching the other links one by one
            for link in self.links:
                link_ok = link.research_link(start_frame)
                if not link_ok:
                    link.miss_frame()

            i += 1
            if i % (frame_per_percent + 1) == 0 and progress_bar is not None:
                progress_bar.setValue(i)

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
