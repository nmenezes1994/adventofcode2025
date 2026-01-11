import sys

ARGS_FILE_NAME_INDEX: int = 1
STARTING_DEVICE_NAME: str = 'svr'
REACTOR_DEVICE_NAME: str = 'out'
DAC_DEVICE_NAME: str = 'dac'
FFT_DEVICE_NAME: str = 'fft'

def main(args: list[str]) -> None:
    connections = get_connections(args[ARGS_FILE_NAME_INDEX])
    _, result, _, _ = count_paths_to_reactor(connections, STARTING_DEVICE_NAME, {})
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

def count_paths_to_reactor(connections: dict[str, list[str]], current_device: str, known_paths: dict[str, tuple[int, int, int, int]]) -> tuple[int, int, int, int]:
    if current_device in known_paths:
        return known_paths[current_device]
    
    if current_device not in connections:
        known_paths[current_device] = (1, 0, 0, 0)
        return known_paths[current_device]
    
    is_dac: bool = current_device == DAC_DEVICE_NAME
    is_fft: bool = current_device == FFT_DEVICE_NAME

    total_paths: int = 0
    total_valid_paths: int = 0
    total_paths_with_dac: int = 0
    total_paths_with_fft: int = 0
    for output in connections[current_device]:
        paths, valid_paths, paths_with_dac, paths_with_fft = count_paths_to_reactor(connections, output, known_paths)
        
        total_paths += paths

        if is_dac:
            if paths_with_fft > 0:
                total_valid_paths += paths_with_fft
            else:
                total_paths_with_dac += paths
        elif is_fft:
            if paths_with_dac > 0:
                total_valid_paths += paths_with_dac
            else:
                total_paths_with_fft += paths
        else:
            total_valid_paths += valid_paths
            total_paths_with_dac += paths_with_dac
            total_paths_with_fft += paths_with_fft

    known_paths[current_device] = (total_paths, total_valid_paths, total_paths_with_dac, total_paths_with_fft)

    return known_paths[current_device]

if __name__ == '__main__':
    main(sys.argv)