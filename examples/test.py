import numpy as np
import skimage.draw
from mc_diag_boat.vec2 import Vec2
from mc_diag_boat.angle import BoatAngle
from mc_diag_boat.schematic import add_gaps, cut_regions, generate_schematic


if False:
    x = 2 / 2
    print(type(x), x)
    y = 42
    z = 6
    a = y // z
    print(type(a), a)

offset = Vec2(-40.0, 50.2)

if False:
    raster = np.transpose(skimage.draw.line_nd((0.0, 0.0), offset.as_tuple(), endpoint=True)).tolist()
    array_raster = skimage.draw.line_nd((0.0, 0.0), offset.as_tuple(), endpoint=True)
    raster = [Vec2(x, z) for x, z in zip(*array_raster)]
    print(raster)
    print(type(raster))
    print(type(raster[0]))

if False:
    gapped_raster = add_gaps(raster, 1)
    cut_raster = cut_regions(raster)
    cut_gapped_raster = cut_regions(gapped_raster)
    print(gapped_raster)
    print(cut_raster)
    print(cut_gapped_raster)

if False:
    schem = generate_schematic(offset)
    print(type(schem))
    #print({key: region.__dict__ for key, region in schem.regions.items()})
    schem.save("schem_test.litematica")

if False:
    fv = Vec2(1.0, 5) // 2
    print(type(fv), fv)
    print(type(fv.x), type(fv.z))
    fv = 2.1 * Vec2(1, 5)
    print(type(fv), fv)

if False:
    v = Vec2(2.4, 2.7)
    iv = v.round()
    fv = v.round(0)
    print(iv, fv)
    v2 = iv - fv
    print(v2)
    v2 = iv - iv
    print(v2)
    dot = iv.dot(fv)
    cross = iv.cross(fv)
    print(dot)
    print(cross)

if False:
    v = Vec2.ZERODEG.rotated(180)
    print(v, v.angle())
    print(v.rotated(-5).angle())
    v = Vec2.ZERODEG.rotated(-180)
    print(v, v.angle())
    print(v.rotated(-5).angle())
    v = Vec2.ZERODEG.rotated(-1)
    print(v, v.angle())
    print(v.rotated(-5).angle())
    v = Vec2.ZERODEG.rotated(-91)
    print(v, v.angle())
    print(v.rotated(-5).angle())

if False:
    v = Vec2.NORTH
    print(v, v.angle())
    v = v * 10
    print(v, v.angle())
    v = v.rotated(39)
    print(v, v.angle())
    v = 10 * Vec2.NORTH.rotated(39)
    print(v, v.angle())
    v = Vec2.EAST
    print(v, v.angle())
    v = Vec2.ZERO
    print(v, v.angle())

if True:
    v1 = Vec2(2.0, 50.1)
    v2 = Vec2(0.0, 501.0)
    proj = v1.project(v2)
    print(proj)

if False:
    for i in range(0, 360, 16):
        angle = BoatAngle.from_index(i)
        print(angle)
        print(BoatAngle.closest_to(angle, 5))
    print(BoatAngle.closest_to(180, 5))

if True:
    a1 = BoatAngle.SOUTH
    a2 = BoatAngle.EAST
    print(a1, a2)
    ud = a1.unit_deviation(a2)
    print(ud)

