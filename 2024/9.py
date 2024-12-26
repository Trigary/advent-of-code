def task_1():
    memory = []

    with open('9.txt') as f:
        line = f.readline().strip()
        next_id = 0
        for line_i in range(len(line)):
            n = int(line[line_i])
            if line_i % 2 == 0:  # Read used memory
                for i in range(n):
                    memory.append(next_id)
                next_id += 1
            else:  # Read free memory
                for i in range(n):
                    memory.append(-1)

    # print(''.join([str(x) if x != -1 else '.' for x in memory]))

    free_i = 0
    filled_i = len(memory) - 1
    while True:
        while free_i < len(memory) and memory[free_i] != -1:
            free_i += 1
        while 0 < filled_i and memory[filled_i] == -1:
            filled_i -= 1
        if free_i >= len(memory) or filled_i <= 0 or free_i >= filled_i:
            break
        memory[free_i] = memory[filled_i]
        memory[filled_i] = -1

    checksum = 0
    for i in range(len(memory)):
        if memory[i] != -1:
            checksum += memory[i] * i

    # print(''.join([str(x) if x != -1 else '.' for x in memory]))
    print(checksum)


def task_2():
    memory = []  # (id, length)

    with open('9.txt') as f:
        line = f.readline().strip()
        next_id = 0
        for line_i in range(len(line)):
            n = int(line[line_i])
            if line_i % 2 == 0:  # Read used memory
                memory.append((next_id, n))
                next_id += 1
            else:  # Read free memory
                memory.append((-1, n))

    # print(''.join([str(x[0]) * x[1] if x[0] != -1 else '.' * x[1] for x in memory]))

    filled_i = len(memory)
    while filled_i > 0:
        filled_i -= 1
        if memory[filled_i][0] == -1:
            continue

        mem_id, mem_len = memory[filled_i]

        for free_i in range(filled_i):
            if memory[free_i][0] != -1 or memory[free_i][1] < mem_len:
                continue

            free_len = memory[free_i][1]
            memory[filled_i] = (-1, mem_len)
            memory[free_i] = (mem_id, mem_len)
            memory.insert(free_i + 1, (-1, free_len - mem_len))
            filled_i += 1
            break

    expanded_memory = [[x[0]] * x[1] for x in memory]
    expanded_memory = sum(expanded_memory, [])
    checksum = 0
    for i in range(len(expanded_memory)):
        if expanded_memory[i] != -1:
            checksum += expanded_memory[i] * i

    # print(''.join([str(x[0]) * x[1] if x[0] != -1 else '.' * x[1] for x in memory]))
    print(checksum)


if __name__ == '__main__':
    task_1()
    task_2()
