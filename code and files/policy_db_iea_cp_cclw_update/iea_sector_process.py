import json
import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_data():
    data = pd.read_excel("iea_dedup_result.xlsx")
    return data


def get_dict():
    with open("iea_sector_dict.json", "r") as f:
        map_dict = json.load(f)
    return map_dict


def save(result):
    with pd.ExcelWriter('iea_sector_result.xlsx') as writer:
        result.to_excel(writer, index=False)


if __name__ == '__main__':
    df = get_data()
    iea_sector_dict = get_dict()

    df["Sectors temp"] = df["Sectors"]
    df["Sectors temp"].fillna("", inplace=True)

    # Sectors split by ";"
    df["Sectors temp"] = df["Sectors temp"].apply(lambda x: x.strip().split(";") if x else x)

    sector = []
    subsector = []

    for num, row in df.iterrows():
        if not row["Sectors temp"]:
            sector.append("")
            subsector.append("")
        else:
            sector_inner = []
            subsector_inner = []
            for i in row["Sectors temp"]:
                if i:
                    try:
                        if iea_sector_dict[i.strip()][0]:
                            sector_inner.append(iea_sector_dict[i.strip()][0])
                            if iea_sector_dict[i.strip()][1]:
                                subsector_inner.append(iea_sector_dict[i.strip()][1])
                    except KeyError as e:
                        print(e)
                        print(row["Sectors temp"])

            if len(set(sector_inner)) > 1:
                sector_inner_set = set(sector_inner)
                sector_inner_set.add("Multi-sector")
                sector_inner_temp = set(";".join(set(sector_inner_set)).split(';'))
            else:
                sector_inner_temp = set(";".join(set(sector_inner)).split(';'))

            sector_inner_temp.discard("")
            sector.append(";".join(sector_inner_temp))

            subsector_inner_temp = set(";".join(set(subsector_inner)).split(';'))
            subsector_inner_temp.discard("")
            subsector.append(";".join(subsector_inner_temp))

    # print(len(sector))
    # print(len(subsector))
    df.drop(['Sectors temp'], axis=1, inplace=True)
    df["sector"] = sector
    df["subsector"] = subsector
    save(df)
