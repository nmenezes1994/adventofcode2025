if __name__ == '__main__':
    position = 50
    password = 0

    with open('/home/nmenezes/repos/adventofcode2025/day1/secret_entrance/input.txt', 'r', encoding='utf-8') as f:
        for line in f:
            initial_position = position

            direction = line[0]
            delta= int(line[1:])

            full_rotations = abs(delta) // 100
            password += full_rotations
            
            rotation = delta % 100

            match direction:
                case 'L':
                    position -= rotation
                case 'R':
                    position += rotation
            
            if (initial_position != 0 and position < 0) or position > 100:
                password += 1

            position %= 100

            if position == 0:
                password += 1
    
    print(f'The password is: {password}')
