import json
import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_data():
    data = pd.read_excel("iea_sector_region_instrument_annex_result.xlsx")
    return data


def get_dict():
    with open("iea_objective_dict.json", "r") as f:
        json_dict = json.load(f)
    return json_dict


def save(result):
    with pd.ExcelWriter("iea_sector_region_instrument_annex_objective_result.xlsx") as writer:
        result.to_excel(writer, index=False)


if __name__ == '__main__':
    df = get_data()
    map_dict = get_dict()

    df["Topics"].fillna("", inplace=True)
    df["Topics"] = df["Topics"].apply(lambda x: x.strip().split(";") if x else x)
    # print(df["Topics"])
    # print(df.info())

    objective = []
    subobjective = []

    for num, row in df.iterrows():
        if not row["Topics"]:
            objective.append("")
            subobjective.append("")
        else:
            objective_inner = []
            subobjective_inner = []
            for i in row["Topics"]:
                if i:
                    try:
                        if map_dict[i.strip()][0]:
                            objective_inner.append(map_dict[i.strip()][0])
                            if map_dict[i.strip()][1]:
                                subobjective_inner.append(map_dict[i.strip()][1])
                    except KeyError as e:
                        print(e)

            objective_inner_temp = set(";".join(set(objective_inner)).split(';'))
            objective_inner_temp.discard("")
            subobjective_inner_temp = set(";".join(set(subobjective_inner)).split(';'))
            subobjective_inner_temp.discard("")
            objective.append(";".join(objective_inner_temp))
            subobjective.append(";".join(subobjective_inner_temp))

            # objective.append(";".join(set(objective_inner)))
            # subobjective.append(";".join(set(subobjective_inner)))

    df["Topics"] = df["Topics"].apply(lambda x: ";".join(x) if len(x) > 0 else "")
    df["objective"] = objective
    df["subobjective"] = subobjective
    save(df)
