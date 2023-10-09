import json
import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_data():
    data = pd.read_excel("lse_sector_region_result.xlsx")
    return data


def get_json_data():
    with open("lse_instrument_dict.json", "r") as f:
        json_data = json.load(f)
    return json_data


def save(result):
    with pd.ExcelWriter('lse_sector_region_instrument_result.xlsx') as writer:
        result.to_excel(writer, index=False)


if __name__ == '__main__':
    df = get_data()
    map_dict = get_json_data()
    # print(df.info())

    df["Instruments"].fillna("", inplace=True)
    df["sector"].fillna("", inplace=True)
    df["Instruments_temp"] = df["Instruments"].apply(
        lambda x: x.strip().replace(";  ", ';').replace("; ", ';').split(";") if x else x)
    # print(len({i for j in df["Instruments_temp"].to_list() for i in j}))

    instrument = []
    sector_instrument = []

    for num, row in df.iterrows():
        if not len(row["Instruments_temp"]) > 0:
            instrument.append('')
            sector_instrument.append('')
        else:
            instrument_inner = []
            sector_instrument_inner = []
            for i in row["Instruments_temp"]:
                if map_dict[i.strip()][0] == 'No':
                    instrument_inner.append(map_dict[i.strip()][1])
                    if map_dict[i.strip()][2]:
                        sector_instrument_inner.append(map_dict[i.strip()][2])
                    else:
                        sector_instrument_inner.append("")
                elif map_dict[i.strip()][0] == 'Sector':
                    instrument_inner.append(map_dict[i.strip()][1])
                    if row["sector"]:
                        for sec in row["sector"].split(';'):
                            if map_dict[i.strip()][2][sec]:
                                sector_instrument_inner.append(map_dict[i.strip()][2][sec])

            instrument_inner_temp = set(";".join(set(instrument_inner)).split(';'))
            instrument_inner_temp.discard("")
            sector_instrument_inner_temp = set(";".join(set(sector_instrument_inner)).split(';'))
            sector_instrument_inner_temp.discard("")
            instrument.append(";".join(instrument_inner_temp))
            sector_instrument.append(";".join(sector_instrument_inner_temp))

    df["Instrument"] = instrument
    df["Sector-Instrument"] = sector_instrument
    df.drop(['Instruments_temp'], axis=1, inplace=True)
    # df["Instruments"] = df["Instruments"].apply(lambda x: ";".join(x) if x else x)

    save(df)
