import dataclasses
import heapq
import math

with open('18.txt') as f:
    falling = [line.split(',') for line in f]
    falling = [(int(x), int(y)) for x, y in falling]

WORLD_SIZE = 71


@dataclasses.dataclass
class Matrix:
    score: {(int, int): float}


@dataclasses.dataclass(order=True)
class Branch:
    score: int
    xy: (int, int)


def solve_world(world: [[bool]]) -> Branch:
    branches = []
    heapq.heappush(branches, Branch(score=0, xy=(0, 0)))

    matrix = Matrix(
            score={(x, y): math.inf for x in range(len(world[0])) for y in range(len(world))},
    )

    while branches:
        print('Count of branches:', len(branches))
        branch: Branch = heapq.heappop(branches)

        # Check if we've already visited this cell
        if branch.score >= matrix.score[branch.xy]:
            continue
        else:
            matrix.score[branch.xy] = branch.score

        # Reached the end
        if branch.xy == (WORLD_SIZE - 1, WORLD_SIZE - 1):
            return branch

        # Move to a neighbor
        for delta_xy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_xy = (branch.xy[0] + delta_xy[0], branch.xy[1] + delta_xy[1])
            if 0 <= new_xy[0] < WORLD_SIZE and 0 <= new_xy[1] < WORLD_SIZE:
                if world[new_xy[1]][new_xy[0]]:
                    heapq.heappush(branches, Branch(score=branch.score + 1, xy=new_xy))


def create_world(disable_first_n) -> [[bool]]:
    world = []
    for _ in range(WORLD_SIZE):
        world.append([True] * WORLD_SIZE)
    for x, y in falling[:disable_first_n]:
        world[y][x] = False
    return world


def task_1() -> None:
    world = create_world(1024)
    sol = solve_world(world)
    print(sol.score)


def task_2() -> None:
    left, right = 0, len(falling)
    while left < right:
        middle = (left + right) // 2
        world = create_world(middle)
        sol = solve_world(world)
        if sol:
            left = middle + 1
        else:
            right = middle
    print(falling[left - 1])


if __name__ == '__main__':
    task_1()
    task_2()
