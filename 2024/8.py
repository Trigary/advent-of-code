with open('8.txt') as f:
    world = [list(line.strip()) for line in f]

world_max_x, world_max_y = len(world[0]), len(world)

same_freq: {str: [(int, int)]} = dict()

for y, row in enumerate(world):
    for x, cell in enumerate(row):
        if cell == '.':
            continue
        if cell not in same_freq:
            same_freq[cell] = []
        same_freq[cell].append((x, y))

nodes: {(int, int)} = set()

for freq_list in same_freq.values():
    for freq_a in freq_list:
        for freq_b in freq_list:
            if freq_a == freq_b:
                continue

            diff = (freq_b[0] - freq_a[0], freq_b[1] - freq_a[1])
            nodes.add((freq_a[0] - diff[0], freq_a[1] - diff[1]))
            nodes.add((freq_b[0] + diff[0], freq_b[1] + diff[1]))

            if diff[0] % 3 == 0 and diff[1] % 3 == 0:
                nodes.add((freq_a[0] + diff[0] // 3, freq_a[1] + diff[1] // 3))
                nodes.add((freq_b[0] - diff[0] // 3, freq_b[1] - diff[1] // 3))

nodes = {(x, y) for x, y in nodes if 0 <= x < world_max_x and 0 <= y < world_max_y}

print(len(nodes))


def gcd(x, y) -> int:
    while y:
        x, y = y, x % y
    return x


nodes = set()

for freq_list in same_freq.values():
    for freq_a in freq_list:
        for freq_b in freq_list:
            if freq_a == freq_b:
                continue

            vec = (freq_b[0] - freq_a[0], freq_b[1] - freq_a[1])
            vec_gcd = gcd(abs(vec[0]), abs(vec[1]))
            vec = (vec[0] // vec_gcd, vec[1] // vec_gcd)

            x, y = freq_a
            while 0 <= x < world_max_x and 0 <= y < world_max_y:
                nodes.add((x, y))
                x += vec[0]
                y += vec[1]

            x, y = freq_a
            while 0 <= x < world_max_x and 0 <= y < world_max_y:
                nodes.add((x, y))
                x -= vec[0]
                y -= vec[1]

print(len(nodes))
