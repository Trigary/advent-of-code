def load_available_list() -> [str]:
    with open('19.txt') as f:
        return f.readline().strip().split(', ')


def load_task_list() -> [str]:
    with open('19.txt') as f:
        f.readline()
        f.readline()
        return [line.strip() for line in f]


def is_solveable(basic: {str}, can_be_solved_n: {str: int}, task: str) -> int:
    if task == '':
        return 1

    ans = can_be_solved_n.get(task, None)
    if ans is not None:
        return ans

    ans = 0
    for sub in basic:
        if task.startswith(sub):
            ans += is_solveable(basic, can_be_solved_n, task[len(sub):])

    can_be_solved_n[task] = ans
    return ans


def main() -> None:
    can_be_solved_n = dict()
    basic = set(load_available_list())
    task_list = load_task_list()

    result = 0
    for task in task_list:
        result += 1 if 0 < is_solveable(basic, can_be_solved_n, task) else 0
    print(result)

    result = 0
    for task in task_list:
        print(task, is_solveable(basic, can_be_solved_n, task))
        result += is_solveable(basic, can_be_solved_n, task)
    print(result)


if __name__ == '__main__':
    main()
