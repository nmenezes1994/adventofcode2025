import sys
import re
import itertools

MANUAL_REGEX = r'^\[([\.#]+)\] +(\(\d+(?:,\d+)*\)(?: +\(\d+(?:,\d+)*\))+) +\{(\d+(?:,\d+)*)\}$'
MAX_COMBINATION_ITERATIONS = 100

def main(args: list[str]) -> None:
    result: int = 0

    with open(args[1], 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(MANUAL_REGEX, line.strip())
            
            target_joltage_levels: list[int] = list(map(int, match.group(3).split(',')))
            
            buttons: list[tuple[int, ...]] = []
            for button_str in match.group(2).split(' '):
                button = eval(button_str)
                if type(button) is int:
                    button = (button,)
                buttons.append(button)

            min_combination_size: int = max(target_joltage_levels)

            for combination_size in range(min_combination_size, min_combination_size + MAX_COMBINATION_ITERATIONS + 1):
                combination_found: bool = False
                button_combinations = itertools.combinations_with_replacement(buttons, combination_size)
                for button_combination in button_combinations:
                    pass
                    joltage_levels: list[int] = [0 for _ in range(len(target_joltage_levels))]
                    for button in button_combination:
                        for lever in button:
                            joltage_levels[lever] += 1
                    if joltage_levels == target_joltage_levels:
                        result += combination_size
                        combination_found = True
                        break 
                if combination_found:
                    break
                elif combination_size == min_combination_size + MAX_COMBINATION_ITERATIONS:
                    raise RuntimeError(f'Maximum number of combinations reached without result: {combination_size}')
                
    print(f'The result is {result}')

if __name__ == '__main__':
    main(sys.argv)