import pandas as pd
import numpy as np

# ECOLEX_Legislation = ["ECOLEX_Legislation_EN.xlsx"]
# for i in range(0, 40):
#     ECOLEX_Legislation.append("ECOLEX_Legislation_{}_EN.xlsx".format(i))

# for index, inputfile in enumerate(ECOLEX_Legislation):
#     print(index)
#     df = pd.read_excel(inputfile)
#     df.loc[:, ['Source']] = 'ECOLEX_Legislation'
#     with pd.ExcelWriter(inputfile, engine='xlsxwriter',
#                         engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
#         df.to_excel(writer, index=False)

# ECOLEX_Legislation = ["ECOLEX_Legislation.csv"]
# for i in range(0, 40):
#     ECOLEX_Legislation.append("ECOLEX_Legislation_{}.csv".format(i))
# 
# for index, inputfile in enumerate(ECOLEX_Legislation):
#     print(index)
#     df = pd.read_csv(inputfile)
#     df.loc[:, ['Source']] = 'ECOLEX_Legislation'
#     df.to_csv(inputfile, index=False)


df = pd.read_csv("ECOLEX_Treaty.csv")
df.loc[:, ['Source']] = 'ECOLEX_Treaty'
df.to_csv("ECOLEX_Treaty.csv", index=False)

ECOLEX_Treaty = ["ECOLEX_Treaty_EN.xlsx", "ECOLEX_Treaty_EN_ISO_REGION_INCOME.xlsx"]

for index, inputfile in enumerate(ECOLEX_Treaty):
    print(index)
    df = pd.read_excel(inputfile)
    df.loc[:, ['Source']] = 'ECOLEX_Treaty'
    with pd.ExcelWriter(inputfile, engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        df.to_excel(writer, index=False)
