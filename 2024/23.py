computer_to_connected: {str: {str}} = dict()

with open('23.txt') as f:
    for line in f:
        comp_a, comp_b = line.strip().split('-')
        group_a, group_b = computer_to_connected.get(comp_a, set()), computer_to_connected.get(comp_b, set())
        group_a.add(comp_b)
        group_b.add(comp_a)
        computer_to_connected[comp_a] = group_a
        computer_to_connected[comp_b] = group_b
    print('Loading done')

triples = []
for comp, group in computer_to_connected.items():
    for other_a in group:
        if other_a <= comp:
            continue
        # comp < other_a
        for other_b in group:
            if other_b <= other_a:
                continue
            # comp < other_a < other_b
            if other_b in computer_to_connected[other_a]:
                triples.append((comp, other_a, other_b))
print('Triple generation done', len(triples))

print(triples)

result_1 = 0
for (a, b, c) in triples:
    if a[0] == 't' or b[0] == 't' or c[0] == 't':
        result_1 += 1
print(result_1)

result_2 = []


def search_connected(sol: [str], choices: {str}, filters: [{str}]) -> None:
    global result_2
    for choice in choices:
        if choice <= sol[-1]:
            continue
        if all(choice in a_filter for a_filter in filters):
            new_sol = sol + [choice]
            if len(result_2) < len(new_sol):
                result_2 = new_sol
            filters.append(computer_to_connected[choice])
            search_connected(new_sol, choices, filters)
            filters.pop()


for comp, connected in computer_to_connected.items():
    search_connected([comp], connected, [])

print("Result 2:", len(result_2))
print(','.join(result_2))
