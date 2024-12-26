import heapq

with open('12.txt') as f:
    world = [list(line.strip()) for line in f]


def explore(visited: {(int, int)}, y: int, x: int) -> (int, int, int):  # area, perimeter, border
    stack = [(y, x)]
    inside = set()
    target = world[y][x]
    area, perimeter, border = 0, 0, 0

    while stack:
        y, x = stack.pop()
        if (y, x) in visited:
            continue

        visited.add((y, x))
        area += 1
        inside.add((y, x))

        for i, (dy, dx) in enumerate([(1, 0), (-1, 0), (0, 1), (0, -1)]):
            if 0 <= y + dy < len(world) and 0 <= x + dx < len(world[0]) and world[y + dy][x + dx] == target:
                stack.append((y + dy, x + dx))
            else:
                perimeter += 1

    perimeter_sets = [set(), set(), set(), set()]
    heap = list(inside)
    heapq.heapify(heap)

    while heap:
        y, x = heapq.heappop(heap)
        for i, (dy, dx) in enumerate([(1, 0), (-1, 0), (0, 1), (0, -1)]):
            if 0 <= y + dy < len(world) and 0 <= x + dx < len(world[0]) and world[y + dy][x + dx] == target:
                pass
            else:
                perimeter_sets[i].add((y, x))
                if dy != 0:
                    if (y, x - 1) not in perimeter_sets[i]:
                        border += 1
                else:
                    if (y - 1, x) not in perimeter_sets[i]:
                        border += 1

    return area, perimeter, border


def main_1() -> None:
    visited = set()
    regions = []
    for y in range(len(world)):
        for x in range(len(world[y])):
            if (y, x) not in visited:
                regions.append(explore(visited, y, x))

    for r in regions:
        print(r)

    print(sum([area * perimeter for area, perimeter, border in regions]))
    print(sum([area * border for area, perimeter, border in regions]))


def main_2() -> None:
    pass


if __name__ == '__main__':
    main_1()
    main_2()
