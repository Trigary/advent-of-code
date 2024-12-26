def load_maze() -> [[int]]:
    with open('20.txt') as f:
        maze = [list(line.strip()) for line in f]

    cell_to_int = {
        'S': 0,
        '.': -1,
        '#': -2,
        'E': -3
    }

    return [[cell_to_int[c] for c in row] for row in maze]


def print_maze(maze: [[int]]) -> None:
    def int_to_str(x) -> str:
        if x == -1:
            return '.'
        elif x == -2:
            return '###'
        elif x == -3:
            return ' E '
        else:
            return str(x).rjust(3)

    for row in maze:
        print(''.join(int_to_str(c) for c in row))


def find_cell_xy(maze: [[int]], cell: int) -> (int, int):
    for y, row in enumerate(maze):
        for x, c in enumerate(row):
            if c == cell:
                return x, y
    raise ValueError(f'Cell {cell} not found in maze')


def solve_maze(maze: [[int]]) -> None:
    x, y = find_cell_xy(maze, 0)
    steps = -1
    while maze[y][x] != -3:
        steps += 1
        maze[y][x] = steps
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            cell = maze[y + dy][x + dx]
            if cell == -1 or cell == -3:
                x, y = x + dx, y + dy
                break
    maze[y][x] = steps + 1


def generate_deltas(total_delta: int) -> [(int, int)]:
    result = []
    for dx in range(-total_delta, total_delta + 1):
        for dy in range(-total_delta, total_delta + 1):
            if abs(dx) + abs(dy) <= total_delta:
                result.append((dx, dy))
    return result


def count_cheats(maze: [[int]], max_cheat_delta: int, min_diff: int) -> int:
    deltas = generate_deltas(max_cheat_delta)

    cheats = 0
    current_cell = 0
    x, y = find_cell_xy(maze, current_cell)
    while True:
        for dx, dy in deltas:
            if 0 <= y + dy < len(maze) and 0 <= x + dx < len(maze[0]):
                cheat_delta = abs(dx) + abs(dy)
                if maze[y + dy][x + dx] - current_cell >= min_diff + cheat_delta:
                    # print('Found cheat', current_cell - next_cell + cheat_delta)
                    cheats += 1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if maze[y + dy][x + dx] == current_cell + 1:
                x, y = x + dx, y + dy
                current_cell += 1
                break
        else:
            break
    return cheats


def main() -> None:
    maze = load_maze()
    solve_maze(maze)
    # print_maze(maze)
    min_diff = 100
    print(count_cheats(maze, 2, min_diff))
    print(count_cheats(maze, 20, min_diff))


if __name__ == '__main__':
    main()
