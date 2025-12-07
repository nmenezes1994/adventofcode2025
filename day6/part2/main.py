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
    cells: list[list[str]] = []

    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            cells.append(list(line))

    cells = [list(row) for row in zip(*cells)]

    problem_numbers: list[str] = []
    problem_op: str = ''

    for column in cells:
        if all(s == ' ' for s in column):
            problems.append((problem_op.strip(), list(map(int, problem_numbers))))
            problem_numbers = []
            problem_op: str = ''
            continue

        problem_op += column[-1]
        problem_numbers.append(''.join(column[:-1]))

    problems.append((problem_op.strip(), list(map(int, problem_numbers))))

    return problems

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