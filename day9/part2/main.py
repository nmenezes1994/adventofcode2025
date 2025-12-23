from enum import Enum
from itertools import batched

import sys
import csv

TILE_COLOR = 0
TILE_ROW = 1
TILE_COLUMN = 2
RED_TILE_ROW = 0
RED_TILE_COLUMN = 1

class EdgeDirection(Enum):
    RIGHT = 1
    LEFT = 2
    DOWN = 3
    UP = 4

def main(args: list[str]) -> None:
    tiles = get_tiles(args[1])
    exclusion_zone = get_exclusion_zones(tiles)
    result = get_largest_area(tiles, exclusion_zone)
    print(f'The result is {result}')

def get_tiles(file_name: str) -> list[tuple[str, int, int]]:
    tiles: list[tuple[str, int, int]] = []
    red_tiles: list[tuple[str, int, int]] = []
    
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            tile_column, tile_line = tuple(map(int, line.strip().split(',')))
            red_tiles.append(('red', tile_line, tile_column))

    for red_tile_idx, red_tile in enumerate(red_tiles):
        green_tiles: list[tuple[str, int, int]] = []

        next_red_tile = red_tiles[(red_tile_idx + 1) % len(red_tiles)]
        
        match get_direction(red_tile, next_red_tile):
            case EdgeDirection.RIGHT: 
                green_tiles = [('green', red_tile[TILE_ROW], column) for column in range(red_tile[TILE_COLUMN] + 1, next_red_tile[TILE_COLUMN])]
            case EdgeDirection.LEFT: 
                green_tiles = [('green', red_tile[TILE_ROW], column) for column in range(red_tile[TILE_COLUMN] - 1, next_red_tile[TILE_COLUMN], -1)]
            case EdgeDirection.DOWN: 
                green_tiles = [('green', row, red_tile[TILE_COLUMN]) for row in range(red_tile[TILE_ROW] + 1, next_red_tile[TILE_ROW])]
            case EdgeDirection.UP: 
                green_tiles = [('green', row, red_tile[TILE_COLUMN]) for row in range(red_tile[TILE_ROW] - 1, next_red_tile[TILE_ROW], -1)]

        tiles.append(red_tile)
        tiles.extend(green_tiles)

    return tiles

def get_direction(tile: tuple[str, int, int], next_tile: tuple[str, int, int]) -> EdgeDirection:
    delta_row: int = next_tile[TILE_ROW] - tile[TILE_ROW]
    delta_column: int = next_tile[TILE_COLUMN] - tile[TILE_COLUMN]

    if delta_row == 0:
        # Horizontal right
        if delta_column > 0:
            return EdgeDirection.RIGHT
        # Horizontal left
        else:
            return EdgeDirection.LEFT
    else:
        # Vertical down
        if delta_row > 0:
            return EdgeDirection.DOWN
        # Vertical up
        else:
            return EdgeDirection.UP

def get_exclusion_zones(tiles: list[tuple[str, int, int]]) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    horizontal_exclusion_zone: list[tuple[int, int]] = []
    vertical_exclusion_zone: list[tuple[int, int]] = []
    existing_tiles = set(map(lambda tile: (tile[TILE_ROW], tile[TILE_COLUMN]), tiles))

    red_tiles = list(filter(lambda tile: tile[TILE_COLOR] == 'red', tiles))

    for tile_idx, red_tile in enumerate(red_tiles):
        next_red_tile = red_tiles[(tile_idx + 1) % len(red_tiles)]

        exclusion_zone_edge_tiles: set[tuple[int, int]] = set()
        is_horizontal: bool = False

        match get_direction(red_tile, next_red_tile):
            case EdgeDirection.RIGHT: 
                is_horizontal = True
                exclusion_zone_edge_tiles.update([(red_tile[TILE_ROW] - 1, column) for column in range(red_tile[TILE_COLUMN], next_red_tile[TILE_COLUMN] + 1)])
            case EdgeDirection.LEFT: 
                is_horizontal = True
                exclusion_zone_edge_tiles.update([(red_tile[TILE_ROW] + 1, column) for column in range(red_tile[TILE_COLUMN], next_red_tile[TILE_COLUMN] - 1, -1)])
            case EdgeDirection.DOWN: 
                exclusion_zone_edge_tiles.update([(row, red_tile[TILE_COLUMN] + 1) for row in range(red_tile[TILE_ROW], next_red_tile[TILE_ROW] + 1)])
            case EdgeDirection.UP: 
                exclusion_zone_edge_tiles.update([(row, red_tile[TILE_COLUMN] - 1) for row in range(red_tile[TILE_ROW], next_red_tile[TILE_ROW] - 1, -1)])
        
        tmp = sorted(list(exclusion_zone_edge_tiles.difference(existing_tiles)))

        if is_horizontal:
            horizontal_exclusion_zone.append(tmp[0])
            horizontal_exclusion_zone.append(tmp[-1])
        else:
            vertical_exclusion_zone.append(tmp[0])
            vertical_exclusion_zone.append(tmp[-1])


    return (horizontal_exclusion_zone, vertical_exclusion_zone)

def get_largest_area(tiles: list[tuple[str, int, int]], exclusion_zone: tuple[list[tuple[int, int]], list[tuple[int, int]]]) -> int:
    largest_area: int = 0
    sorted_red_tiles = sorted(map(lambda tile: (tile[TILE_ROW], tile[TILE_COLUMN]),filter(lambda tile: tile[TILE_COLOR] == 'red', tiles)))

    for red_tile_idx, red_tile in enumerate(sorted_red_tiles):
        for next_red_tile in sorted_red_tiles[red_tile_idx + 1:]:
            if is_valid_rectangle(red_tile, next_red_tile, exclusion_zone):
                area: int = (next_red_tile[RED_TILE_ROW] - red_tile[RED_TILE_ROW] + 1) * (next_red_tile[RED_TILE_COLUMN] - red_tile[RED_TILE_COLUMN] + 1)
                if area > largest_area:
                    largest_area = area

    return largest_area

def is_valid_rectangle(top_corner: tuple[int, int], bottom_opposite_corner: tuple[int, int], exclusion_zone: tuple[list[tuple[int, int]], list[tuple[int, int]]]) -> bool:
    top_left_corner: tuple[int, int] = (top_corner[RED_TILE_ROW], min(top_corner[RED_TILE_COLUMN], bottom_opposite_corner[RED_TILE_COLUMN]))
    top_right_corner: tuple[int, int] = (top_corner[RED_TILE_ROW], max(top_corner[RED_TILE_COLUMN], bottom_opposite_corner[RED_TILE_COLUMN]))
    bottom_left_corner: tuple[int, int] = (bottom_opposite_corner[RED_TILE_ROW], min(top_corner[RED_TILE_COLUMN], bottom_opposite_corner[RED_TILE_COLUMN]))
    bottom_right_corner: tuple[int, int] = (bottom_opposite_corner[RED_TILE_ROW], max(top_corner[RED_TILE_COLUMN], bottom_opposite_corner[RED_TILE_COLUMN]))

    if intersects((top_left_corner, top_right_corner), exclusion_zone) or intersects((bottom_left_corner, bottom_right_corner), exclusion_zone) or intersects((top_right_corner, bottom_right_corner), exclusion_zone) or intersects((top_left_corner, bottom_left_corner), exclusion_zone):
        return False
    else:
        return True
    
def intersects(edge: tuple[tuple[int, int], tuple[int, int]], exclusion_zone: tuple[list[tuple[int, int]], list[tuple[int, int]]]):
    match get_direction(('', *edge[0]), ('', * edge[1])):
        case EdgeDirection.RIGHT | EdgeDirection.LEFT:
            for tile, next_tile in batched(exclusion_zone[1], n=2):
                edge_row = edge[0][0]
                tile_column = tile[1]
                if (tile[0] <= edge_row <= next_tile[0]) and (edge[0][1] <= tile_column <= edge[1][1]):
                    return True
        case EdgeDirection.DOWN | EdgeDirection.UP:
            for tile, next_tile in batched(exclusion_zone[0], n=2):
                edge_column = edge[0][1]
                tile_row = tile[0]
                if (tile[1] <= edge_column <= next_tile[1]) and (edge[0][0] <= tile_row <= edge[1][0]):
                    return True

    return False

if __name__ == '__main__':
    main(sys.argv)