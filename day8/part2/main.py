import sys
import math

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
    circuits, distances = get_distances(args[1])
    last_junction_boxes = connect_junction_boxes(circuits, distances)

    if last_junction_boxes is not None:
        result: int = compute_result(*last_junction_boxes)

        print(f'The result is {result}')

def get_distances(file_name: str) -> tuple[list[Circuit], list[tuple[float, JunctionBox, JunctionBox]]]:
    distances: list[tuple[float, JunctionBox, JunctionBox]] = []
    junction_boxes: list[JunctionBox] = []
    circuits: list[Circuit] = []

    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            junction_box: JunctionBox = JunctionBox(*list(map(int, line.strip().split(','))))
            junction_boxes.append(junction_box)
            circuits.append(Circuit([junction_box]))

    for junction_box_index, junction_box in enumerate(junction_boxes):
        for next_junction_box in junction_boxes[junction_box_index + 1:]:
            distance = linear_distance(junction_box, next_junction_box)
            distances.append((distance, junction_box, next_junction_box))

    return circuits, distances

def linear_distance(first_junction_box: JunctionBox, second_junction_box: JunctionBox) -> float:
    return math.sqrt((first_junction_box.x - second_junction_box.x)**2 + (first_junction_box.y - second_junction_box.y)**2 + (first_junction_box.z - second_junction_box.z)**2)

def connect_junction_boxes(circuits: list[Circuit], distances: list[tuple[float, JunctionBox, JunctionBox]]) -> tuple[JunctionBox, JunctionBox] | None:
    for distance in sorted(distances, key=lambda x: x[0]):
        first_junction_box: JunctionBox = distance[1]
        second_junction_box: JunctionBox = distance[2]

        first_circuit = get_circuit(first_junction_box, circuits)
        second_circuit = get_circuit(second_junction_box, circuits)

        if ((first_circuit is not None) and (second_circuit is not None)) and (first_circuit is not second_circuit):
            first_circuit.add_junction_boxes(second_circuit.get_junction_boxes())
            circuits.remove(second_circuit)
        
        if len(circuits) == 1:
            return first_junction_box, second_junction_box

def get_circuit(junction_box: JunctionBox, circuits: list[Circuit]) -> Circuit | None:
    for circuit in circuits:
        if circuit.contains(junction_box):
            return circuit

    return None

def compute_result(first_junction_box: JunctionBox, second_junction_box: JunctionBox) -> int:
    return first_junction_box.x * second_junction_box.x

if __name__ == '__main__':
    main(sys.argv)