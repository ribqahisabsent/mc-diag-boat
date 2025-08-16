import numpy as np
import skimage.draw
from mc_diag_boat.vec2 import Vec2
from mc_diag_boat.angle import Angle
from mc_diag_boat.pattern import PatternGenerator
from mc_diag_boat.schematic import _add_gaps, _cut_regions, generate_schematic
from mc_diag_boat.formatting import pretty_seqs
from mc_diag_boat.input import loop_input


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
    gapped_raster = _add_gaps(raster, 1)
    cut_raster = _cut_regions(raster)
    cut_gapped_raster = _cut_regions(gapped_raster)
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

if False:
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

if False:
    a1 = BoatAngle.SOUTH
    a2 = BoatAngle.EAST
    a3 = BoatAngle(1)
    print(a1, a2)
    print(a3)
    ud = a1.unit_deviation(a2)
    print(ud)
    a4 = a3 + a2
    print(a4)
    print(-a4)

if False:
    a1 = Angle.SOUTH
    a2 = Angle(532343.9)
    print(a2)
    bas = a1.closest_boat_angle(5)
    print(bas)
    print(bool(0.0), bool(1.0))
    bas2 = bas[0].closest_boat_angle()
    print(bas2)

if False:
    trgt = Vec2(-2050.0, -1607)
    pg = PatternGenerator(trgt)
    print(len(pg.patterns))
    print(len(pg.patterns))
    pfront = pg.pareto_front
    print(len(pfront))
    pf_tuples = [(
        "Length",
        "Deviation",
        "Angular Deviation",
    )] + [(
        len(p),
        p.deviation(),
        p[-1].angle() - trgt.angle(),
    ) for p in pfront]
    pretty_pfront = pretty_seqs(pf_tuples)
    for p in pretty_pfront:
        print(f"  {p}")
    sort = pg.len_sorted(short2long=False)
    print(len(sort[0]), sort[0].deviation())
    print(len(sort[-1]), sort[-1].deviation())
    sort = pg.deviation_sorted()
    print(len(sort[0]), sort[0].deviation())
    print(len(sort[-1]), sort[-1].deviation())


if True:
    trgt = Vec2(-205, 160)
    pg = PatternGenerator(trgt)
    pattern = pg.pareto_front[-3]

if False:
    options = {0, 1, 2, 3, 4}
    inp = loop_input(f"choices: {options}: ", options)
    inp = loop_input(f"choices: {options}: ")
    print(inp, type(inp))

