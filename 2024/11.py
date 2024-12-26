import math


def load() -> [int]:
    with open('11.txt') as f:
        return [int(x) for x in f.read().split()]


def advance(stones: [int]) -> [int]:
    out = []
    for stone in stones:
        if stone == 0:
            out.append(1)
        else:
            n_digits = math.ceil(math.log10(stone + 1))
            if n_digits % 2 == 0:
                divisor = 10 ** (n_digits // 2)
                out.append(stone // divisor)
                out.append(stone % divisor)
            else:
                out.append(stone * 2024)
    return out


def main_1() -> None:
    stones = load()
    print(stones)
    for i in range(25):
        stones = advance(stones)
        print(stones)
    print(len(stones))


stone_iters_to_length: {(int, int): int} = dict()


def get_length(stone: int, iters: int) -> int:
    if iters == 0:
        return 1
    res = stone_iters_to_length.get((stone, iters), None)
    if res is not None:
        return res

    if stone == 0:
        res = get_length(1, iters - 1)
    else:
        n_digits = math.ceil(math.log10(stone + 1))
        if n_digits % 2 == 0:
            divisor = 10 ** (n_digits // 2)
            res = get_length(stone // divisor, iters - 1) + get_length(stone % divisor, iters - 1)
        else:
            res = get_length(stone * 2024, iters - 1)

    stone_iters_to_length[(stone, iters)] = res
    return res


def main_2() -> None:
    stones = load()
    result = 0
    for stone in stones:
        result += get_length(stone, 75)
    print(result)


if __name__ == '__main__':
    main_1()
    main_2()
