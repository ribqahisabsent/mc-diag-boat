from typing import Sequence
import litemapy as lm
from .vec2 import Vec2


SXN_SIZE = 16


# Add gaps to a raster and segment it into small sections for inclusion in a schematic
def add_gaps(raster: Sequence[Vec2[int]], gap_size: int) -> list[Vec2[int]]:
    return [
        coord
        for index, coord in enumerate(raster)
        if index % (gap_size + 1) == 0 or index == len(raster) - 1
    ]


def cut_regions(points: Sequence[Vec2[int]]) -> list[Sequence[Vec2[int]]]:
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


# Format a name for a schematic, including the given origin and destination coordinates
def name_schematic(origin: Vec2[int], destination: Vec2[int]) -> str:
    return "dbpath_" + str(origin).replace(" ", "") + "_" + str(destination).replace(" ", "")


# Create a Region object for a schematic, given a path (list of coordinates)
def make_region(path: Sequence[Vec2[int]], blocks: Sequence[lm.BlockState]) -> lm.Region:
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
    gapped_raster = add_gaps(raster, gap_size)
    regioned_raster = cut_regions(gapped_raster)
    if name is None:
        name = lm.info.DEFAULT_NAME
    schem = lm.Schematic(name=name, author="mc_diag_boat")
    if isinstance(blocks, lm.BlockState):
        blocks = [blocks]
    for index, region in enumerate(regioned_raster):
        schem.regions[str(index)] = make_region(region, blocks)
    return schem
    #filename = smart_filename(schem_name + ".litematic")
    #schem.save(filename)
    #print("Saved schematic", filename)

