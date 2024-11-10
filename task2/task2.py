import sys
from itertools import chain

def parse_file(file_path):
    with open(file_path, 'r') as f:
        edges = [tuple(map(int, line.split(','))) for line in f.read().strip().splitlines()]
    nodes = set(chain.from_iterable(edges))
    graph = {parent: [] for parent, _ in edges}
    for parent, child in edges:
        graph[parent].append(child)
    return graph, max(nodes)

def compute_relationships(graph, node_count):
    relations = [[0]*5 for _ in range(node_count)]
    for node, children in graph.items():
        relations[node-1][0] = len(children)
        for child in children:
            relations[child-1][1] += 1
            relations[node-1][2] += relations[child-1][0]
            if child in graph:
                for grandchild in graph[child]:
                    relations[grandchild-1][3] += 1
    
    root = (set(graph.keys()) - set(chain.from_iterable(graph.values()))).pop()
    levels = {}
    queue = [(root, 0)]
    while queue:
        node, level = queue.pop(0)
        levels.setdefault(level, []).append(node)
        queue.extend((child, level + 1) for child in graph.get(node, []))
    
    for level_nodes in levels.values():
        for node in level_nodes:
            relations[node-1][4] = len(level_nodes) - 1
    return relations

def main(file_path):
    graph, node_count = parse_file(file_path)
    relation_matrix = compute_relationships(graph, node_count)
    return '\n'.join(','.join(map(str, row)) for row in relation_matrix)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(main(sys.argv[1]))
    else:
        print("Необходимо указать путь к файлу")
