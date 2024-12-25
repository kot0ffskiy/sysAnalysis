import math

def task(csv_string):
    matrix = [list(map(int, row.split(','))) for row in csv_string.strip().split('\n')]
    n = len(matrix)
    k = len(matrix[0]) if n > 0 else 0

    if n == 0 or k == 0:
        return 0.0

    entropy = 0.0
    for i in range(n):
        for j in range(k):
            lij = matrix[i][j]
            if lij > 0: 
                norm = lij / (n - 1)
                entropy += norm * math.log2(norm)

    entropy = -entropy

    return round(entropy, 1)

def main(input_data):
    if '\n' in input_data or ',' in input_data:
        # Если входные данные содержат недопустимые для имени файла 
        # символы, считаем их строкой
        csv_string = input_data
    else:
        try:
            # Иначе предполагаем, что это путь к файлу
            with open(input_data, 'r') as file:
                csv_string = file.read()
        except FileNotFoundError:
            print("Error: File not found or invalid input provided.")
            return
    
    # Вызываем функцию task и выводим результат
    result = task(csv_string)
    print(f"Calculated entropy: {result}")

if __name__ == "__main__":
    # Передача строки CSV или имени файла
    main('2,0,2,0,0\n0,1,0,0,1\n2,1,0,0,1\n0,1,0,1,1\n0,1,0,1,1\n')
