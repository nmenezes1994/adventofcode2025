import sys
import math

MAX_JUNCTION_BOXES_TO_CONNECT: int = 1000
TOP_CIRCUITS_TO_COMPUTE: int = 3

class JunctionBox:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x: int = x
        self.y: int = y
        self.z: int = z

class Circuit:
    def __init__(self, junction_boxes: list[JunctionBox]) -> None:
        self.__junction_boxes: list[JunctionBox] = junction_boxes

    def get_junction_boxes(self) -> list[JunctionBox]:
        return self.__junction_boxes
    
    def contains(self, junction_box: JunctionBox) -> bool:
        return junction_box in self.__junction_boxes
    
    def count_junction_boxes(self) -> int:
        return len(self.__junction_boxes)

    def add_junction_boxes(self, junction_boxes: list[JunctionBox]) -> list[JunctionBox]:
        self.__junction_boxes.extend(junction_boxes)
        return self.get_junction_boxes()

def main(args: list[str]) -> None:
    distances: list[tuple[float, JunctionBox, JunctionBox]] = get_distances(args[1])
    circuits: list[Circuit] = connect_junction_boxes(distances)
    result: int = compute_result(circuits)

    print(f'The result is {result}')

    

def get_distances(file_name: str) -> list[tuple[float, JunctionBox, JunctionBox]]:
    distances: list[tuple[float, JunctionBox, JunctionBox]] = []
    junction_boxes: list[JunctionBox] = []

    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            junction_box: JunctionBox = JunctionBox(*list(map(int, line.strip().split(','))))
            junction_boxes.append(junction_box)

    for junction_box_index, junction_box in enumerate(junction_boxes):
        for next_junction_box in junction_boxes[junction_box_index + 1:]:
            distance = linear_distance(junction_box, next_junction_box)
            distances.append((distance, junction_box, next_junction_box))

    return distances

def linear_distance(first_junction_box: JunctionBox, second_junction_box: JunctionBox) -> float:
    return math.sqrt((first_junction_box.x - second_junction_box.x)**2 + (first_junction_box.y - second_junction_box.y)**2 + (first_junction_box.z - second_junction_box.z)**2)

def connect_junction_boxes(distances: list[tuple[float, JunctionBox, JunctionBox]]) -> list[Circuit]:
    circuits: list[Circuit] = []
    
    for distance in sorted(distances, key=lambda x: x[0])[:MAX_JUNCTION_BOXES_TO_CONNECT]:
        first_junction_box: JunctionBox = distance[1]
        second_junction_box: JunctionBox = distance[2]

        first_circuit = get_circuit(first_junction_box, circuits)
        second_circuit = get_circuit(second_junction_box, circuits)

        if (first_circuit is None) and (second_circuit is None):
            circuits.append(Circuit([first_junction_box, second_junction_box]))
        elif (first_circuit is not None) and (second_circuit is None):
            first_circuit.add_junction_boxes([second_junction_box])
        elif (first_circuit is None) and (second_circuit is not None):
            second_circuit.add_junction_boxes([first_junction_box])
        elif ((first_circuit is not None) and (second_circuit is not None)) and (first_circuit is not second_circuit):
            first_circuit.add_junction_boxes(second_circuit.get_junction_boxes())
            circuits.remove(second_circuit)

    return circuits

def get_circuit(junction_box: JunctionBox, circuits: list[Circuit]) -> Circuit | None:
    for circuit in circuits:
        if circuit.contains(junction_box):
            return circuit

    return None

def compute_result(circuits: list[Circuit]) -> int:
    top_circuit_sizes: list[int] = [circuit.count_junction_boxes() for circuit in sorted(circuits, key=lambda x: x.count_junction_boxes(),reverse=True)[:TOP_CIRCUITS_TO_COMPUTE]]
    return math.prod(top_circuit_sizes)

if __name__ == '__main__':
    main(sys.argv)