import mc_diag_boat as db


def get_boat_offsets(offset: db.Vec2[int]) -> list[db.Vec2[float]]:
    return [
        offset.project(db.Vec2.from_polar(1.0, angle))
        for angle in offset.angle().closest_boat_angle(4)
    ]


def get_patterns(offsets: list[db.Vec2[float]]) -> list[db.Pattern]:
    return [
        pattern
        for offset in offsets
        for pattern in db.pattern.PatternGenerator(offset).patterns
    ]


def get_pareto_patterns(
    offset: db.Vec2[int],
    patterns: list[db.Pattern],
) -> list[db.Pattern]:
    patterns_attrs = [
        (-(offset - pattern.target).length(), -pattern.deviation(), -len(pattern))
        for pattern in patterns
    ]
    pareto_patterns = [
        patterns[index]
        for index in db.optimization.pareto_indices(patterns_attrs)
    ]
    return [
        pattern
        for index, pattern in enumerate(pareto_patterns)
        if not any(pattern == other for other in pareto_patterns[:index])
    ]


def choose_pattern(offset: db.Vec2[int], patterns: list[db.Pattern]) -> db.Pattern:
    sorted_patterns = sorted(patterns, key=lambda p: p.deviation())
    print(f"""
Offset: {offset}
Patterns:""")
    for line in db.report.pretty_seqs([(
        index,
        ": offset_error:",
        f"{round((offset - pattern.target).length(), 2)} blocks",
        " n_blocks:",
        len(pattern) - 1,
        " travel_error:",
        f"{round(pattern.deviation(), 2)} blocks",
    ) for index, pattern in enumerate(sorted_patterns)]):
        print("   ", line)
    choice = db.loop_input(
        "\nEnter index of desired pattern (default, 0): ",
        {index for index in range(len(sorted_patterns))},
        default=0,
    )
    return sorted_patterns[choice]


def display_pattern(pattern: db.Pattern) -> None:
    boat_angle = pattern.target.angle().closest_boat_angle()
    print(f"""
Boat placement angle range: {boat_angle.boat_placement_range()}
    F3 angle while in boat: {round(boat_angle, 1):.1f}""")
    fig = db.report.plot_pattern(pattern)
    db.report.show_plots()
    #fig.savefig("test.png")


def main():
    origin = db.vec2_input("Enter origin", int)
    destination = db.vec2_input("Enter destination", int)
    offset = destination - origin
    boat_offsets = get_boat_offsets(offset)
    patterns = get_patterns(boat_offsets)
    pareto_patterns = get_pareto_patterns(offset, patterns)
    pattern = choose_pattern(offset, pareto_patterns)
    display_pattern(pattern)


if __name__ == "__main__":
    main()

