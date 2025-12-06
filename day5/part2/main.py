import sys

LOWER = 0
UPPER = 1

def main(args: list[str]) -> None:
    fresh_id_ranges = get_fresh_id_ranges(args[1])
    num_fresh_ids = count_fresh_ids(fresh_id_ranges)
    print(f'The result is {num_fresh_ids}')

def get_fresh_id_ranges(file_name: str) -> list[tuple[int, int]]:
    fresh_id_ranges: list[tuple[int, int]] = []

    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == '':
                break

            range_ends = list(map(int, line.strip().split('-')))
            fresh_id_ranges.append((range_ends[0], range_ends[1]))
    
    return fresh_id_ranges

def count_fresh_ids(fresh_id_ranges: list[tuple[int, int]]) -> int:
    num_fresh_ids: int = 0

    merged_fresh_ids_ranges = merge_id_ranges(fresh_id_ranges)

    for fresh_id_range in merged_fresh_ids_ranges:
        num_fresh_ids += fresh_id_range[UPPER] - fresh_id_range[LOWER] + 1

    return num_fresh_ids

def merge_id_ranges(id_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged_id_ranges: list[tuple[int, int]] = id_ranges

    while True:
        next_merged_id_ranges: list[tuple[int, int]] = []
        merged_id_range_indexes: set[tuple[int, int]] = set()

        for id_range_index, current_id_range in enumerate(merged_id_ranges):
            if current_id_range not in merged_id_range_indexes:
                next_id_range: tuple[int, int] = current_id_range

                for id_range_to_compare in merged_id_ranges[id_range_index + 1:]:
                    if (id_range_to_compare not in merged_id_range_indexes) and not (next_id_range[UPPER] < id_range_to_compare[LOWER] or next_id_range[LOWER] > id_range_to_compare[UPPER]):
                        # There is an overlap between the current ID range and the next one in the list, so merge the two
                        next_id_range = (min(next_id_range[LOWER], id_range_to_compare[LOWER]), max(next_id_range[UPPER], id_range_to_compare[UPPER]))
                        merged_id_range_indexes.add(id_range_to_compare)

                next_merged_id_ranges.append(next_id_range)

        merged_id_ranges = next_merged_id_ranges

        if not merged_id_range_indexes:
            break

    return merged_id_ranges

if __name__ == '__main__':
    main(sys.argv)