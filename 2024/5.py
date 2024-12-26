def dict_of_set_add(d, k, e) -> None:
    s = d.get(k, None)
    if s is None:
        d[k] = {e}
    else:
        s.add(e)


key_before_elem: {int: {int}} = {}
updates: [int] = []

with open('5.txt') as f:
    for line in f:
        line = line.strip()
        if line == '':
            break
        before, after = line.split('|')
        before, after = int(before), int(after)
        dict_of_set_add(key_before_elem, before, after)
    for line in f:
        updates.append([int(x) for x in line.split(',')])

result_1 = 0
input_2 = []

for update in updates:
    prev = set()
    success = True
    for x in update:
        for p in prev:
            if p in key_before_elem.get(x, {}):
                success = False
                break
        if not success:
            break
        prev.add(x)
    if success:
        result_1 += update[len(update) // 2]
    else:
        input_2.append(update)

print(result_1)

result_2 = 0

for update in input_2:
    update_set = set(update)
    update_key_before_elem = {x: key_before_elem.get(x, set()).intersection(update_set) for x in update}
    visited = set()
    result = []


    def visit(n):
        if n in visited:
            return
        for m in update_key_before_elem[n]:
            visit(m)
        visited.add(n)
        result.append(n)


    for x in update_set:
        visit(x)

    result_2 += result[len(result) // 2]

print(result_2)
