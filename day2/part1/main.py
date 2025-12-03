import sys
import re

FILE_ENCODING: str = 'utf-8'
RANGE_SEP: str = ','
RANGE_ENDS_SEP: str = '-'
INVALID_ID_REGEX: str = r'^(\d+)\1$'


def main(args: list[str]) -> None:
    result: int = 0

    ranges = read_input(args[1])

    for range in ranges:
        invalid_ids = get_invalid_ids(range[0], range[1])
        result += sum(invalid_ids)

    print(f'The result is: {result}')

def read_input(file: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []

    with open(file, 'r', encoding=FILE_ENCODING) as f:
        line = f.readline()

        for range in line.split(RANGE_SEP):
            range_ends = range.split(RANGE_ENDS_SEP)
            
            start = int(range_ends[0])
            end = int(range_ends[1])

            ranges.append((start, end))
    
    return ranges
            
def get_invalid_ids(range_start: int, range_end: int) -> list[int]:
    invalid_ids: list[int] = []

    for id in range(range_start, range_end + 1):
        if is_id_invalid(id):
            invalid_ids.append(id)
    
    return invalid_ids

def is_id_invalid(id: int) -> bool:
    p = re.compile(INVALID_ID_REGEX)
    if p.match(str(id)):
        return True
    else:
        return False

if __name__ == '__main__':
    main(sys.argv)