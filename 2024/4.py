# Actually either returns 1 or 0: whether XMAS is present from the given start point in the given direction
def count1(grid, counter, start_x, start_y, step_x, step_y):
    for i, c in enumerate('XMAS'):
        x, y = start_x + i * step_x, start_y + i * step_y
        if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
            return 0
        if grid[start_y + i * step_y][start_x + i * step_x] != c:
            return 0
    for i in range(len('XMAS')):
        x, y = start_x + i * step_x, start_y + i * step_y
        counter[y][x] += 1
    return 1


def main1():
    with open('4.txt') as f:
        grid = [line.strip() for line in f]

    counter = [[0 for _ in grid[0]] for _ in grid]

    result = 0
    for start_x in range(len(grid[0])):
        for start_y in range(len(grid)):
            result += count1(grid, counter, start_x, start_y, 1, 0)
            result += count1(grid, counter, start_x, start_y, 0, 1)
            result += count1(grid, counter, start_x, start_y, -1, 0)
            result += count1(grid, counter, start_x, start_y, 0, -1)
            result += count1(grid, counter, start_x, start_y, 1, 1)
            result += count1(grid, counter, start_x, start_y, -1, -1)
            result += count1(grid, counter, start_x, start_y, 1, -1)
            result += count1(grid, counter, start_x, start_y, -1, 1)

    for row in counter:
        print(''.join(str(x) for x in row))
    print()
    print(result)


def count2(grid, x, y, tl, tr, bl, br):
    if grid[y][x] != 'A':
        return 0
    if grid[y - 1][x - 1] != tl or grid[y - 1][x + 1] != tr or grid[y + 1][x - 1] != bl or grid[y + 1][x + 1] != br:
        return 0
    return 1


def main2():
    with open('4.txt') as f:
        grid = [line.strip() for line in f]

    result = 0
    for start_x in range(1, len(grid[0]) - 1):
        for start_y in range(1, len(grid) - 1):
            result += count2(grid, start_x, start_y, 'M', 'M', 'S', 'S')
            result += count2(grid, start_x, start_y, 'M', 'S', 'M', 'S')
            result += count2(grid, start_x, start_y, 'S', 'M', 'S', 'M')
            result += count2(grid, start_x, start_y, 'S', 'S', 'M', 'M')

    print(result)


if __name__ == '__main__':
    main1()
    main2()
