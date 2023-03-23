import pandas as pd
import os
from collections import Counter

city = "Samara"

file_dir = os.path.split(__file__)[0]

df = pd.read_csv(f"{file_dir}/{city}.csv", delimiter='\t', encoding='utf-16') # old

# добавление пробела к номеру
def space_adding(df):
    for row in df.values:
        row[2] = " " + row[2]

# подсчет кол-ва вхождений каждого элемента в список
def duplicate_counting(df, limit):
    array = []
    for i in range(len(df.values)):
        array.append(f'{df.values[i][0]} {df.values[i][1]} {df.values[i][2]}')

    c = Counter(array).most_common(limit)
    for elem in c:
        print(elem)

space_adding(df)

df = df.drop_duplicates()

df.to_csv(f'{file_dir}/{city}_t.csv', sep='\t', index= False, encoding="utf-16")
