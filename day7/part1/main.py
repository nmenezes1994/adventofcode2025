import sys

START_POS_TOKEN = 'S'
SPLITTER_TOKEN = '^'
RAY_TOKEN = '|'

def main(args: list[str]) -> None:
    manifold, start_pos = get_manifold(args[1])

    num_splits = get_num_splits(start_pos, manifold)

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

def get_num_splits(start_pos: int, manifold: list[list[str]]) -> int:

    if len(manifold[0]) < start_pos < 0:
        return 0

    manifold_column: list[str] = [list(row) for row in zip(*manifold)][start_pos]

    splitter_row: int = 0
    for line_number, cell in enumerate(manifold_column):
        if manifold[line_number][start_pos] == RAY_TOKEN:
            return 0
        elif cell == SPLITTER_TOKEN:
            splitter_row = line_number
            break
        else:
            manifold[line_number][start_pos] = RAY_TOKEN

    if splitter_row == 0:
        return 0

    left_splits: int = get_num_splits(start_pos - 1, manifold[splitter_row:])
    right_splits: int = get_num_splits(start_pos + 1, manifold[splitter_row:])

    return left_splits + right_splits + 1

if __name__ == '__main__':
    main(sys.argv)