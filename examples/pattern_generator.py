import mc_diag_boat as db


origin_x = int(input("origin x: "))
origin_z = int(input("origin z: "))
destination_x = int(input("destination x: "))
destination_z = int(input("destination z: "))

origin = db.Vec2(origin_x, origin_z)
destination = db.Vec2(destination_x, destination_z)
offset = destination - origin

