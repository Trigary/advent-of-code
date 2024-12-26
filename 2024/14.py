import dataclasses
import re

SIZE_X, SIZE_Y = 101, 103


@dataclasses.dataclass
class Robot:
    pos: (int, int)
    vel: (int, int)

    def move(self, units: int) -> None:
        self.pos = (self.pos[0] + self.vel[0] * units, self.pos[1] + self.vel[1] * units)
        self.pos = (self.pos[0] % SIZE_X, self.pos[1] % SIZE_Y)

    def quadrant(self) -> int:
        x, y = self.pos
        if x < SIZE_X // 2:
            if y < SIZE_Y // 2:
                return 1
            elif y > SIZE_Y // 2:
                return 3
        elif x > SIZE_X // 2:
            if y < SIZE_Y // 2:
                return 2
            elif y > SIZE_Y // 2:
                return 4
        return 0


def load_robots() -> [Robot]:
    result = []
    with open('14.txt') as f:
        for line in f:
            match = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)
            if match:
                x, y, vx, vy = map(int, match.groups())
                result.append(Robot((x, y), (vx, vy)))
    return result


def main_1() -> None:
    robots: [Robot] = load_robots()

    for r in robots:
        r.move(100)

    quadrants = [0] * 5
    for r in robots:
        quadrants[r.quadrant()] += 1

    print(quadrants)
    print(quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4])


def organization_score(world: [[str]]) -> int:
    # Count the empty 3x3 squares
    result = 0
    for y in range(1, SIZE_Y - 1):
        for x in range(1, SIZE_X - 1):
            if all(world[y + dy][x + dx] == ' ' for dy in range(-1, 2) for dx in range(-1, 2)):
                result += 1
    return result


def main_2() -> None:
    robots: [Robot] = load_robots()

    start, end = 8200, 8300
    for r in robots:
        r.move(start - 1)

    for step_count in range(start, end + 1):
        for r in robots:
            r.move(1)

        world = [[' ' for _ in range(SIZE_X)] for _ in range(SIZE_Y)]
        for r in robots:
            world[r.pos[1]][r.pos[0]] = '■'

        if organization_score(world) < 6900:
            continue

        print(f"After {step_count} steps: (score: {organization_score(world)})")
        for row in world:
            print(''.join(row))
        print()
        input("Continue?")


if __name__ == "__main__":
    main_1()
    main_2()

# I found that the robots enter more organized positions periodically.
# In fact, there are two different periods. I found their intersection in a separate Python script:

# >>> a = [18 + 103 * x for x in range(1000)]
# >>> a[0:10]
# [18, 121, 224, 327, 430, 533, 636, 739, 842, 945]
# >>> b = [77 + 101 * x for x in range(1000)]
# >>> b[0:10]
# [77, 178, 279, 380, 481, 582, 683, 784, 885, 986]
# >>>
# >>>
# >>>
# >>> for x in b:
# ...   if x in a:
# ...     print(x)
# ...
# 8258
# 18661
# 29064
# 39467
# 49870
# 60273
# 70676
# 81079
# 91482
