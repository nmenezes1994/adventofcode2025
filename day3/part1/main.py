import sys

def main(args):
    result = 0

    with open(args[1], 'r', encoding='utf-8') as f:
        for line in f:
            if line:
                batteries = list(map(int, list(line.strip())))
                bank_joltage = get_bank_joltage(batteries)
                print(bank_joltage)
                result += bank_joltage

    print(f'The result is {result}')

def get_bank_joltage(batteries):
    first_battery, pos = get_largest(batteries[:len(batteries)-1])
    second_battery, _ = get_largest(batteries[pos+1:])

    return int(str(first_battery) + str(second_battery))

def get_largest(subbank):
    largest = max(subbank)
    pos = subbank.index(largest)

    return largest, pos

if __name__ == '__main__':
    main(sys.argv)