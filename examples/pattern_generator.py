import mc_diag_boat as db


def get_boat_angles(offset: db.Vec2[int]) -> dict[int, tuple[db.Angle, db.Vec2[int]]]:
    return {
        index: (
            angle,
            offset.project(db.Vec2.from_polar(1.0, angle)).round(),
        )
        for index, angle in enumerate(offset.angle().closest_boat_angle(4))
    }


def choose_pattern(
    offset: db.Vec2[int],
    angle: tuple[db.Angle, db.Vec2[int]],
) -> db.Pattern | None:
    patterns = {
        index: pattern
        for index, pattern in enumerate(db.pattern.PatternGenerator(angle[1]).pareto_front)
    }
    print(f"""
Offset: {offset}
Angle: {offset.angle()}
Boat angle error: {offset - angle[1]}
Patterns for boat angle:""")
    for index, pattern in patterns.items():
        print(f"    {index} : [n_blocks: {len(pattern)} , error: {pattern.deviation()} blocks]")
    choice = db.loop_input(
        "\nEnter index of desired pattern (default, choose other boat angle): ",
        {index for index in patterns.keys()},
        default=-1,
    )
    if choice == -1:
        return None
    return patterns[choice]


def choose_angle(
    offset: db.Vec2[int],
    boat_angles: dict[int, tuple[db.Angle, db.Vec2[int]]]
) -> int:
    print(f"""
Offset: {offset}
Angle: {offset.angle()}
Closest boat angles and offsets:""")
    for index, angle in boat_angles.items():
        print(f"    {index} : [offset: {angle[1]} , error: {angle[1] - offset} , angle: {angle[0]}]")
    return db.loop_input(
        "\nEnter index of desired boat angle (default, 0): ",
        {index for index in boat_angles.keys()},
        default=0,
    )


def choose(
    offset: db.Vec2[int],
    boat_angles: dict[int, tuple[db.Angle, db.Vec2[int]]],
) -> tuple[db.Angle, db.Pattern]:
    angle_index = 0
    while True:
        choice = choose_pattern(offset, boat_angles[angle_index])
        if isinstance(choice, db.Pattern):
            return boat_angles[angle_index][0], choice
        angle_index = choose_angle(offset, boat_angles)


def display_pattern(angle: db.Angle, pattern: db.Pattern) -> None:
    print(f"""
Boat placement angle range: {angle.boat_placement_range()}
    F3 angle while in boat: {round(angle, 1):.1f}""")
    db.report.plot_pattern(pattern)
    db.report.show_plots()


def main():
    origin = db.vec2_input("Enter origin", int)
    destination = db.vec2_input("Enter destination", int)
    offset = destination - origin
    boat_angles = get_boat_angles(offset)
    angle, pattern = choose(offset, boat_angles)
    display_pattern(angle, pattern)


if __name__ == "__main__":
    main()

