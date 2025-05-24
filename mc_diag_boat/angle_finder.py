from math import sin, cos, atan, degrees, radians, dist
from skimage.draw import line_nd
import ipywidgets as w
import numpy as np
from matplotlib import pyplot as plt
from os.path import isfile
from litemapy import Schematic, Region, BlockState# Format origin and destination coordinates as tuple[int, int]


def format_coords(origin_x: int, origin_z: int, destination_x: int, destination_z: int) -> tuple[tuple[int, int], tuple[int, int]]:
    return (origin_x, origin_z), (destination_x, destination_z)


# Compute the relative position of a point from an origin point
def get_offset(p0: tuple[int, int], p1: tuple[int, int]) -> tuple[int, int]:
    return (p1[0]-p0[0], p1[1]-p0[1])


# Compute the angle from an origin point to another point, given the offset
def get_angle(offset: tuple[int, int]) -> float:
    if offset[0] == 0:
        if offset[1] > 0:
            return 0.0
        if offset[1] < 0:
            return 180.0
        else:
            raise ValueError("No offset of destination from origin")
    direction = degrees(atan(offset[1]/offset[0]))
    if offset[0] > 0:
        return direction - 90.0
    elif offset[0] < 0:
        return direction + 90.0


# Format a string conveying an angle and its antipode
def format_angles(angle: float, decimals: int = 1) -> str:
    antipode = 0.0
    if angle == 0.0:
        antipode = 180.0
    elif angle < 0.0:
        antipode = angle + 180.0
    elif angle > 0.0:
        antipode = angle - 180.0
    return f'{angle:.{decimals}f}' + " deg | (antipode: " + f'{antipode:.{decimals}f}' + " deg)"


# Compute basic information about origin and destination
def basics_metrics(origin_x: int, origin_z: int, destination_x: int, destination_z: int) -> tuple[tuple[int, int], float, float]:
    origin, destination = format_coords(origin_x, origin_z, destination_x, destination_z)
    offset = get_offset(origin, destination)
    distance = dist(origin, destination)
    optimal_angle = get_angle(offset)
    return offset, distance, optimal_angle


# Print basic information about origin and destination
def print_basics(offset: tuple[int, int], distance: float, optimal_angle: float) -> None:
    print("Destination offset:", offset)
    print("Distance:", f'{distance:.1f}', "blocks")
    print("True Angle:", format_angles(optimal_angle, 5))


# Compute the distance deviation over each block traveled, given an anglular deviation
def get_block_error(angle_error: float) -> float:
    return abs(2 * sin(radians(angle_error/2)))


# Format a string conveying angle, block, and total errors
def format_errors(angle_error: float, block_error: float, distance: float) -> str:
    angle = " ".join(["'ANGLE':", f'{angle_error:.3}', "deg"])
    block = " ".join(["'PER BLOCK':", f'{block_error:.3}', "blocks"])
    total = " ".join(["'TOTAL':", f'{distance*block_error:.2f}', "blocks"])
    return "{ " + ", ".join([angle, block, total]) + " }"


# Compute information about manual player alignment
def manual_metrics(optimal_angle: float) -> tuple[float, float, float]:
    apparent_angle = round(optimal_angle, 1)
    min_angle = apparent_angle - 0.05
    max_angle = apparent_angle + 0.05
    if abs(optimal_angle - min_angle) > abs(optimal_angle - max_angle):
        angle_error = optimal_angle - min_angle
    else:
        angle_error = optimal_angle - max_angle
    block_error = get_block_error(angle_error)
    return apparent_angle, angle_error, block_error


# Print information about manual player alignment
def print_manual(distance: float, apparent_angle: float, angle_error: float, block_error: float) -> None:
    print("\nMANUAL DIRECTION:")
    print("    Apparent (F3) angle:", format_angles(apparent_angle))
    print("    MAX Errors:", format_errors(angle_error, block_error, distance))


# Find the closest boat angle to a given angle
def closest_boat_angle_index(optimal_angle: float) -> int:
    index = 0
    for index, angle in enumerate(BOAT_ANGLES):
        if angle > optimal_angle:
            break
    if abs(optimal_angle-angle) > abs(optimal_angle-BOAT_ANGLES[index-1]):
        index -= 1
    return index


# Compute information about boat player alignment
def boat_metrics(optimal_angle: float, boat_angle_adjust: int = 0) -> tuple[float, float, float]:
    boat_angle_index = (closest_boat_angle_index(optimal_angle) + boat_angle_adjust) % 256
    boat_angle = BOAT_ANGLES[boat_angle_index]
    angle_error = optimal_angle - boat_angle
    block_error = get_block_error(angle_error)
    return boat_angle_index, angle_error, block_error


# Convert from polar coordinates to cartesion coordinates, factoring in a given origin point
def polar_to_cartesian(origin: tuple[int, int], distance: float, angle: float, round_d: bool = False) -> tuple[int, int]:
    angle_r = radians(angle)
    destination = ((-1 * distance * sin(angle_r)) + origin[0], (distance * cos(angle_r)) + origin[1])
    if round_d:
        return (round(destination[0]), round(destination[1]))
    return destination


# Print information about boat player alignment
def print_boat(distance: float, boat_angle_index: int, angle_error: float, block_error: float, boat_destination: tuple[int, int]) -> None:
    print("\nBOAT DIRECTION:")
    print("    Boat angle:", format_angles(BOAT_ANGLES[boat_angle_index], 5))
    print("    Apparent (F3) boat angle:", format_angles(APPARENT_BOAT_ANGLES[boat_angle_index]))
    print("    Errors:", format_errors(angle_error, block_error, distance))
    print("    Boat Destination:", boat_destination)


# Compute the raster of a line segment, given its length and angle
def rasterize(distance: float, angle: float) -> list[list[int]]:
    offset = polar_to_cartesian((0, 0), distance, angle)
    integer_offset = (int(round(100 * offset[0], 0)), int(round(100 * offset[1], 0)))
    raster = np.transpose(line_nd((0.0, 0.0), offset, endpoint=True)).tolist()
    return raster


# Add gaps to a raster and segment it into small sections for inclusion in a schematic
def cut_sxns(raster: list[list[int]], gap_size: int) -> list[list[list[int]]]:
    uncut_path = [coord for index, coord in enumerate(raster) if index % (gap_size + 1) == 0]
    sxn_size = max(int(BASE_SXN_SIZE / (gap_size + 1)), 1)
    return [[uncut_path[index] for index in range(sxn_start, min(sxn_start + sxn_size, len(uncut_path)))] for sxn_start in range(0, len(uncut_path), sxn_size)]


# Format a name for a schematic, including the given origin and destination coordinates
def name_schematic(origin_x: int, origin_z: int, destination_x: int, destination_z: int) -> str:
    origin, destination = format_coords(origin_x, origin_z, destination_x, destination_z)
    return "path_" + str(origin) + "_" + str(destination)


# Create a Region object for a schematic, given a path (list of coordinates)
def make_region(path: list[list[int]], blocks: list[BlockState]) -> Region:
    if len(blocks) == 0:
        raise ValueError("Must be at least one BlockState provided.")
    path_span = (path[-1][0] - path[0][0] + (1 if path[-1][0] >= 0 else -1), path[-1][1] - path[0][1] + (1 if path[-1][1] >= 0 else -1))
    region = Region(path[0][0], 0, path[0][1], path_span[0], len(blocks), path_span[1])
    for coords in path:
        for block_index, block_state in enumerate(blocks):
            region[coords[0] - path[0][0], block_index, coords[1] - path[0][1]] = block_state
    return region


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
    for pattern_length in range(1, MAX_PATTERN_SIZE + 1):
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
        print("\nNO SUITABLE PATTERN FOUND WITHIN", MAX_PATTERN_SIZE, "BLOCKS.")
        return None, None, None
    return pattern, angle_error, block_error


# Print information about a given pattern
def print_pattern(distance: float, pattern: list[list[int]], angle_error: float, block_error: float) -> None:
    print("\nBOAT PATH BUILD PATTERN:")
    print("    Found", len(pattern) - 1, "blocks long pattern:")
    print("    Iterations are offset by", get_offset(pattern[0], pattern[-1]), "blocks")
    print("    Errors (from boat direction):", format_errors(angle_error, block_error, distance))


# Display a 2D map representing the blocks in a given pattern
def graph_pattern(pattern: list[list[int]]) -> None:
    pattern_space = np.zeros((abs(pattern[-1][0]) + 1, abs(pattern[-1][1]) + 1))
    for site in range(len(pattern) - 1):
        pattern_space[(abs(pattern[site][0]), abs(pattern[site][1]))] = (len(pattern) - site) / len(pattern) + COLOR_MIN_VALUE
    pattern_space[(abs(pattern[-1][0]), abs(pattern[-1][1]))] = 1.0 + COLOR_MIN_VALUE
    pattern_space = np.transpose(pattern_space)
    plt.imshow(pattern_space, cmap='turbo', interpolation='nearest')
    if pattern[-1][0] < 0:
        plt.gca().invert_xaxis()
    if pattern[-1][1] < 0:
        plt.gca().invert_yaxis()
    plt.title("Start at red (0, 0), go through rainbow\n(lone red is start of next iteration)")
    plt.xlabel("West < - > East")
    plt.ylabel("South < - > North")
    plt.xticks([i for i in range(abs(pattern[-1][0]) + 1)])
    plt.yticks([i for i in range(abs(pattern[-1][1]) + 1)])
    plt.show()


################################################
################ CORE FUNCTIONS ################
################################################

# Display relevant metrics related to the origin and destination
def evaluate_angles(origin_x: int, origin_z: int, destination_x: int, destination_z: int) -> None:
    global boat_destination_g
    offset, distance, optimal_angle = basics_metrics(origin_x, origin_z, destination_x, destination_z)
    print_basics(offset, distance, optimal_angle)
    apparent_angle, apparent_angle_error, apparent_block_error = manual_metrics(optimal_angle)
    print_manual(distance, apparent_angle, apparent_angle_error, apparent_block_error)
    boat_angle_index, boat_angle_error, boat_block_error = boat_metrics(optimal_angle)
    boat_destination_g = polar_to_cartesian((origin_x, origin_z), distance, BOAT_ANGLES[boat_angle_index], round_d=True)
    print_boat(distance, boat_angle_index, boat_angle_error, boat_block_error, boat_destination_g)


# Create and save a Litematica schematic file (.litematic); name uses the current BOAT destination
schem_gen_output = w.Output(layout={'border': '2px solid black', 'margin': '8px', 'padding': '4px', 'width': '1000px'})
@schem_gen_output.capture()
def generate_schematic(b) -> None:
    offset, distance, optimal_angle = basics_metrics(origin_x.value, origin_z.value, destination_x.value, destination_z.value)
    boat_angle_index = boat_metrics(optimal_angle)[0]
    raster = rasterize(distance, BOAT_ANGLES[boat_angle_index])
    sxned_path = cut_sxns(raster, gap_size.value)
    schem_name = name_schematic(origin_x.value, origin_z.value, boat_destination_g[0], boat_destination_g[1])
    schem = Schematic(name=schem_name)
    for sxn in sxned_path:
        schem.regions[f'{sxn}'] = make_region(sxn, blocks_g)
    filename = smart_filename(schem_name + ".litematic")
    schem.save(filename)
    print("Saved schematic", filename)


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
