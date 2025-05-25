MAX_PATTERN_SIZE = 100
BOAT_ANGLES = [1.40625*placement for placement in range(-127,128)] + [180.0]
APPARENT_BOAT_ANGLES = [round(angle, 1) if angle > 0.0 else -1*round(abs(angle)+0.000000001, 1) for angle in BOAT_ANGLES]
BLOCK_OPTIONS = [
    'minecraft:blue_ice',
    'minecraft:packed_ice',
    'minecraft:ice',
    'minecraft:stone',
    'minecraft:stone_button',
    'minecraft:stone_pressure_plate',
    'minecraft:lever',
    'minecraft:rail',
]

