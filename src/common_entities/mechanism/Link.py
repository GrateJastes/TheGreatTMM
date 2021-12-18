import numpy as np
from cv2 import cv2

from src import common_entities as ce
from src.cv_module import consts
from src.cv_module.cv_utils.utils import *
from src.cv_module.cv_utils.geometry import ellipse_area


# The class which represents the link of a mechanism. It can be researched independently from Mechanism in a particular
# state when the needed data is provided.
class Link:
    is_initial: bool
    points: list[ce.Point]
    link_id: int
    color: tuple[int, int, int]
    color_bounds: tuple[np.ndarray, np.ndarray]

    def __init__(self,
                 color: tuple[int, int, int],
                 points: list[ce.Point],
                 is_initial=False,
                 link_id=0):
        self.color = color
        self.points = points
        self.is_initial = is_initial
        self.link_id = link_id

        self.color_bounds = consts.get_bound_colors(color)

    def retry_with_low_red(self, start_frame) -> tuple:
        frame = prepare_frame(start_frame, consts.get_bound_colors(self.color, True, self.color_bounds))
        contours, _ = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None, None

        signatures = find_marker_signatures(contours)
        if not signatures:
            return None, None

        return contours, signatures

    def research_link(self, start_frame: np.ndarray, last_scale: float) -> bool:
        dots_accepted = 0
        got_contours_low_red = False
        got_signatures_low_red = False

        frame = prepare_frame(start_frame, self.color_bounds)
        contours, _ = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            if self.color != consts.BGR.RED:
                self.miss_frame()
                return False

            contours, _ = self.retry_with_low_red(start_frame)
            if not contours:
                self.miss_frame()
                return False
            else:
                got_contours_low_red = True

        signatures = find_marker_signatures(contours)
        if not signatures:
            if self.color != consts.BGR.RED or got_contours_low_red:
                self.miss_frame()
                return False

            _, signatures = self.retry_with_low_red(start_frame)
            if not signatures:
                self.miss_frame()
                return False
            else:
                got_signatures_low_red = True

        if got_contours_low_red or got_signatures_low_red:
            self.color_bounds = consts.get_bound_colors(self.color, True, self.color_bounds)

        signatures.sort(key=ellipse_area, reverse=True)

        if self.is_initial:
            marker = (signatures[0][0][0], signatures[0][0][1])
            marker = (int(marker[0]), int(marker[1]))

            self.points[0].path.append(marker, last_scale)

            return True

        markers = [(int(ellipse[0][0]), int(ellipse[0][1])) for ellipse in signatures]

        last_dots = [point.path.last_dot_coords for point in self.points]
        matches, rest_markers = self.__find_matches(last_dots, markers)

        rest_markers_iter = iter(rest_markers)
        for point in self.points:
            if point.path.last_dot_coords == (None, None):
                try:
                    marker = next(rest_markers_iter)

                    marker = (int(marker[0]), int(marker[1]))
                    point.path.append(marker, last_scale)
                    dots_accepted += 1
                except StopIteration:
                    pass

                continue

            if point.path.last_dot_coords in matches.keys():
                marker = matches[point.path.last_dot_coords]

                marker = (int(marker[0]), int(marker[1]))

                point.path.append(marker, last_scale)
                dots_accepted += 1

        path_len_max = max([len(p.path.dots) for p in self.points])
        for point in self.points:
            if len(point.path.dots) < path_len_max:
                point.path.append((None, None))

        if dots_accepted == len(self.points):
            return True
        else:
            return False

    def __find_matches(self,
                       last_dots: list[tuple],
                       markers: list[tuple[int, int]]
                       ) -> (dict, list[tuple[int, int]]):
        # We need to ensure that there are markers unambiguously correlated with the last
        # dots on paths and vice versa.
        markers_to_dots_closests = {}
        dots_to_markers_closests = {}

        # Only then we can append them to the final matches dictionary
        final_matches = {}  # markers to dots

        # First we are looking for markers which are closest to every dot on the ends of the paths
        for last_dot in last_dots:
            if last_dot is None or last_dot[0] is None:
                continue

            closest_marker = find_closest(last_dot, markers)
            markers_to_dots_closests[last_dot] = closest_marker

        # Then we make the opposite dictionary
        for marker in markers:
            closest_dot = find_closest(marker, last_dots)
            dots_to_markers_closests[marker] = closest_dot

        # And finally we compare existing dictionaries, extracting only those pairs, which have their counterpart in
        # the other dict
        for last_dot in markers_to_dots_closests:
            marker_candidate = markers_to_dots_closests[last_dot]
            if dots_to_markers_closests[marker_candidate] == last_dot:
                final_matches[last_dot] = marker_candidate
                markers.remove(marker_candidate)
                last_dots.remove(last_dot)

        # After all we return the confirmed matches and the markers which don't have any close 'last dots' to them
        return final_matches, markers

    def miss_frame(self) -> None:
        for point in self.points:
            point.path.append((None, None))

    def draw_on_frame(self, frame: np.ndarray, frame_num: int, scale: float) -> None:
        print("drawing: ", self.link_id)
        for point in self.points:
            if len(point.path.dots) < frame_num + 1:
                continue
            point_coords = rescale((
                point.path.dots[frame_num].x,
                point.path.dots[frame_num].y,
            ), 1. / scale)
            text_coords = rescale((
                point.path.dots[frame_num].x + consts.PREVIEW_POINT_TEXT_SHIFT,
                point.path.dots[frame_num].y - consts.PREVIEW_POINT_TEXT_SHIFT,
            ), 1. / scale)

            point_coords = (int(point_coords[0]), int(point_coords[1]))
            text_coords = (int(text_coords[0]), int(text_coords[1]))

            cv2.circle(
                frame,
                point_coords,
                consts.PREVIEW_POINT_CENTRE_RADIUS,
                consts.BGR.YELLOW,
                consts.PREVIEW_POINT_CENTRE_THICKNESS,
            )

            cv2.putText(
                frame,
                point.name,
                text_coords,
                cv2.FONT_HERSHEY_SIMPLEX,
                consts.PREVIEW_POINT_FONT_SCALE,
                consts.BGR.YELLOW,
                consts.PREVIEW_POINT_TEXT_THICKNESS,
            )
