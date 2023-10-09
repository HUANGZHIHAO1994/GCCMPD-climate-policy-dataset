import json
import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_data():
    data = pd.read_excel("cp_sector_region_instrument_annex_result.xlsx")
    return data


def get_dict():
    with open("cp_objective_dict.json", "r") as f:
        json_dict = json.load(f)
    return json_dict


def save(result):
    with pd.ExcelWriter("cp_sector_region_instrument_annex_objective_result.xlsx") as writer:
        result.to_excel(writer, index=False)


if __name__ == '__main__':
    df = get_data()
    map_dict = get_dict()

    df["Policy objective temp"] = df["Policy objective"]
    df["Policy objective temp"].fillna("", inplace=True)

    df["Policy objective temp"] = df["Policy objective temp"].apply(
        lambda x: x.replace(', ', ',').replace(';', ',').strip().split(',') if len(x) > 0 else x)
    # print(df.info())

    objective = []
    subobjective = []

    for num, row in df.iterrows():
        if not row["Policy objective temp"]:
            objective.append("")
            subobjective.append("")
        else:
            objective_inner = []
            subobjective_inner = []
            for i in row["Policy objective temp"]:
                if i:

                    if map_dict[i.strip()][0]:
                        objective_inner.append(map_dict[i.strip()][0])
                        if map_dict[i.strip()][1]:
                            subobjective_inner.append(map_dict[i.strip()][1])
                else:
                    print(row["Policy objective temp"])

            objective_inner_temp = set(";".join(set(objective_inner)).split(';'))
            objective_inner_temp.discard("")
            subobjective_inner_temp = set(";".join(set(subobjective_inner)).split(';'))
            subobjective_inner_temp.discard("")
            objective.append(";".join(objective_inner_temp))
            subobjective.append(";".join(subobjective_inner_temp))

    # print(len(objective))
    # print(len(subobjective))
    df["objective"] = objective
    df["subobjective"] = subobjective
    df.drop(['Policy objective temp'], axis=1, inplace=True)
    save(df)
