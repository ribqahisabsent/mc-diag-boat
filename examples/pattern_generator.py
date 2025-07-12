from mc_diag_boat.vec2 import Vec2
from mc_diag_boat.pattern import Pattern, PatternGenerator
import mc_diag_boat.optimization as opt
import mc_diag_boat.input as inp
import mc_diag_boat.report as rep


def get_boat_offsets(offset: Vec2[int]) -> list[Vec2[float]]:
    return [
        offset.project(Vec2.from_polar(1.0, angle))
        for angle in offset.angle().closest_boat_angle(4)
    ]


def get_patterns(offsets: list[Vec2[float]]) -> list[Pattern]:
    return [
        pattern
        for offset in offsets
        for pattern in PatternGenerator(offset).patterns
    ]


def get_pareto_patterns(
    offset: Vec2[int],
    patterns: list[Pattern],
) -> list[Pattern]:
    patterns_attrs = [
        (-(offset - pattern.target).length(), -pattern.deviation(), -len(pattern))
        for pattern in patterns
    ]
    pareto_patterns = [
        patterns[index]
        for index in opt.pareto_indices(patterns_attrs)
    ]
    return [
        pattern
        for index, pattern in enumerate(pareto_patterns)
        if not any(pattern == other for other in pareto_patterns[:index])
    ]


def choose_pattern(
    origin: Vec2[int],
    offset: Vec2[int],
    patterns: list[Pattern],
) -> Pattern:
    sorted_patterns = sorted(patterns, key=lambda p: p.deviation())
    print(f"""
Offset: {offset}, Distance: {round(offset.length(), 2)}
Patterns:""")
    lines = rep.pretty_seqs([(
        index,
        ": destination:",
        (origin + pattern.target).round(),
        " dest_error:",
        f"{round((offset - pattern.target).length(), 2)} blocks",
        " n_blocks:",
        len(pattern) - 1,
        " travel_error:",
        f"{round(pattern.deviation(), 2)} blocks",
    ) for index, pattern in enumerate(sorted_patterns)])
    for line in lines:
        print("   ", line)
    choice = inp.loop_input(
        "\nEnter index of desired pattern (default, 0): ",
        {index for index in range(len(sorted_patterns))},
        default=0,
    )
    return sorted_patterns[choice]


def display_pattern(origin: Vec2[int], pattern: Pattern) -> None:
    pattern_name = f"dbpatt_{origin.dense_str()}_{(origin + pattern.target.round()).dense_str()}"
    fig, plt = pattern.plot()
    fig.savefig(pattern_name)
    print("\nSaved pattern", pattern_name)
    boat_angle = pattern.target.angle().closest_boat_angle()
    print(f"""
Boat placement angle range: {boat_angle.boat_placement_range()}
    F3 angle while in boat: {round(boat_angle, 1):.1f}""")
    plt.show()


def main():
    origin = inp.vec2_input("Enter origin", int)
    destination = inp.vec2_input("Enter destination", int)
    offset = destination - origin
    boat_offsets = get_boat_offsets(offset)
    patterns = get_patterns(boat_offsets)
    pareto_patterns = get_pareto_patterns(offset, patterns)
    pattern = choose_pattern(origin, offset, pareto_patterns)
    display_pattern(origin, pattern)


if __name__ == "__main__":
    main()

