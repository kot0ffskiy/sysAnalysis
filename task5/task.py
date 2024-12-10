import json

def convert_rank_to_matrix(rank):
    participants = 0
    for group in rank:
        if isinstance(group, list):
            participants = max(participants, max(group))
        else:
            participants = max(participants, group)

    matrix = [[0 for _ in range(participants)] for _ in range(participants)]

    for i, group in enumerate(rank):
        items = group if isinstance(group, list) else [group]
        
        # Устанавливаем равенство внутри группы
        for item in items:
            for other_item in items:
                matrix[item - 1][other_item - 1] = 1

        # Указываем, что текущая группа лучше всех последующих групп
        for item in items:
            for next_group in rank[i + 1:]:
                next_items = next_group if isinstance(next_group, list) else [next_group]
                for next_item in next_items:
                    matrix[item - 1][next_item - 1] = 1

    return matrix

def find_conflicts(matrix_a, matrix_b):
    conflicts = []

    for i in range(len(matrix_a)):
        for j in range(i):
            if matrix_a[i][j] * matrix_b[i][j] == 0 and matrix_a[j][i] * matrix_b[j][i] == 0:
                conflicts.append([i + 1, j + 1])
    
    return conflicts

def main(rank_a_json, rank_b_json):
    rank_a = json.loads(rank_a_json)
    rank_b = json.loads(rank_b_json)

    matrix_a = convert_rank_to_matrix(rank_a)
    matrix_b = convert_rank_to_matrix(rank_b)
    
    conflicts = find_conflicts(matrix_a, matrix_b)

    return json.dumps(conflicts)

if __name__ == "__main__":
    rank_a = json.dumps([1, [2, 3], 4, [5, 6, 7], 8, 9, 10])
    rank_b = json.dumps([[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]])
    
    result = main(rank_a, rank_b)
    print("Ядро противоречий:", result)
