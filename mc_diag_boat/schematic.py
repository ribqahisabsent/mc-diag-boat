# MC Diag Boat - A set of functions for building diagonal boat roads in Minecraft
# Copyright (C) 2024  ribqahisabsent

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import Sequence
import litemapy as lm
from .vec2 import Vec2


SXN_SIZE = 16


# Add gaps to a raster and segment it into small sections for inclusion in a schematic
def _add_gaps(raster: Sequence[Vec2[int]], gap_size: int) -> list[Vec2[int]]:
    return [
        coord
        for index, coord in enumerate(raster)
        if index % (gap_size + 1) == 0 or index == len(raster) - 1
    ]


def _cut_regions(points: Sequence[Vec2[int]]) -> list[Sequence[Vec2[int]]]:
    regioned: list[Sequence[Vec2]] = []
    region_start_index = 0
    for index in range(len(points)):
        diff = (points[index] - points[region_start_index])
        if abs(diff.x) >= SXN_SIZE or abs(diff.z) >= SXN_SIZE:
            regioned.append(points[region_start_index:index])
            region_start_index = index
    if region_start_index < len(points) - 1:
        regioned.append(points[region_start_index:len(points) - 1])
    return regioned


# Create a Region object for a schematic, given a path (list of coordinates)
def _make_region(path: Sequence[Vec2[int]], blocks: Sequence[lm.BlockState]) -> lm.Region:
    if len(blocks) == 0:
        raise ValueError("Must be at least one BlockState provided.")
    path_span = Vec2(
        path[-1].x - path[0].x + (1 if path[-1].x >= 0 else -1),
        path[-1].z - path[0].z + (1 if path[-1].z >= 0 else -1)
    )
    region = lm.Region(
        x=path[0].x,
        y=0,
        z=path[0].z,
        width=int(path_span.x),
        height=len(blocks),
        length=int(path_span.z),
    )
    for coords in path:
        for block_index, block_state in enumerate(blocks):
            region[coords.x - path[0].x, block_index, coords.z - path[0].z] = block_state
    return region


# TODO make logic for naming part  of another function, accept a name here
# Create and save a Litematica schematic file (.litematic); name uses the current BOAT destination
def generate_schematic(
    offset: Vec2,
    gap_size: int = 0,
    blocks: lm.BlockState | Sequence[lm.BlockState] = lm.BlockState("minecraft:blue_ice"),
    name: str | None = None
) -> lm.Schematic:
    raster = offset.raster()
    gapped_raster = _add_gaps(raster, gap_size)
    regioned_raster = _cut_regions(gapped_raster)
    if name is None:
        name = lm.info.DEFAULT_NAME
    schem = lm.Schematic(name=name, author="mc_diag_boat")
    if isinstance(blocks, lm.BlockState):
        blocks = [blocks]
    for index, region in enumerate(regioned_raster):
        schem.regions[str(index)] = _make_region(region, blocks)
    return schem
    #filename = smart_filename(schem_name + ".litematic")
    #schem.save(filename)
    #print("Saved schematic", filename)

