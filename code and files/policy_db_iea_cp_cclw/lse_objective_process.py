import json
import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_data():
    data = pd.read_excel("lse_sector_region_instrument_annex_result.xlsx")
    return data


def get_dict():
    with open("lse_objective_dict.json", "r") as f:
        json_dict = json.load(f)
    return json_dict


def save(result):
    with pd.ExcelWriter("lse_sector_region_instrument_annex_objective_result.xlsx") as writer:
        result.to_excel(writer, index=False)


if __name__ == '__main__':
    df = get_data()
    map_dict = get_dict()

    df["Keywords temp"] = df["Keywords"]
    df["Keywords temp"].fillna("", inplace=True)
    df["Keywords temp"] = df["Keywords temp"].apply(
        lambda x: x.strip().replace(",  ", ',').replace(", ", ',').split(',') if len(x) > 0 else x)

    df["Sectors"].fillna("", inplace=True)
    df["Sectors"] = df["Sectors"].apply(lambda x: x.strip().split(",") if len(x) > 0 else x)

    objective = []
    subobjective = []

    for num, row in df.iterrows():
        if not row["Keywords temp"]:
            objective_inner = []
            subobjective_inner = []
            if 'Health' in row["Sectors"]:
                objective_inner.append('Social')
                subobjective_inner.append('Social:Health impact')
            if 'Social development' in row["Sectors"]:
                objective_inner.append('Social')
            if 'Environment' in row["Sectors"]:
                objective_inner.append('Environmental')

            if objective_inner:
                objective_inner_temp = set(";".join(set(objective_inner)).split(';'))
                objective_inner_temp.discard("")
                objective.append(";".join(objective_inner_temp))
            else:
                objective.append("")

            if subobjective_inner:
                subobjective_inner_temp = set(";".join(set(subobjective_inner)).split(';'))
                subobjective_inner_temp.discard("")
                subobjective.append(";".join(subobjective_inner_temp))
            else:
                subobjective.append("")

        else:
            objective_inner = []
            subobjective_inner = []
            if 'Health' in row["Sectors"]:
                objective_inner.append('Social')
                subobjective_inner.append('Social:Health impact')
            if 'Social development' in row["Sectors"]:
                objective_inner.append('Social')
            if 'Environment' in row["Sectors"]:
                objective_inner.append('Environmental')

            for i in row["Keywords temp"]:

                if map_dict[i.strip()][0]:
                    objective_inner.append(map_dict[i.strip()][0])
                    if map_dict[i.strip()][1]:
                        subobjective_inner.append(map_dict[i.strip()][1])

            objective_inner_temp = set(";".join(set(objective_inner)).split(';'))
            objective_inner_temp.discard("")
            subobjective_inner_temp = set(";".join(set(subobjective_inner)).split(';'))
            subobjective_inner_temp.discard("")
            objective.append(";".join(objective_inner_temp))
            subobjective.append(";".join(subobjective_inner_temp))

            # objective.append(";".join(set(objective_inner)))
            # subobjective.append(";".join(set(subobjective_inner)))

    df["objective"] = objective
    df["subobjective"] = subobjective
    df.drop(['Keywords temp'], axis=1, inplace=True)
    save(df)
