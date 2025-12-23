import sys
import re
import itertools

MANUAL_REGEX = r'^\[([\.#]+)\] +(\(\d+(?:,\d+)*\)(?: +\(\d+(?:,\d+)*\))+) +\{(\d+(?:,\d+)*)\}$'
MAX_COMBINATION_SIZE = 20

def main(args: list[str]) -> None:
    result: int = 0

    with open(args[1], 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(MANUAL_REGEX, line.strip())
            
            target_indicator_lights: list[int] = list(map(lambda light: 0 if light == '.' else 1, match.group(1)))
            
            buttons: list[tuple[int, ...]] = []
            for button_str in match.group(2).split(' '):
                button = eval(button_str)
                if type(button) is int:
                    button = (button,)
                buttons.append(button)

            for combination_size in range(1, MAX_COMBINATION_SIZE + 1):
                combination_found: bool = False
                button_combinations = itertools.combinations_with_replacement(buttons, combination_size)
                for button_combination in button_combinations:
                    pass
                    indicator_lights: list[int] = [0 for _ in range(len(target_indicator_lights))]
                    for button in button_combination:
                        for light in button:
                            indicator_lights[light] += 1
                            indicator_lights[light] %= 2
                    if indicator_lights == target_indicator_lights:
                        result += combination_size
                        combination_found = True
                        break 
                if combination_found:
                    break
                elif combination_size == MAX_COMBINATION_SIZE:
                    raise RuntimeError(f'Maximum number of combinations reached without result: {combination_size}')
                
    print(f'The result is {result}')

if __name__ == '__main__':
    main(sys.argv)