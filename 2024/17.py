import dataclasses
from typing import Optional

with open('17.txt') as f:
    init_a = int(f.readline().split()[-1])
    init_b = int(f.readline().split()[-1])
    init_c = int(f.readline().split()[-1])
    f.readline()
    program = [int(x) for x in (f.readline().split()[-1]).split(',')]


@dataclasses.dataclass
class State:
    reg_a: int
    reg_b: int
    reg_c: int
    pointer: int


def read_literal(state: State) -> int:
    return program[state.pointer + 1]


def read_combo(state: State) -> int:
    v = program[state.pointer + 1]
    if 0 <= v <= 3:
        return v
    elif v == 4:
        return state.reg_a
    elif v == 5:
        return state.reg_b
    elif v == 6:
        return state.reg_c
    else:
        raise ValueError(f'Invalid combo value {v}')


def operate(state: State) -> Optional[int]:
    opcode = program[state.pointer]
    if opcode == 0:
        state.reg_a >>= read_combo(state)
        state.pointer += 2
        return None
    elif opcode == 1:
        state.reg_b ^= read_literal(state)
        state.pointer += 2
        return None
    elif opcode == 2:
        state.reg_b = read_combo(state) % 8
        state.pointer += 2
        return None
    elif opcode == 3:
        if state.reg_a == 0:
            state.pointer += 2
        else:
            state.pointer = read_literal(state)
        return None
    elif opcode == 4:
        state.reg_b ^= state.reg_c
        state.pointer += 2
        return None
    elif opcode == 5:
        res = read_combo(state) % 8
        state.pointer += 2
        return res
    elif opcode == 6:
        state.reg_b = state.reg_a >> read_combo(state)
        state.pointer += 2
        return None
    elif opcode == 7:
        state.reg_c = state.reg_a >> read_combo(state)
        state.pointer += 2
        return None


def main_1() -> None:
    state = State(init_a, init_b, init_c, 0)
    result = []
    while 0 <= state.pointer < len(program):
        res = operate(state)
        if res is not None:
            result.append(res)
    print(','.join((str(x) for x in result)))


def rec_solve(answer: int, triplets_computed: int) -> int:
    if triplets_computed == len(program):
        return answer

    next_output = program[len(program) - triplets_computed - 1]

    for answer_piece in range(8):
        state = State(answer << 3 | answer_piece, 0, 0, 0)
        while 0 <= state.pointer < len(program):
            output = operate(state)
            if output is not None:
                break
        else:
            raise ValueError("An output value should have been produced")
        if output == next_output:
            result = rec_solve(answer << 3 | answer_piece, triplets_computed + 1)
            if result is not None:
                return result


if __name__ == '__main__':
    main_1()
    print(rec_solve(0, 0))

# 2,4: b = a % 8
# 1,1: b = b ^ 1
# 7,5: c = a >> b
# 1,5: b = b ^ 5
# 4,0: b = b ^ c
# 5,5: out: b % 8
# 0,3: a = a >> 3
# 3,0: start over if a > 0 otherwise exit
#
# do
#   b = (a % 8) ^ 1
#   c = a >> b
#   b = b ^ 5 ^ c
#   print(b % 8)
#   a = a >> 3
# while a > 0

# do
#   print: (a % 8) ^ 4 ^ ((a >> ((a % 8) ^ 1)) % 8)
#   a = a >> 3
# while a > 0

# 2,4,1,1,7,5,1,5,4,0,5,5,0,3,3,0

# Starting at the end:
# 0 = (a[45:48] % 8) ^ 4 ^ 0  ->  a[45:48] = 4
# 3 = (a[42:45] % 8) ^ 4 ^ ?  ->  a[42:45] = 7
# 3 = (a[39:42] % 8) ^ 4 ^ ?  ->  a[39:42] = 7
