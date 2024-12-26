with open('2.txt') as f:
    reports = [[int(x) for x in line.split(' ')] for line in f]

safe = 0


def is_safe(list):
    for i, y in enumerate(list):
        if i == 0:
            continue
        x = list[i - 1]

        if x - y < 1 or x - y > 3:
            break
    else:
        return True

    for i, y in enumerate(list):
        if i == 0:
            continue
        x = list[i - 1]

        if y - x < 1 or y - x > 3:
            break
    else:
        return True

    return False


for report in reports:
    if is_safe(report):
        safe += 1

print(safe)


def sublists(list):
    return [
        [x for i, x in enumerate(list) if i != exclude_i]
        for exclude_i in range(0, len(list))
    ]


safe = 0

for report in reports:
    for sublist in sublists(report):
        if is_safe(sublist):
            safe += 1
            break

print(safe)
