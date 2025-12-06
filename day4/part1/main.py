import sys

MAX_NEIGHBOURS = 3
PAPER_SLOT = '@'

def main(args: list[str]) -> None:
    paper_grid = read_input(args[1])
    result = count_accessible_paper_rolls(paper_grid)
    print(f'The result is {result}')

def read_input(file_name: str) -> list[list[bool]]:
    paper_grid: list[list[bool]] = []

    with open(file_name, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f):
            paper_grid.append([])
            for char in list(line.strip()):
                paper_grid[line_number].append(char == PAPER_SLOT)

    return paper_grid


def count_accessible_paper_rolls(paper_grid: list[list[bool]]) -> int:
    accessible_paper_rolls: int = 0

    for row_number, row in enumerate(paper_grid):
        for slot_number, slot in enumerate(row):
            if slot and is_paper_roll_accessible(paper_grid, row_number, slot_number):
                accessible_paper_rolls += 1

    return accessible_paper_rolls

def is_paper_roll_accessible(paper_grid: list[list[bool]], row_number: int, slot_number: int) -> bool:
    num_of_neighbours: int = 0

    for row_delta, slot_delta in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        if (0 <= (row_number + row_delta) < len(paper_grid)) and (0 <= (slot_number + slot_delta) < len(paper_grid[row_number])):
            if paper_grid[row_number + row_delta][slot_number + slot_delta]:
                num_of_neighbours += 1
            
                if num_of_neighbours > MAX_NEIGHBOURS:
                    return False
    
    return True

if __name__ == '__main__':
    main(sys.argv)