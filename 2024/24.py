import graphviz


def load_initial_values() -> {str: int}:
    with open('24.txt') as f:
        result = dict()
        while (line := f.readline().strip()) != '':
            name, value = line.split(': ')
            result[name] = int(value)
        return result


def op_and(a: int, b: int) -> int:
    return a & b


def op_or(a: int, b: int) -> int:
    return a | b


def op_xor(a: int, b: int) -> int:
    return a ^ b


def load_dependency_graph() -> {str: (str, str, str)}:
    op_to_func = {
        'AND': op_and,
        'OR': op_or,
        'XOR': op_xor
    }
    with open('24.txt') as f:
        result = dict()
        while (_ := f.readline().strip()) != '':
            pass
        for line in f:
            a, op, b, _, output = line.split()
            result[output] = (a, op_to_func[op], b)
        return result


def topological_sort(dependency_graph: {str: (str, str, str)}) -> [str]:
    result = []
    visited = set()

    def dfs(node: str):
        if node in visited:
            return
        visited.add(node)
        if node in dependency_graph:
            a, _, b = dependency_graph[node]
            dfs(a)
            dfs(b)
        result.append(node)

    for n in dependency_graph.keys():
        dfs(n)
    return result


def has_loop(dependency_graph) -> bool:
    permanent_mark = set()
    temporary_mark = set()
    result = False

    def visit(node: str):
        if node in permanent_mark:
            return
        if node in temporary_mark:
            nonlocal result
            result = True
            return
        temporary_mark.add(node)
        if node in dependency_graph:
            a, _, b = dependency_graph[node]
            visit(a)
            visit(b)
        permanent_mark.add(node)

    for n in dependency_graph.keys():
        visit(n)
        if result:
            return True
    return result


def num_to_var(prefix: str, num: int) -> str:
    return prefix + str(num).rjust(2, '0')


def main_1() -> None:
    values = load_initial_values()
    dependency_graph = load_dependency_graph()
    sorted_nodes = topological_sort(dependency_graph)

    for node in sorted_nodes:
        if node not in values:
            a, op, b = dependency_graph[node]
            values[node] = op(values[a], values[b])

    shift = 0
    result = 0
    while (key := num_to_var('z', shift)) in values:
        result |= values[key] << shift
        shift += 1

    print(result)


def render_dependency_graph(dependency_graph: {str: (str, str, str)}) -> None:
    dot = graphviz.Digraph()
    op_to_color = {
        'op_and': 'red',
        'op_or': 'green',
        'op_xor': 'blue'
    }
    for node, (a, op, b) in dependency_graph.items():
        dot.node(node, node + "\n" + f'{a} {op.__name__} {b}', color=op_to_color[op.__name__])
        dot.edge(node, a)
        dot.edge(node, b)
    dot.render('24.gv', format='png', view=True)


def calc_specific_value(values_input_output: {str: int}, dependency_graph, val: str) -> int:
    result = values_input_output.get(val, None)
    if result is not None:
        return result

    a, op, b = dependency_graph[val]
    a = calc_specific_value(values_input_output, dependency_graph, a)
    b = calc_specific_value(values_input_output, dependency_graph, b)
    result = op(a, b)
    values_input_output[val] = result
    return result


def calc_transitive_dependencies(sorted_nodes: [str], dependency_graph: {str: (str, str, str)}) -> {str: {str}}:
    result = dict()
    for node in sorted_nodes:
        result[node] = set()
        if node in dependency_graph:
            a, _, b = dependency_graph[node]
            result[node].add(a)
            result[node].add(b)
            result[node].update(result[a])
            result[node].update(result[b])
    return result


def is_correctly_calculated(dependency_graph, z_num: int) -> bool:
    values = dict()
    for i in range(z_num + 1):
        values[num_to_var('x', i)] = 0
        values[num_to_var('y', i)] = 0

    try:
        if z_num > 0:
            values_copy = values.copy()
            values_copy[num_to_var('x', z_num - 1)] = 1
            values_copy[num_to_var('y', z_num - 1)] = 1
            if calc_specific_value(values_copy, dependency_graph, num_to_var('z', z_num)) != 1:
                return False

        for x, y in [(0, 0), (0, 1), (1, 0)]:
            values[num_to_var('x', z_num)] = x
            values[num_to_var('y', z_num)] = y
            if calc_specific_value(values.copy(), dependency_graph, num_to_var('z', z_num)) != x | y:
                return False
    except KeyError:
        return False

    return True


def z_to_possibly_incorrectly_calculated(dependency_graph) -> {str: {str}}:
    result = dict()
    correct = set()
    num = 0
    while (key := num_to_var('z', num)) in dependency_graph:
        possibly_incorrect = {key}
        to_check = [dependency_graph[key][0], dependency_graph[key][2]]
        while to_check:
            node = to_check.pop()
            if node[0] == 'x' or node[0] == 'y':
                continue
            if node not in correct:
                correct.add(node)
                possibly_incorrect.add(node)
                to_check.append(dependency_graph[node][0])
                to_check.append(dependency_graph[node][2])
        result[key] = possibly_incorrect
        num += 1
    return result


def try_solve(dependency_graph, max_swaps: int = 4) -> [(str, str)]:
    sorted_nodes = topological_sort(dependency_graph)
    transitive_dependencies = calc_transitive_dependencies(sorted_nodes, dependency_graph)
    z_to_possibly_wrong = z_to_possibly_incorrectly_calculated(dependency_graph)

    num_bits = 0
    while num_to_var('z', num_bits) in dependency_graph:
        num_bits += 1

    correct = set()
    for z in range(num_bits - 1):
        if is_correctly_calculated(dependency_graph, z):
            correct |= z_to_possibly_wrong[num_to_var('z', z)]
            continue

        if max_swaps == 0:
            return None

        for new_dep in z_to_possibly_wrong[num_to_var('z', z)]:
            for other in dependency_graph.keys():
                if other in correct:
                    continue

                other_trans = transitive_dependencies[other]
                if any(num_to_var(v, i) in other_trans for i in range(z + 1, 46) for v in ['x', 'y']):
                    continue

                new_dep_graph = dependency_graph.copy()
                new_dep_triple, other_triple = new_dep_graph[new_dep], new_dep_graph[other]
                new_dep_graph[new_dep] = other_triple
                new_dep_graph[other] = new_dep_triple

                if has_loop(new_dep_graph):
                    continue

                if not all(is_correctly_calculated(new_dep_graph, zz) for zz in range(z + 1)):
                    continue

                rest_solution = try_solve(new_dep_graph, max_swaps - 1)
                if rest_solution is not None:
                    return [(new_dep, other)] + rest_solution
        return None
    return []


def main_2() -> None:
    dependency_graph = load_dependency_graph()
    render_dependency_graph(dependency_graph)

    swaps = try_solve(dependency_graph)
    print('Required swaps', swaps)
    swaps = sorted([y for x in swaps for y in x])
    print(','.join(swaps))


if __name__ == '__main__':
    main_1()
    main_2()
