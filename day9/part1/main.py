import sys

LINE = 0
COLUMN = 1

def main(args: list[str]) -> None:
    red_tiles = get_red_tiles(args[1])
    areas = get_areas(red_tiles)
    result: int = areas[0]
    print(f'The result is {result}')

def get_red_tiles(file_name: str) -> list[tuple[int, int]]:
    red_tiles: list[tuple[int, int]] = []
    
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            tile_column, tile_line = tuple(map(int, line.strip().split(',')))
            red_tiles.append((tile_line, tile_column))
        
    red_tiles.sort()

    return red_tiles

def get_areas(red_tiles: list[tuple[int, int]]) -> list[int]:
    areas: list[int] = []

    for red_tile_idx, red_tile in enumerate(red_tiles):
        for next_red_tile in red_tiles[red_tile_idx + 1:]:
            area: int = (next_red_tile[LINE] - red_tile[LINE] + 1) * (next_red_tile[COLUMN] - red_tile[COLUMN] + 1)
            areas.append(area)

    areas.sort(reverse=True)
    return areas

if __name__ == '__main__':
    main(sys.argv)