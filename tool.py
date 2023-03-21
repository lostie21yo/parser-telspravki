import pandas as pd
import os

file_dir = os.path.split(__file__)[0]
df = pd.read_csv(f"{file_dir}/Stavropol.csv", delimiter='\t', encoding='utf-16') # old
for row in df.values:
    row[2] = " " + row[2]

df.to_csv(f'{file_dir}/Stavropol_t.csv', sep='\t', index= False, encoding="utf-16")
