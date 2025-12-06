import sys

def main(args: list[str]) -> None:
    fresh_id_ranges, available_ids = get_ids(args[1])
    fresh_available_ids = get_fresh_available_ids(fresh_id_ranges, available_ids)
    print(f'The result is {len(fresh_available_ids)}')

def get_ids(file_name: str) -> tuple[list[tuple[int, int]], list[int]]:
    fresh_id_ranges = []
    available_ids = []

    with open(file_name, 'r', encoding='utf-8') as f:
        in_fresh_id_range_section = True
        
        for line in f:
            if line.strip() == '':
                in_fresh_id_range_section = False
                continue

            if in_fresh_id_range_section:
                range_ends = list(map(int, line.strip().split('-')))
                fresh_id_ranges.append((range_ends[0], range_ends[1]))
            else:
                available_ids.append(int(line.strip()))
    
    return fresh_id_ranges, available_ids

def get_fresh_available_ids(fresh_id_ranges: list[tuple[int, int]], available_ids: list[int]) -> list[int]:
    fresh_available_ids: list[int] = []

    for available_id in available_ids:
        for fresh_id_range in fresh_id_ranges:
            if fresh_id_range[0] <= available_id <= fresh_id_range[1]:
                fresh_available_ids.append(available_id)
                break

    return fresh_available_ids

if __name__ == '__main__':
    main(sys.argv)