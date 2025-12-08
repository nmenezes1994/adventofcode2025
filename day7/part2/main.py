import sys
import re

START_POS_TOKEN = 'S'
SPACE_TOKEN = '.'

def main(args: list[str]) -> None:
    manifold, start_pos = get_manifold(args[1])
    number_of_lines = len(manifold)

    num_splits = get_num_paths(start_pos, manifold, number_of_lines)

    print(f'The result is {num_splits}')

def get_manifold(file_name: str) -> tuple[list[list[str]], int]:
    start_pos: int
    manifold: list[list[str]] = []

    with open(file_name, 'r', encoding='utf-8') as f:
        start_pos = f.readline().find(START_POS_TOKEN)

        for line_number, line in enumerate(f):
            manifold.append([])
            for char in list(line.strip()):
                manifold[line_number].append(char)

    return (manifold, start_pos)

def get_num_paths(start_pos: int, manifold: list[list[str]], number_of_lines) -> int:

    if len(manifold[0]) < start_pos < 0:
        return 0

    manifold_column: list[str] = [list(row) for row in zip(*manifold)][start_pos]

    splitter_row = next((i for i, ch in enumerate(manifold_column) if ch != SPACE_TOKEN), -1)
    if splitter_row == -1:
        return 1
    elif manifold_column[splitter_row].isnumeric():
        return int(manifold_column[splitter_row])
    else:
        num_paths: int = get_num_paths(start_pos - 1, manifold[splitter_row:], number_of_lines) + get_num_paths(start_pos + 1, manifold[splitter_row:], number_of_lines)
        
        manifold[splitter_row][start_pos] = str(num_paths)

        return num_paths

if __name__ == '__main__':
    main(sys.argv)