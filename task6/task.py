import json

def calculate_membership(value: float, points: list) -> float:
    """
    Вычисляет степень принадлежности для заданного значения на основе линейно-кусочной функции.
    """
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= value <= x2:
            return y1 + (y2 - y1) * (value - x1) / (x2 - x1)
    return 0.0

def fuzzify(value: float, membership_functions: list) -> dict:
    """
    Фаззификация: вычисление степеней принадлежности.
    """
    fuzzy_values = {}
    for term in membership_functions:
        term_id = term['id']
        points = term['points']
        fuzzy_values[term_id] = calculate_membership(value, points)
    return fuzzy_values

def apply_rules(fuzzy_temperature: dict, rules: list, heating_membership_functions: dict) -> dict:
    """
    Применение правил логического вывода.
    """
    fuzzy_heating = {}
    for rule in rules:
        temperature_term, heating_term = rule
        activation = fuzzy_temperature.get(temperature_term, 0.0)
        if heating_term not in fuzzy_heating:
            fuzzy_heating[heating_term] = []
        for point in heating_membership_functions[heating_term]['points']:
            fuzzy_heating[heating_term].append((point[0], min(activation, point[1])))
    return fuzzy_heating

def defuzzify(fuzzy_heating: dict) -> float:
    """
    Дефаззификация: нахождение четкого значения управления.
    """
    numerator = 0.0
    denominator = 0.0
    for _, points in fuzzy_heating.items():
        for x, y in points:
            numerator += x * y
            denominator += y
    return numerator / denominator if denominator != 0 else 0.0

def main(temperature_json: str, heating_json: str, rules_json: str, current_temperature: float) -> float:
    """
    Основная функция для вычисления оптимального управления.
    """
    temperature_membership_functions = json.loads(temperature_json)['температура']
    heating_membership_functions = {item['id']: item for item in json.loads(heating_json)['уровень нагрева']}
    rules = json.loads(rules_json)

    fuzzy_temperature = fuzzify(current_temperature, temperature_membership_functions)
    print(fuzzy_temperature)

    fuzzy_heating = apply_rules(fuzzy_temperature, rules, heating_membership_functions)
    print(fuzzy_heating)

    optimal_heating = defuzzify(fuzzy_heating)
    print(optimal_heating)

    return round(optimal_heating, 2)

if __name__ == "__main__":
    temperature_json = '''{
        "температура": [
            {
                "id": "холодно",
                "points": [[0,1], [18,1], [22,0], [50,0]]
            },
            {
                "id": "комфортно",
                "points": [[18, 0], [22, 1], [24, 1], [26, 0]]
            },
            {
                "id": "жарко",
                "points": [[0, 0], [24, 0], [26, 1], [50, 1]]
            }
        ]
    }'''
    heating_json = '''{
        "уровень нагрева": [
            {
                "id": "слабый",
                "points": [[0, 1], [4, 1], [6, 0], [10, 0]]
            },
            {
                "id": "умеренный",
                "points": [[4, 0], [6, 1], [8, 1], [10, 0]]
            },
            {
                "id": "интенсивный",
                "points": [[8, 0], [10, 1], [12, 1], [14, 0]]
            }
        ]
    }'''
    rules_json = '''[
        ["холодно", "интенсивный"],
        ["комфортно", "умеренный"],
        ["жарко", "слабый"]
    ]'''
    current_temperature = 20.0

    result = main(temperature_json, heating_json, rules_json, current_temperature)
    print(f"Значение оптимального управления: {result}")
