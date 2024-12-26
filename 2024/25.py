FIVE_TUPLE = (int, int, int, int, int)


def load_locks_keys() -> ([FIVE_TUPLE], [FIVE_TUPLE]):
    locks, keys = [], []

    def load_five_tuple(file) -> FIVE_TUPLE:
        result = [0, 0, 0, 0, 0]
        for y, row in enumerate([file.readline().strip() for _ in range(5)]):
            for x, cell in enumerate(row):
                if cell == '#':
                    result[x] += 1
        file.readline()
        file.readline()
        return tuple(result)

    with open('25.txt') as f:
        for line in f:
            if line.strip() == '#####':
                locks.append(load_five_tuple(f))
            else:
                keys.append(load_five_tuple(f))
        return locks, keys


def main_1() -> None:
    locks, keys = load_locks_keys()
    print('Locks:', locks)
    print('Keys:', keys)

    overlaps = 0
    for lock in locks:
        for key in keys:
            for i in range(5):
                if key[i] + lock[i] > 5:
                    overlaps += 1
                    break
    print(len(locks) * len(keys) - overlaps)


if __name__ == '__main__':
    main_1()
