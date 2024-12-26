import dataclasses


@dataclasses.dataclass
class Task:
    button_a: (int, int)
    button_b: (int, int)
    target: (int, int)


def load_tasks() -> [Task]:
    result = []
    with open('13.txt') as f:
        while line := f.readline():
            split = line.strip().split(' ')
            button_a = int(split[2][2:-1]), int(split[3][2:])
            split = f.readline().strip().split(' ')
            button_b = int(split[2][2:-1]), int(split[3][2:])
            split = f.readline().strip().split(' ')
            target = int(split[1][2:-1]), int(split[2][2:])
            result.append(Task(button_a, button_b, target))
            f.readline()
    return result


def solve_task(task: Task) -> (int, int):
    # x_a * a + x_b * b = x_t
    # y_a * a + y_b * b = y_t
    # ----
    # b = (x_t - x_a * a) / x_b
    # b = (y_t - y_a * a) / y_b
    # ----
    # (x_t - x_a * a) / x_b = (y_t - y_a * a) / y_b
    # (x_t - x_a * a) * y_b = (y_t - y_a * a) * x_b
    # x_t * y_b - x_a * a * y_b = y_t * x_b - y_a * a * x_b
    # x_t * y_b - y_t * x_b = x_a * a * y_b - y_a * a * x_b
    # x_t * y_b - y_t * x_b = a * (x_a * y_b - y_a * x_b)
    # a = (x_t * y_b - y_t * x_b) / (x_a * y_b - y_a * x_b)

    x_a, y_a = task.button_a
    x_b, y_b = task.button_b
    x_t, y_t = task.target

    if (x_t * y_b - y_t * x_b) % (x_a * y_b - y_a * x_b) != 0:
        return None

    solved_a = (x_t * y_b - y_t * x_b) / (x_a * y_b - y_a * x_b)
    solved_b = (x_t - x_a * solved_a) / x_b
    return round(solved_a), round(solved_b)


def main() -> None:
    tasks = load_tasks()

    for task in tasks:
        if task.button_a[0] % task.button_b[0] == 0 and task.button_a[1] % task.button_b[1] == 0:
            print('A is divisible by B')
        if task.button_b[0] % task.button_a[0] == 0 and task.button_b[1] % task.button_a[1] == 0:
            print('B is divisible by A')

    result = 0
    for task in tasks:
        sol = solve_task(task)
        if sol is not None:
            result += sol[0] * 3 + sol[1]
    print(result)

    for task in tasks:
        task.target = (task.target[0] + 10000000000000, task.target[1] + 10000000000000)

    result = 0
    for task in tasks:
        sol = solve_task(task)
        if sol is not None:
            result += sol[0] * 3 + sol[1]
    print(result)


if __name__ == '__main__':
    main()
