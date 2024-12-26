import math


def calculate_steps(grid: [[str]], up_first: bool) -> {(str, str): [(str, str)]}:
    button_to_xy = dict()
    for y, row in enumerate(grid):
        for x, button in enumerate(row):
            if button != ' ':
                button_to_xy[button] = (x, y)

    result = dict()
    for target, (tx, ty) in button_to_xy.items():
        for current, (cx, cy) in button_to_xy.items():
            if target == current:
                continue

            sub_result = []
            if ty > cy:
                sub_result.append(('v', grid[cy + 1][cx + 0]))
            elif ty < cy:
                sub_result.append(('^', grid[cy - 1][cx + 0]))
            if tx > cx:
                sub_result.append(('>', grid[cy + 0][cx + 1]))
            elif tx < cx:
                sub_result.append(('<', grid[cy + 0][cx - 1]))
            # if up_first:
            #     if ty < cy:
            #         sub_result.append(('^', grid[cy - 1][cx + 0]))
            #     elif tx > cx:
            #         sub_result.append(('>', grid[cy + 0][cx + 1]))
            #     elif ty > cy:
            #         sub_result.append(('v', grid[cy + 1][cx + 0]))
            #     elif tx < cx:
            #         sub_result.append(('<', grid[cy + 0][cx - 1]))
            # else:
            #     if tx > cx:
            #         sub_result.append(('>', grid[cy + 0][cx + 1]))
            #     elif ty > cy:
            #         sub_result.append(('v', grid[cy + 1][cx + 0]))
            #     elif ty < cy:
            #         sub_result.append(('^', grid[cy - 1][cx + 0]))
            #     elif tx < cx:
            #         sub_result.append(('<', grid[cy + 0][cx - 1]))
            result[(target, current)] = [(step, nc) for step, nc in sub_result if nc != ' ']
    return result


# (target, current_pos) -> [(step, new_pos)]
NUMERIC_STEPS = calculate_steps(
        [['7', '8', '9'],
         ['4', '5', '6'],
         ['1', '2', '3'],
         [' ', '0', 'A']], up_first=True
)
DIRECTIONAL_STEPS = calculate_steps(
        [[' ', '^', 'A'],
         ['<', 'v', '>']], up_first=False
)


def keep_min_length(lists: [[str]]) -> [[str]]:
    min_length = min(len(path) for path in lists)
    return [path for path in lists if len(path) == min_length]


def press_buttons(target: str, current_pos: str, steps_dict) -> [[str]]:
    result = []
    head = [(current_pos, [])]
    while head:
        (current_pos, path) = head.pop()
        if current_pos == target:
            result.append(path + ["A"])
            continue
        for step, new_pos in steps_dict[(target, current_pos)]:
            head.append((new_pos, path + [step]))
    result = keep_min_length(result)

    # If the same button is pressed multiple times, then do so in adjacent steps
    step_count = dict()
    for step in result[0]:
        step_count[step] = step_count.get(step, 0) + 1

    final_result = []
    for path in result:
        i = 0
        valid = True
        while valid and i < len(path):
            step = path[i]
            for j in range(1, step_count[step]):
                i += 1
                if path[i] != step:
                    valid = False
                    break
            i += 1
        if valid:
            final_result.append(path)
    return final_result


def calculate_press_cache(steps_cache: {(str, str): [(str, str)]}) -> {(str, str): [[str]]}:
    result = dict()
    cells = [target for target, _ in steps_cache.keys()]
    for target in cells:
        for current in cells:
            result[(target, current)] = press_buttons(target, current, steps_cache)
    return result


PRESS_NUMERIC_CACHE = calculate_press_cache(NUMERIC_STEPS)
PRESS_DIRECTIONAL_CACHE = calculate_press_cache(DIRECTIONAL_STEPS)


def load_codes() -> [str]:
    with open("21.txt") as f:
        return [line.strip() for line in f]


def calculate_required_moves(path: [[str]]) -> int:
    result = 0
    last_button = path[0]
    for button in path[1:]:
        result += len(PRESS_DIRECTIONAL_CACHE[(last_button, button)][0])
        last_button = button
    return result


def calc_steps(to_press_alternatives: [[str]], press_cache) -> [[str]]:
    final_result, min_length, min_to_press = [], math.inf, None
    for to_press in to_press_alternatives:
        last_button, sub_result = "A", [[]]
        for indirect_button in to_press:
            old_sub_result, sub_result = sub_result, []
            for direct_path in press_cache[(indirect_button, last_button)]:
                for b2_sub_result in old_sub_result:
                    sub_result.append(b2_sub_result + direct_path)
            last_button = indirect_button
            if len(sub_result[0]) > min_length:
                break
        else:
            if not math.isinf(min_length) and min_length > len(sub_result[0]):
                print(f'New best path: {to_press}; worse alternative: {min_to_press}')
            min_length, min_to_press = min(min_length, len(sub_result[0])), to_press
            final_result.extend(sub_result)
    # print(f'Best path: {min_to_press}; alternatives: {[x for x in to_press_alternatives if x != min_to_press]}')
    final_result = keep_min_length(final_result)
    min_required_moves = min(calculate_required_moves(path) for path in final_result)
    return [path for path in final_result if calculate_required_moves(path) == min_required_moves]


def solve(code: str, directional_count: int) -> [str]:
    result = calc_steps([code], PRESS_NUMERIC_CACHE)
    for i in range(directional_count):
        print(f'Count of alternatives after {i + 1} robot(s): {len(result)}')
        result = calc_steps(result, PRESS_DIRECTIONAL_CACHE)
    return result[0]


def main_1() -> None:
    result = 0
    for code in load_codes():
        steps = solve(code, 2)
        print(len(steps), ''.join(steps))
        result += len(steps) * int(code[:-1])
    print(result)


def main_2() -> None:
    result = 0
    for code in load_codes():
        steps = solve(code, 3)
        print(len(steps), ''.join(steps))
        result += len(steps) * int(code[:-1])
    print(result)


if __name__ == "__main__":
    main_1()
    main_2()

# TODO find out why this difference exists:
# Better choice: '<AAA>Av<<AA>>^A<vAA>AA^A<vA>^A'
# Worse choice:  '<AAA>Av<<AA>>^AvAA<AA^>Av<A^>A'
# Possibly solved by the calc_required_moves function

# TODO maybe cache: {(current_pos, to_press): [[str]]}
# issue: to_press can be very long
