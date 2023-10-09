import json
import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_data():
    data = pd.read_csv("lse.csv")
    return data


def get_dict():
    with open("lse_sector_dict.json", "r") as f:
        map_dict = json.load(f)
    return map_dict


def save(result):
    with pd.ExcelWriter('lse_sector_result.xlsx') as writer:
        result.to_excel(writer, index=False)


if __name__ == '__main__':
    df = get_data()
    lse_sector_dict = get_dict()

    df["Sectors"].fillna("", inplace=True)

    # Sectors split by ","
    df["Sectors"] = df["Sectors"].apply(lambda x: x.strip().split(",") if len(x) > 0 else x)

    sector = []
    subsector = []

    for num, row in df.iterrows():
        if not row["Sectors"]:
            sector.append("")
            subsector.append("")
        else:
            sector_inner = []
            subsector_inner = []
            for i in row["Sectors"]:
                if lse_sector_dict[i.strip()][0]:
                    sector_inner.append(lse_sector_dict[i.strip()][0])
                    if lse_sector_dict[i.strip()][1]:
                        subsector_inner.append(lse_sector_dict[i.strip()][1])

            if len(set(sector_inner)) > 1:
                sector_inner_set = set(sector_inner)
                sector_inner_set.add("Multi-sector")
                sector.append(";".join(sector_inner_set))
            else:
                sector.append(";".join(set(sector_inner)))
            subsector.append(";".join(set(subsector_inner)))

    # print(len(sector))
    # print(len(subsector))
    df["Sectors"] = df["Sectors"].apply(lambda x: ",".join(x) if len(x) > 0 else "")
    df["sector"] = sector
    df["subsector"] = subsector
    save(df)
