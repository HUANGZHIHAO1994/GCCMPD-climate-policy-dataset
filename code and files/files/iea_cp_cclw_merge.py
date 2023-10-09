import pandas as pd
import os

ECOLEX_Legislation = []
for i in range(0, 10):
    ECOLEX_Legislation.append("iea_cp_cclw_{}_EN.xlsx".format(i))

dfs = []
for index, inputfile in enumerate(ECOLEX_Legislation):
    print(index)
    dfs.append(pd.read_excel(inputfile))

df = pd.concat(dfs)
df.to_excel("iea_cp_cclw_EN.xlsx", index=False)
