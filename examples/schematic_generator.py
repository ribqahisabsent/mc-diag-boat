import mc_diag_boat as db


origin_x = int(input("origin x: "))
origin_z = int(input("origin z: "))
destination_x = int(input("destination x: "))
destination_z = int(input("destination z: "))
gap_size = int(input("gap size: "))

origin = db.Vec2(origin_x, origin_z)
destination = db.Vec2(destination_x, destination_z)
offset = destination - origin
closest_boat_angles = {
    index: (angle, (db.Vec2.ZERODEG.rotate(angle) * offset.length()).round())
    for index, angle in enumerate(db.BoatAngle.closest_to(offset.angle(), 4))
}

print(f"""
Offset: {offset}
Angle: {offset.angle()}
Closest boat angles and offsets:""")
for index, angle in closest_boat_angles.items():
    print(f"    {index} : [offset: {angle[1]} , error: {offset - angle[1]} , angle: {angle[0]}]")

while True:
    try:
        choice = input("\nEnter index of desired boat angle (default 0): ")
        if choice == "":
            choice = 0
        else:
            choice = int(choice)
        chosen_angle = closest_boat_angles[choice]
        break
    except Exception as e:
        print(type(e).__name__, e)

schem_name = db.name_schematic(origin, destination)
schem = db.generate_schematic(chosen_angle[1], gap_size)
schem.save(schem_name + ".litematica")
print("Saved schematic", schem_name)

print(f"""
Boat placement angle range: {chosen_angle[0].placement_range()}
    F3 angle while in boat: {round(chosen_angle[0], 1)}
""")

