def load_data() -> ([[str]], [str]):
    with open('15.txt') as f:
        world = []
        for line in f:
            line = line.strip()
            if line == '':
                break
            else:
                world.append(list(line))

        moves = []
        for line in f:
            moves.extend(line.strip())

        return world, moves


def scale_world(world: [[str]]) -> [[str]]:
    to_new = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
    new_world = []
    for row in world:
        new_row = []
        for cell in row:
            new_row.extend(to_new[cell])
        new_world.append(new_row)
    return new_world


def find_robot(world: [[str]]) -> (int, int):
    for y, row in enumerate(world):
        for x, cell in enumerate(row):
            if cell == '@':
                return y, x


def execute_simple_move(world: [[str]], robot: (int, int), move: str) -> (int, int):
    dy, dx = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}[move]

    new_y, new_x = robot
    while True:
        new_y, new_x = new_y + dy, new_x + dx
        if world[new_y][new_x] == '#':
            return robot
        elif world[new_y][new_x] == 'O':
            continue
        else:
            new_robot = (robot[0] + dy, robot[1] + dx)
            world[new_y][new_x] = 'O'
            world[new_robot[0]][new_robot[1]] = '@'
            world[robot[0]][robot[1]] = '.'
            return new_robot


def calc_gps_sum(world: [[str]]) -> int:
    result = 0
    for y, row in enumerate(world):
        for x, cell in enumerate(row):
            if cell == 'O' or cell == '[':
                result += y * 100 + x
    return result


def execute_advanced_move(world: [[str]], robot: (int, int), move: str) -> (int, int):
    dy, dx = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}[move]

    to_move = []
    head = [robot]
    while head:
        y, x = head.pop(0)
        if (y, x) in to_move:
            continue
        to_move.append((y, x))
        new_y, new_x = y + dy, x + dx
        if world[new_y][new_x] == '#':
            return robot
        elif world[new_y][new_x] == '[':
            head.append((new_y, new_x))
            if dy != 0:
                head.append((new_y, new_x + 1))
        elif world[new_y][new_x] == ']':
            head.append((new_y, new_x))
            if dy != 0:
                head.append((new_y, new_x - 1))
        else:
            continue

    for cell in reversed(to_move):
        y, x = cell
        if world[y + dy][x + dx] != '.':
            raise ValueError('Collision, move: ' + move + ', xy: ' + str((y, x)) + ', dxy: ' + str((dy, dx)))
        world[y + dy][x + dx] = world[y][x]
        world[y][x] = '.'

    return robot[0] + dy, robot[1] + dx


def main_1() -> None:
    world, moves = load_data()
    robot = find_robot(world)
    for move in moves:
        robot = execute_simple_move(world, robot, move)
        # for row in world:
        #     print(''.join(row))
        # print()

    print(calc_gps_sum(world))


def main_2() -> None:
    world, moves = load_data()
    world = scale_world(world)
    robot = find_robot(world)

    # for row in world:
    #     print(''.join(row))
    # print()

    for move in moves:
        robot = execute_advanced_move(world, robot, move)
        # for row in world:
        #     print(''.join(row))
        # print()

    print(calc_gps_sum(world))


if __name__ == '__main__':
    main_1()
    main_2()
