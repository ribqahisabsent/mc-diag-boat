from litemapy import BlockState
from mc_diag_boat.vec2 import Vec2
import mc_diag_boat.schematic as sch
import mc_diag_boat.input as inp
import mc_diag_boat.report as rep


BLOCKS = [
    "minecraft:blue_ice",
    "minecraft:packed_ice",
    "minecraft:ice",
    "minecraft:stone",
    "minecraft:stone_button",
    "minecraft:stone_pressure_plate",
    "minecraft:lever",
    "minecraft:rail",
]


def get_boat_offsets(offset: Vec2[int]) -> list[Vec2[float]]:
    return [
        offset.project(Vec2.from_polar(1.0, angle))
        for angle in offset.angle().closest_boat_angle(4)
    ]


def choose_path_offset(offset: Vec2[int], boat_offsets: list[Vec2[float]]) -> Vec2[float]:
    print(f"""
Offset: {offset}
Closest boat offsets:""")
    lines = rep.pretty_seqs([(
        index,
        ": error:",
        f"{round((boat_offset - offset).length(), 2)} blocks",
    ) for index, boat_offset in enumerate(boat_offsets)])
    for line in lines:
        print("   ", line)
    return boat_offsets[inp.loop_input(
        "\nEnter index of desired boat angle (default, 0): ",
        {index for index in range(len(boat_offsets))},
        default=0,
    )]


def choose_blocks() -> list[BlockState]:
    print("\nBlock options:")
    for index, block in enumerate(BLOCKS):
        print("   ", index + 1, ":", block)
    while True:
        indices = str(inp.loop_input(
            "\nEnter indices of desired blocks in order (default, 15 (blue ice topped with buttons)): ",
            int,
            default=12,
        ))
        try:
            if any(int(index) - 1 < 0 for index in indices):
                raise ValueError("Indices must be 1 or greater")
            return [
                BlockState(BLOCKS[int(index) - 1]).with_properties(face="floor", facing="north")
                for index in indices
            ]
        except Exception as e:
            print(f"{type(e).__name__}, {e}")
            continue


def create_schematic(
    origin: Vec2[int],
    path_offset: Vec2[float],
    blocks: list[BlockState],
    gap_size: int,
) -> None:
    schem_name = sch.name_schematic(origin, (origin + path_offset.round()).round())
    schem = sch.generate_schematic(path_offset, gap_size, blocks,schem_name)
    schem.save(schem_name + ".litematica")
    print("\nSaved schematic", schem_name)
    path_angle = path_offset.angle().closest_boat_angle()
    print(f"""
Boat placement angle range: {path_angle.boat_placement_range()}
    F3 angle while in boat: {round(path_angle, 1):.1f}""")


def main():
    origin = inp.vec2_input("Enter origin", int)
    destination = inp.vec2_input("Enter destination", int)
    offset = destination - origin
    boat_offsets = get_boat_offsets(offset)
    path_offset = choose_path_offset(offset, boat_offsets)
    gap_size = inp.loop_input(
        "\nEnter gap size (default, 0): ",
        {n for n in range(255)},
        default=0,
    )
    blocks = choose_blocks()
    create_schematic(origin, path_offset, blocks, gap_size)


if __name__ == "__main__":
    main()

