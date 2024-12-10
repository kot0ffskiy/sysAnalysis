import numpy as np
import pandas as pd
from io import StringIO

def entropy(probabilities):
    probabilities = probabilities[probabilities > 0]  # Исключаем нули
    return -np.sum(probabilities * np.log2(probabilities))

def main() -> list:
    csv_data = """Возрастная группа,Электроника,Одежда,Книги,Обувь
                18-24,20,15,10,5
                25-34,30,20,15,10
                35-44,25,25,20,15
                45-54,20,20,25,20
                55+,15,15,30,25"""
    data = pd.read_csv(StringIO(csv_data), index_col=0)

    prob = data / data.values.sum()

    margin_prob_A = prob.sum(axis=1)
    margin_prob_B = prob.sum(axis=0)

    H_AB = entropy(prob.values.flatten())
    H_A = entropy(margin_prob_A)
    H_B = entropy(margin_prob_B)

    Ha_B = sum(
        p_a * entropy(prob.loc[idx] / p_a)
        for idx, p_a in zip(prob.index, margin_prob_A) if p_a > 0
    )

    I_AB = H_B - Ha_B

    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(Ha_B, 2), round(I_AB, 2)]


result = main()
print(result)
