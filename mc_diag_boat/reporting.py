from math import sin, radians
import numpy as np
import matplotlib.pyplot as plt


SIG_FIGS = 4
COLOR_MIN_VALUE = 0.12


#class MCAngle:
#    def __init__(self, 


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


# Format a string conveying angle, block, and total errors
def format_errors(angle_error: float, block_error: float, distance: float) -> str:
    angle = " ".join(["'ANGLE':", f'{angle_error:.3}', "deg"])
    block = " ".join(["'PER BLOCK':", f'{block_error:.3}', "blocks"])
    total = " ".join(["'TOTAL':", f'{distance*block_error:.2f}', "blocks"])
    return "{ " + ", ".join([angle, block, total]) + " }"


# Print basic information about origin and destination
def print_basics(offset: tuple[int, int], distance: float, optimal_angle: float) -> None:
    print("Destination offset:", offset)
    print("Distance:", f'{distance:.1f}', "blocks")
    print("True Angle:", format_angles(optimal_angle, 5))


# Print information about manual player alignment
def print_manual(distance: float, apparent_angle: float, angle_error: float, block_error: float) -> None:
    print("\nMANUAL DIRECTION:")
    print("    Apparent (F3) angle:", format_angles(apparent_angle))
    print("    MAX Errors:", format_errors(angle_error, block_error, distance))


# Print information about boat player alignment
def print_boat(distance: float, boat_angle_index: int, angle_error: float, block_error: float, boat_destination: tuple[int, int]) -> None:
    print("\nBOAT DIRECTION:")
    print("    Boat angle:", format_angles(BOAT_ANGLES[boat_angle_index], 5))
    print("    Apparent (F3) boat angle:", format_angles(APPARENT_BOAT_ANGLES[boat_angle_index]))
    print("    Errors:", format_errors(angle_error, block_error, distance))
    print("    Boat Destination:", boat_destination)


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



