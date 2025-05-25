from math import sin, cos, atan, degrees, radians, dist
from skimage.draw import line_nd
import ipywidgets as w
import numpy as np
from os.path import isfile
from litemapy import Schematic, Region, BlockState
from . import constants
from . import reporting
from .types import Vec2


# Format origin and destination coordinates as tuple[int, int]
#def format_coords(origin_x: int, origin_z: int, destination_x: int, destination_z: int) -> tuple[tuple[int, int], tuple[int, int]]:
#    return (origin_x, origin_z), (destination_x, destination_z)


# Compute the relative position of a point from an origin point
#def get_offset(p0: tuple[int, int], p1: tuple[int, int]) -> tuple[int, int]:
#    return (p1[0]-p0[0], p1[1]-p0[1])


# Compute the angle from an origin point to another point, given the offset
def get_angle(offset: Vec2) -> float:
    if offset.x == 0:
        if offset.z > 0:
            return 0.0
        if offset.z < 0:
            return 180.0
        else:
            raise ValueError("No offset of destination from origin")
    direction = degrees(atan(offset.z/offset.x))
    if offset.x > 0:
        return direction - 90.0
    else:
        return direction + 90.0


# Compute basic information about origin and destination
#def basics_metrics(origin: Vec2, destination: Vec2) -> tuple[Vec2, float, float]:
#    #origin, destination = format_coords(origin_x, origin_z, destination_x, destination_z)
#    #offset = get_offset(origin, destination)
#    offset = destination - origin
#    #distance = dist(origin, destination)
#    distance = offset.length()
#    optimal_angle = get_angle(offset)
#    return offset, distance, optimal_angle


# Compute the distance deviation over each block traveled, given an anglular deviation
def get_block_error(angle_error: float) -> float:
    return abs(2 * sin(radians(angle_error/2)))


def max_manual_angle_error(target_angle: float) -> float:
    apparent_angle = round(target_angle, 1)
    min_angle = apparent_angle - 0.05
    max_angle = apparent_angle + 0.05
    if abs(target_angle - min_angle) > abs(target_angle - max_angle):
        angle_error = target_angle - min_angle
    else:
        angle_error = target_angle - max_angle
    return angle_error

# Compute information about manual player alignment
#def manual_metrics(optimal_angle: float) -> tuple[float, float, float]:
#    apparent_angle = round(optimal_angle, 1)
#    min_angle = apparent_angle - 0.05
#    max_angle = apparent_angle + 0.05
#    if abs(optimal_angle - min_angle) > abs(optimal_angle - max_angle):
#        angle_error = optimal_angle - min_angle
#    else:
#        angle_error = optimal_angle - max_angle
#    block_error = get_block_error(angle_error)
#    return apparent_angle, angle_error, block_error


# Find the closest boat angle to a given angle
def closest_boat_angle_index(optimal_angle: float) -> int:
    index = 0
    angle = 0.0
    for index, angle in enumerate(constants.BOAT_ANGLES):
        if angle > optimal_angle:
            break
    if abs(optimal_angle-angle) > abs(optimal_angle-constants.BOAT_ANGLES[index-1]):
        index -= 1
    return index


# Compute information about boat player alignment
def boat_metrics(optimal_angle: float, boat_angle_adjust: int = 0) -> tuple[int, float, float]:
    boat_angle_index = (closest_boat_angle_index(optimal_angle) + boat_angle_adjust) % len(constants.BOAT_ANGLES)
    boat_angle = constants.BOAT_ANGLES[boat_angle_index]
    angle_error = optimal_angle - boat_angle
    block_error = get_block_error(angle_error)
    return boat_angle_index, angle_error, block_error


# Create a unique filename if using the current filename would overwrite a file
def smart_filename(filename: str) -> str:
    if not isfile(filename):
        return filename
    split_filename = filename.rsplit('.', 1)
    new_filename = ' (1).'.join(split_filename)
    i = 2
    while isfile(new_filename):
        new_filename = f' ({i}).'.join(split_filename)
        i += 1
    return new_filename


# Compute the shortest pattern in a given raster that matches the specifications, and print information about the pattern
def find_pattern(distance: float, target_angle: float, raster: list[list[int]], block_error_thr: float, total_error_thr: float) -> tuple[list[list[int]], float, float]:
    pattern = [raster[0]]
    angle_error = 0.0
    block_error = 0.0
    for pattern_length in range(1, constants.MAX_PATTERN_SIZE + 1):
        pattern.append(raster[pattern_length])
        pattern_offset = get_offset(pattern[0], pattern[-1])
        angle_error = get_angle(pattern_offset) - target_angle
        block_error = get_block_error(angle_error)
        if dist((0,0), pattern_offset) >= distance:
            break
        if block_error <= block_error_thr:
            break
        if block_error * distance <= total_error_thr:
            break
    else:
        print("\nNO SUITABLE PATTERN FOUND WITHIN", constants.MAX_PATTERN_SIZE, "BLOCKS.")
        return None, None, None
    return pattern, angle_error, block_error


################################################
################ CORE FUNCTIONS ################
################################################

# Display relevant metrics related to the origin and destination
def evaluate_angles(origin: Vec2, destination: Vec2) -> None:
    global boat_destination_g
    #offset, distance, optimal_angle = basics_metrics(origin_x, origin_z, destination_x, destination_z)
    offset = destination - origin
    distance = offset.length()
    optimal_angle = get_angle(offset)
    print_basics(offset, distance, optimal_angle)
    apparent_angle, apparent_angle_error, apparent_block_error = manual_metrics(optimal_angle)
    print_manual(distance, apparent_angle, apparent_angle_error, apparent_block_error)
    boat_angle_index, boat_angle_error, boat_block_error = boat_metrics(optimal_angle)
    boat_destination_g = polar_to_cartesian((origin_x, origin_z), distance, BOAT_ANGLES[boat_angle_index], round_d=True)
    print_boat(distance, boat_angle_index, boat_angle_error, boat_block_error, boat_destination_g)

    # Take start and destination points
    # Determine the optimal angle, distance, closest boat angle, error values


# Display a repeating block coordinate pattern which approximates the path of a boat angle
def evaluate_pattern(boat_angle_adjust: int, block_error_thr: float, total_error_thr: float, refreshing: bool) -> None:
    if refreshing:
        return
    offset, distance, optimal_angle = basics_metrics(origin_x.value, origin_z.value, destination_x.value, destination_z.value)
    boat_angle_index, boat_angle_error, boat_block_error = boat_metrics(optimal_angle, boat_angle_adjust)
    boat_destination = polar_to_cartesian((origin_x.value, origin_z.value), distance, BOAT_ANGLES[boat_angle_index], round_d=True)
    print_boat(distance, boat_angle_index, boat_angle_error, boat_block_error, boat_destination)
    raster = rasterize(distance, BOAT_ANGLES[boat_angle_index])
    pattern, pattern_angle_error, pattern_block_error = find_pattern(distance, BOAT_ANGLES[boat_angle_index], raster, block_error_thr, total_error_thr)
    if pattern:
        print_pattern(distance, pattern, pattern_angle_error, pattern_block_error)
        graph_pattern(pattern)
