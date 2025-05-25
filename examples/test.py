import numpy as np
import skimage.draw
from mc_diag_boat.types import TravelError, Vec2


a: float = 2.5
b: int = 1
print(a + b)

te = TravelError(0.006, 1000)
print(te)

v1 = Vec2(1.0, 3.4)
v2 = Vec2(4.1, 4.0)
print(v1 + v2)

offset = Vec2.from_polar(40.0, 45.0)
raster = np.transpose(skimage.draw.line_nd((0.0, 0.0), offset.as_tuple(), endpoint=True)).tolist()
array_raster = skimage.draw.line_nd((0.0, 0.0), offset.as_tuple(), endpoint=True)
raster = [Vec2(x, z) for x, z in zip(*array_raster)]
print(raster)
print(type(raster))
print(type(raster[0]))

