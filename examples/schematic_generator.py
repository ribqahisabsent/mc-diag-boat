from mc_diag_boat.vec2 import Vec2
import mc_diag_boat.schematic as sch
import mc_diag_boat.input as inp
import mc_diag_boat.report as rep


origin_x = int(input("origin x: "))
origin_z = int(input("origin z: "))
destination_x = int(input("destination x: "))
destination_z = int(input("destination z: "))
gap_size = int(input("gap size: "))

origin = Vec2(origin_x, origin_z)
destination = Vec2(destination_x, destination_z)
offset = destination - origin
closest_boat_offsets = [
    offset.project(Vec2.from_polar(1.0, angle))
    for angle in offset.angle().closest_boat_angle(4)
]

print(f"""
Offset: {offset}
Angle: {offset.angle()}
Closest boat angles and offsets:""")
for line in rep.pretty_seqs([(
    index,
    " error:",
    f"{round((boat_offset - offset).length(), 2)} blocks",
    " angle:", boat_offset.angle().closest_boat_angle()
) for index, boat_offset in enumerate(closest_boat_offsets)]):
    print("   ", line)

chosen_offset = closest_boat_offsets[inp.loop_input(
    "\nEnter index of desired boat angle (default, 0): ",
    {index for index in range(len(closest_boat_offsets))},
    default=0,
)]

schem_name = sch.name_schematic(origin, (origin + chosen_offset).round())
schem = sch.generate_schematic(chosen_offset, gap_size)
schem.save(schem_name + ".litematica")
print("Saved schematic", schem_name)
chosen_angle = chosen_offset.angle().closest_boat_angle()
print(f"""
Boat placement angle range: {chosen_angle.boat_placement_range()}
    F3 angle while in boat: {round(chosen_angle, 1):.1f}""")

