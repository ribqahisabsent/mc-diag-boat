import numpy as np
import skimage.draw
from mc_diag_boat.types import Vec2
from mc_diag_boat.schematic import add_gaps, cut_regions, generate_schematic


if False:
    x = 2 / 2
    print(type(x), x)
    y = 42
    z = 6
    a = y // z
    print(type(a), a)

#offset = Vec2.from_polar(60.0, 67.5)
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
    schem.save("test_schem.litematica")

if False:
    fv = Vec2(1.0, 5) // 2
    print(type(fv), fv)
    print(type(fv.x), type(fv.z))
    fv = 2.1 * Vec2(1, 5)
    print(type(fv), fv)
    fv = Vec2.from_polar(23, 3)

if True:
    v = Vec2(2.4, 2.7)
    iv = v.rounded()
    fv = v.rounded(0)
    print(iv, fv)

