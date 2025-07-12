from typing import Literal, Sequence


def pretty_seqs(
    sequences: Sequence[Sequence],
    align: Literal["L", "R", "C"] | tuple[Literal["L", "R", "C"]] = "L",
    separator: str = " ",
) -> Sequence[str]:
    if len({len(sequence) for sequence in sequences}) > 1:
        raise ValueError("All sequences must be the same length")
    item_lengths = [max(len(str(item)) for item in col) for col in zip(*sequences)]
    if align == "L":
        return [
            separator.join(f"{str(item):<{item_lengths[col]}}" for col, item in enumerate(row))
            for row in sequences
        ]
    if align == "R":
        return [
            separator.join(f"{str(item):>{item_lengths[col]}}" for col, item in enumerate(row))
            for row in sequences
        ]
    if align == "C":
        return [
            separator.join(f"{str(item):^{item_lengths[col]}}" for col, item in enumerate(row))
            for row in sequences
        ]
    if isinstance(align, tuple) and len(align) != len(sequences[0]):
        raise ValueError("`align` must be the same length as each sequence")
    rows: list[str] = []
    for index, row in enumerate(sequences):
        if align[index] == "L":
            rows.append(separator.join(f"{str(item):<{item_lengths[col]}}" for col, item in enumerate(row)))
        if align[index] == "R":
            rows.append(separator.join(f"{str(item):>{item_lengths[col]}}" for col, item in enumerate(row)))
        if align[index] == "C":
            rows.append(separator.join(f"{str(item):^{item_lengths[col]}}" for col, item in enumerate(row)))
    return rows


SIG_FIGS = 4


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

