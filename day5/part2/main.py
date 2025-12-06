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

    for range_index, fresh_id_range in enumerate(fresh_id_ranges):
        unique_ids_in_range: int = fresh_id_range[UPPER] - fresh_id_range[LOWER] + 1

        for previous_fresh_id_range in fresh_id_ranges[:range_index]:
            if not (fresh_id_range[UPPER] < previous_fresh_id_range[LOWER] or fresh_id_range[LOWER] > previous_fresh_id_range[UPPER]):
                if fresh_id_range[LOWER] < previous_fresh_id_range[LOWER] and fresh_id_range[UPPER] <= previous_fresh_id_range[UPPER]:
                    unique_ids_in_range -= fresh_id_range[UPPER] - previous_fresh_id_range[LOWER] + 1
                elif fresh_id_range[UPPER] > previous_fresh_id_range[UPPER] and fresh_id_range[LOWER] >= previous_fresh_id_range[LOWER]:
                    unique_ids_in_range -= previous_fresh_id_range[UPPER] - fresh_id_range[LOWER] + 1
                elif (fresh_id_range[UPPER] - fresh_id_range[LOWER]) > (previous_fresh_id_range[UPPER] - previous_fresh_id_range[LOWER]):
                    unique_ids_in_range -= previous_fresh_id_range[UPPER] - previous_fresh_id_range[LOWER] + 1
                else:
                    unique_ids_in_range = 0

        num_fresh_ids += unique_ids_in_range

    return num_fresh_ids

# def count_fresh_ids(fresh_id_ranges: list[tuple[int, int]]) -> int:
#     num_fresh_ids: int = 0

#     merged_fresh_ids_ranges = merge_ranges(fresh_id_ranges)

#     for fresh_id_range in merged_fresh_ids_ranges:
#         num_fresh_ids += fresh_id_range[UPPER] - fresh_id_range[LOWER] + 1

#     return num_fresh_ids

def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged_ranges: list[tuple[int, int]] = [ranges[0]]

    for range in ranges[1:]:
        candidate_range: list[tuple[int, int]] = [range]

        for merged_range in merged_ranges:
            if not (range[UPPER] < merged_range[LOWER] or range[LOWER] > merged_range[UPPER]):
                if range[LOWER] < merged_range[LOWER] and range[UPPER] <= merged_range[UPPER]:
                    candidate_range = [(range[LOWER], merged_range[LOWER] - 1)]
                elif range[UPPER] > merged_range[UPPER] and range[LOWER] >= merged_range[LOWER]:
                    candidate_range = [(merged_range[UPPER] + 1, range[UPPER])]
                elif (range[UPPER] - range[LOWER]) > (merged_range[UPPER] - merged_range[LOWER]):
                    candidate_range = [(range[LOWER], merged_range[LOWER] - 1), (merged_range[UPPER] + 1, range[UPPER])]
                # range = (min(range[LOWER], merged_range[LOWER]), max(range[UPPER], merged_range[UPPER]))
        
        merged_ranges.extend(candidate_range)

    return merged_ranges

if __name__ == '__main__':
    main(sys.argv)