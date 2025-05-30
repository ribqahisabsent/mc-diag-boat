import mc_diag_boat as db


origin = db.Vec2(4, 0)
destination = db.Vec2(2000, -592)
offset = destination - origin
schem_name = db.name_schematic(origin, destination)
schem = db.generate_schematic(offset, gap_size=1)
schem.save(schem_name + ".litematica")
print("Saved schematic", schem_name)

