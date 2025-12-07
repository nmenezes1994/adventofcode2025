import sys
import re
from functools import reduce

def main(args: list[str]) -> None:
    problems = get_problems(args[1])
    
    result: int = 0
    for problem in problems:
        result += solve_problem(problem)

    print(f'The result is {result}')

def get_problems(file_name: str) -> list[tuple[str, list[int]]]:
    problems: list[tuple[str, list[int]]] = []
    raw_lines: list[list[str]] = []

    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            raw_lines.append(normalize_text(line).split(' '))

    raw_lines = [list(row) for row in zip(*raw_lines)]

    for raw_line in raw_lines:
        problems.append((raw_line[-1], list(map(int, raw_line[:-1]))))

    return problems

def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip())


def solve_problem(problem: tuple[str, list[int]]) -> int:
    result: int = 0

    match problem[0]:
        case '+':
            result = reduce(lambda x, y: x + y, problem[1])
        case '*':
            result = reduce(lambda x, y: x * y, problem[1])

    return result

if __name__ == '__main__':
    main(sys.argv)