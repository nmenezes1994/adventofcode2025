import sys

ARGS_FILE_NAME_INDEX: int = 1
STARTING_DEVICE_NAME: str = 'you'
REACTOR_DEVICE_NAME: str = 'out'

def main(args: list[str]) -> None:
    connections = get_connections(args[ARGS_FILE_NAME_INDEX])
    result = count_paths_to_reactor(connections, STARTING_DEVICE_NAME)
    print(f'The result is {result}')

def get_connections(file_name: str) -> dict[str, list[str]]:
    connections: dict[str, list[str]] = {}
    
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            tmp = line.split(':')
            device = tmp[0]
            outputs = tmp[1].split()

            connections[device] = outputs

    return connections

def count_paths_to_reactor(connections: dict[str, list[str]], current_device: str) -> int:
    outputs = connections[current_device]
    if len(outputs) == 1 and outputs[0] == REACTOR_DEVICE_NAME:
        return 1
    
    paths: int = 0
    for output in outputs:
        paths += count_paths_to_reactor(connections, output)
    return paths

if __name__ == '__main__':
    main(sys.argv)