import csv
import argparse

def get_cell_value(file_path, row_number, column_number):
    with open(file_path, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)
        if row_number < len(rows) and column_number < len(rows[row_number]):
            return rows[row_number][column_number]
        else:
            raise IndexError("Индекс строки или колонки выходит за пределы таблицы.")
def main():
    parser = argparse.ArgumentParser(description="Получение значения ячейки из CSV-файла.")
    parser.add_argument("file_path", type=str, help="Полный путь к csv-файлу.")
    parser.add_argument("row_number", type=int, help="Номер строки (начиная с 0).")
    parser.add_argument("column_number", type=int, help="Номер колонки (начиная с 0).")
    
    args = parser.parse_args()
    print(get_cell_value(args.file_path, args.row_number, args.column_number))

if __name__ == "__main__":
    main()
