import dataclasses
import math


@dataclasses.dataclass
class Eq:
    result: int
    operands: [int]


eq_list = []
with open('7.txt') as f:
    for line in f:
        nums = line.split(' ')
        eq_list.append(Eq(int(nums[0][:-1]), [int(x) for x in nums[1:]]))


def can_solve_1(result: int, operands: [int], stop_i: int) -> bool:
    x = operands[stop_i - 1]
    if stop_i == 1:
        return result == x
    elif result < x:  # We never multiply by 0
        return False
    elif result % x == 0 and can_solve_1(result // x, operands, stop_i - 1):
        return True
    else:
        return can_solve_1(result - x, operands, stop_i - 1)


def can_solve_2(result: int, operands: [int], stop_i: int) -> bool:
    x = operands[stop_i - 1]
    if stop_i == 1:
        return result == x
    elif result < x:  # We never multiply by 0
        return False
    elif result % x == 0 and can_solve_2(result // x, operands, stop_i - 1):
        return True
    else:
        tens = 10 if x == 1 else 10 ** math.ceil(math.log10(x))
        if result % tens == x and can_solve_2(result // tens, operands, stop_i - 1):
            return True
        else:
            return can_solve_2(result - x, operands, stop_i - 1)


def main() -> None:
    result = 0
    for eq in eq_list:
        if can_solve_1(eq.result, eq.operands, len(eq.operands)):
            result += eq.result
    print(result)

    result = 0
    for eq in eq_list:
        if can_solve_2(eq.result, eq.operands, len(eq.operands)):
            result += eq.result
    print(result)


if __name__ == '__main__':
    main()
