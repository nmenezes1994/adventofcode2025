import sys

ARGS_FILE_NAME_INDEX: int = 1
STARTING_DEVICE_NAME: str = 'svr'
REACTOR_DEVICE_NAME: str = 'out'

def main(args: list[str]) -> None:
    connections = get_connections(args[ARGS_FILE_NAME_INDEX])
    result = count_paths_to_reactor(connections, STARTING_DEVICE_NAME, {})
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

def count_paths_to_reactor(connections: dict[str, list[str]], current_device: str, known_paths: dict[str, int]) -> int:
    if current_device in known_paths:
        return known_paths[current_device]
    
    if current_device not in connections:
        known_paths[current_device] = 1
        return 1
    
    paths: int = 0
    for output in connections[current_device]:
        paths += count_paths_to_reactor(connections, output, known_paths)
    known_paths[current_device] = paths
    return paths

if __name__ == '__main__':
    main(sys.argv)