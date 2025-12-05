import sys

NUM_BATTERIES_IN_BANK = 12

def main(args):
    result = 0

    with open(args[1], 'r', encoding='utf-8') as f:
        for line in f:
            if line:
                batteries = list(map(int, list(line.strip())))
                result += get_bank_joltage(batteries)

    print(f'The result is {result}')

def get_bank_joltage(batteries):
    bank_joltage = 0
    batteries_remaining = NUM_BATTERIES_IN_BANK

    while (batteries_remaining > 0):
        next_battery, pos = get_largest(batteries[:len(batteries) - (batteries_remaining - 1)])
        bank_joltage = int(str(bank_joltage) + str(next_battery))

        batteries = batteries[pos+1:]
        batteries_remaining -= 1

    return bank_joltage

def get_largest(subbank):
    largest = max(subbank)
    pos = subbank.index(largest)

    return largest, pos

if __name__ == '__main__':
    main(sys.argv)