with open('10.txt') as f:
    maze = [list(line.strip()) for line in f]
    maze = [[int(cell) for cell in row] for row in maze]

max_x, max_y = len(maze[0]), len(maze)

start_yx_list = []
for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == 0:
            start_yx_list.append((y, x))


def find_trails(head_yx: (int, int)) -> [(int, int)]:
    branches: [((int, int), int)] = [(head_yx, 0)]  # ((x,y), last_height)
    finished = []

    while branches:
        (last_y, last_x), last_height = branches.pop()
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if 0 <= last_x + dx < max_x and 0 <= last_y + dy < max_y:
                new_height = maze[last_y + dy][last_x + dx]
                if new_height != last_height + 1:
                    continue
                if new_height == 9:
                    finished.append((last_y + dy, last_x + dx))
                else:
                    branches.append(((last_y + dy, last_x + dx), new_height))

    return finished


result_1 = 0
result_2 = 0
for start_yx in start_yx_list:
    trails = find_trails(start_yx)
    result_1 += len(set(trails))
    result_2 += len(trails)

print(result_1)
print(result_2)
