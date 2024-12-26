import copy
import dataclasses
import heapq
import math
from typing import Dict, List, Set, Tuple

with open('16.txt') as f:
    maze = [list(line.strip()) for line in f]

start_xy = (1, len(maze) - 2)
end_xy = (len(maze[0]) - 2, 1)


@dataclasses.dataclass
class Matrix:
    score: Dict[Tuple[int, int], float]
    prev: Dict[Tuple[int, int], Set[Tuple[int, int, str]]]


@dataclasses.dataclass(order=True)
class Branch:
    score: int
    xy: Tuple[int, int]
    facing: str
    prev_xyf: Tuple[int, int, str]


default_matrix = Matrix(
        score={(x, y): math.inf for x in range(len(maze[0])) for y in range(len(maze))},
        prev={(x, y): set() for x in range(len(maze[0])) for y in range(len(maze))},
)

facing_to_matrix: Dict[str, Matrix] = {
    'N': copy.deepcopy(default_matrix),
    'S': copy.deepcopy(default_matrix),
    'E': copy.deepcopy(default_matrix),
    'W': copy.deepcopy(default_matrix),
}

branches = []
heapq.heappush(branches, Branch(score=0, facing='E', xy=start_xy, prev_xyf=(start_xy[0], start_xy[1], 'E')))
finishers: List[Branch] = []

while branches:
    print('Count of branches:', len(branches))
    branch: Branch = heapq.heappop(branches)

    # Check if we've already visited this cell
    matrix = facing_to_matrix[branch.facing]
    if branch.score > matrix.score[branch.xy]:
        continue
    elif branch.score == matrix.score[branch.xy]:
        matrix.prev[branch.xy].add(branch.prev_xyf)
        continue
    else:
        matrix.score[branch.xy] = branch.score
        matrix.prev[branch.xy] = {branch.prev_xyf}

    # Reached the end
    if maze[branch.xy[1]][branch.xy[0]] == 'E':
        finishers.append(branch)
        continue

    # Move to a neighbor
    for delta_xy, new_facing in [((0, -1), 'N'), ((0, 1), 'S'), ((1, 0), 'E'), ((-1, 0), 'W')]:
        new_xy = (branch.xy[0] + delta_xy[0], branch.xy[1] + delta_xy[1])
        if new_xy == (branch.prev_xyf[0], branch.prev_xyf[1]):
            continue
        if maze[new_xy[1]][new_xy[0]] == '#':
            continue

        new_score = branch.score + 1
        if new_facing != branch.facing:
            new_score += 1000
        heapq.heappush(branches, Branch(score=new_score, xy=new_xy, facing=new_facing,
                                        prev_xyf=(branch.xy[0], branch.xy[1], branch.facing)))

for finisher in finishers:
    print(finisher)

finisher_min_score = min(finisher.score for finisher in finishers)

best_cells: Set[Tuple[int, int]] = {end_xy}
xy_facing_queue: List[Tuple[Tuple[int, int], str]] = [(f.xy, f.facing) for f in finishers
                                                      if f.score == finisher_min_score]
already_queued: Set[Tuple[Tuple[int, int], str]] = set(xy_facing_queue)
while xy_facing_queue:
    xy, facing = xy_facing_queue.pop(0)
    for prev_x, prev_y, prev_facing in facing_to_matrix[facing].prev[xy]:
        prev_xy = (prev_x, prev_y)
        best_cells.add(prev_xy)
        if (prev_xy, prev_facing) not in already_queued:
            already_queued.add((prev_xy, prev_facing))
            xy_facing_queue.append((prev_xy, prev_facing))

print(len(best_cells))
