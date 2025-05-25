import litemapy as lm
from .types import Vec2


SXN_SIZE = 16


# Add gaps to a raster and segment it into small sections for inclusion in a schematic
def add_gaps(raster: list[Vec2], gap_size: int) -> list[Vec2]:
    return [
        coord
        for index, coord in enumerate(raster)
        if index % (gap_size + 1) == 0 or index == len(raster) - 1
    ]


def cut_sxns(points: list[Vec2], gap_size: int) -> list[list[Vec2]]:
    sxn_size = max(int(SXN_SIZE / (gap_size + 1)), 1)
    sxned = []
    return [
        uncut_path[sxn_start:min(sxn_start + sxn_size, len(uncut_path))]
        for sxn_start in range(0, len(uncut_path), sxn_size)
    ]


# Format a name for a schematic, including the given origin and destination coordinates
def name_schematic(origin: Vec2, destination: Vec2) -> str:
    return "path_" + str(origin) + "_" + str(destination)


# Create a Region object for a schematic, given a path (list of coordinates)
def make_region(path: list[list[int]], blocks: list[lm.BlockState]) -> lm.Region:
    if len(blocks) == 0:
        raise ValueError("Must be at least one BlockState provided.")
    path_span = (path[-1][0] - path[0][0] + (1 if path[-1][0] >= 0 else -1), path[-1][1] - path[0][1] + (1 if path[-1][1] >= 0 else -1))
    region = lm.Region(path[0][0], 0, path[0][1], path_span[0], len(blocks), path_span[1])
    for coords in path:
        for block_index, block_state in enumerate(blocks):
            region[coords[0] - path[0][0], block_index, coords[1] - path[0][1]] = block_state
    return region


# Create and save a Litematica schematic file (.litematic); name uses the current BOAT destination
def generate_schematic(offset: Vec2, gap_size: int = 0) -> lm.Schematic:
    #raster = rasterize(distance, BOAT_ANGLES[boat_angle_index])
    raster = offset.raster()
    gapped_path = add_gaps(raster, gap_size)
    sxned_path = cut_sxns(gapped_path)
    schem_name = name_schematic(origin_x.value, origin_z.value, boat_destination_g[0], boat_destination_g[1])
    schem = lm.Schematic(name=schem_name, author="mc_diag_boat")
    for sxn in sxned_path:
        schem.regions[f'{sxn}'] = make_region(sxn, blocks_g)
    return schem
    #filename = smart_filename(schem_name + ".litematic")
    #schem.save(filename)
    #print("Saved schematic", filename)

