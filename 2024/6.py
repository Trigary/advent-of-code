with open('6.txt') as f:
    world = [list(line.strip()) for line in f]


def find_char(c) -> (int, int):
    for y, row in enumerate(world):
        for x, cell in enumerate(row):
            if cell == c:
                return x, y
    raise ValueError(f'Character {c} not found in world')


def step(x, y, dx, dy):
    if world[y + dy][x + dx] != '#':
        return x + dx, y + dy, dx, dy
    elif dx == 0 and dy == -1:
        return x, y, 1, 0
    elif dx == 1 and dy == 0:
        return x, y, 0, 1
    elif dx == 0 and dy == 1:
        return x, y, -1, 0
    else:
        return x, y, 0, -1


def valid_4_tuple(x, y, dx, dy) -> bool:
    return 0 <= x + dx < len(world[0]) and 0 <= y + dy < len(world)


def main():
    # noinspection PyTupleAssignmentBalance
    start_x, start_y, start_dx, start_dy = *find_char('^'), 0, -1
    x, y, dx, dy = start_x, start_y, start_dx, start_dy

    visited: {(int, int)} = {(x, y)}
    while valid_4_tuple(x, y, dx, dy):
        x, y, dx, dy = step(x, y, dx, dy)
        visited.add((x, y))

    print(len(visited))

    solution_2: [(int, int)] = []
    visited.remove((start_x, start_y))

    for obs_x, obs_y in visited:
        world[obs_y][obs_x] = '#'

        fast = start_x, start_y, start_dx, start_dy
        slow = fast
        while valid_4_tuple(*slow) and valid_4_tuple(*fast):
            slow = step(*slow)
            fast = step(*fast)
            if not valid_4_tuple(*fast):
                break
            fast = step(*fast)
            if slow == fast:
                solution_2.append((obs_x, obs_y))
                break

        world[obs_y][obs_x] = '.'

    print(len(solution_2))


if __name__ == '__main__':
    main()
