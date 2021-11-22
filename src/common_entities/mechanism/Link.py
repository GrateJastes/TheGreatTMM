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

    def research_link(self, start_frame: np.ndarray) -> bool:
        research_ok = True

        # First of all we preparing frame and converting it to binary image. It is made to research the current link's
        # points only
        frame = prepare_frame(start_frame, self.color_bounds)
        # Finding each contour we can on the result image
        contours, _ = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            research_ok = False
            return research_ok

        # Finding all signatures on the frame, which can be interpreted as link's points' markers. And representing
        # them as ellipses fitted to the contours
        signatures = find_marker_signatures(contours)
        if not signatures:
            research_ok = False
            return research_ok

        # Sorting found signatures by their area to discard small round-shaped interferences
        signatures.sort(key=ellipse_area, reverse=True)

        # If the researching link is the initial one, we know that it has only 1 point of interest. We also
        # must calculate omega angle in this case.
        if self.is_initial:
            # Traversing coordinates, assuming origin marker as origin
            marker = (int(signatures[0][0][0]), int(signatures[0][0][1]))
            # Adding current point to the Link's path
            self.points[0].path.append(marker)
            return research_ok

        # If the link is not initial, it can contain several PoI. In this case we must research all of the signatures,
        # to find relevant(s). Here we make markers (x and y list-pairs) from the signatures' ellipses
        markers = [(int(ellipse[0][0]), int(ellipse[0][1])) for ellipse in signatures]

        # Making list of the last dots to every PoI.
        last_dots = [point.path.last_dot_coords for point in self.points]
        # Finding closest matches between the provided markers and the last dots on PoIs' paths
        matches, rest_markers = self.__find_matches(last_dots, markers)

        # This condition means that we didn't find enough markers to describe all of the PoI on the Link. In current
        # version of the app we just discard whole frame for the Link in this case. TODO: research what we can
        # if len(matches) + len(rest_markers) < len(self.points):
        #     return False

        # Finding markers for points which have no dots in their paths' yet.
        rest_markers_iter = iter(rest_markers)
        for point in self.points:
            if point.path.last_dot_coords == (None, None):
                research_ok = True
                try:
                    point.path.append(next(rest_markers_iter))
                # If there is some PoI which isn't matched to any marker yet, but markers are already out, we
                # must exit the cycle and drop the current frame's research for this Link.
                except StopIteration:
                    point.path.append((None, None))

                continue

            # But if we have found the next dot to the point's path, we could append it and proceed further
            if point.path.last_dot_coords in matches.keys():
                point.path.append(matches[point.path.last_dot_coords])
                research_ok = True

        return research_ok

    # Private method for local usage. Returns found matches (dict. markers to dots) and the rejected markers
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

        # First of all we are looking for markers which are closest to every dot on the ends of the paths
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

    def draw_on_frame(self, frame: np.ndarray, frame_num: int) -> None:
        for point in self.points:
            if len(point.path.dots) < frame_num + 1:
                continue
            point_coords = (
                point.path.dots[frame_num].x,
                point.path.dots[frame_num].y,
            )
            text_coords = (
                point.path.dots[frame_num].x + consts.PREVIEW_POINT_TEXT_SHIFT,
                point.path.dots[frame_num].y - consts.PREVIEW_POINT_TEXT_SHIFT,
            )

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
