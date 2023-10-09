import json
import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_policy_data():
    data = pd.read_excel("policy_db_complete.xlsx", sheet_name="all_policies_dedup")
    return data


def get_instrument_data():
    data = pd.read_excel("Instrument.xlsx")
    return data


if __name__ == '__main__':
    df = get_policy_data()
    # print(df.head())
    # print(df.info())

    df_ist = get_instrument_data()
    # print(df_ist.head())
    # print(df_ist.info())
    tmplist = [x for x in df_ist["Energy (See 7.12)"].tolist() if pd.isnull(x) is False and x != 'nan']

    energy = ";".join(tmplist).replace(" (e.g., EU ETS)", '').split(";")

    tmplist = [x for x in df_ist["Transport (See 8.10)"].tolist() if pd.isnull(x) is False and x != 'nan']

    transport = ";".join(tmplist).split(";")

    tmplist = [x for x in df_ist["Buildings (See 9.10)"].tolist() if pd.isnull(x) is False and x != 'nan']

    buildings = ";".join(tmplist).replace(" (either sectoral or economy wide)", '').split(";")

    tmplist = [x for x in df_ist["industy (See 10.11)"].tolist() if pd.isnull(x) is False and x != 'nan']

    industry = ";".join(tmplist).replace(" (e. g., for energy audits)", '').replace(" (e. g., for fuel switching)",
                                                                                    '').replace(" (also voluntary)",
                                                                                                '').split(";")
    tmplist = [x for x in df_ist["AFOLU (See 11.10)"].tolist() if pd.isnull(x) is False and x != 'nan']

    afolu = ";".join(tmplist).replace("Protection of national, state, and local forests.",
                                      "Protection of national, state, and local forests").replace(
        "Credit lines for low carbon agriculture, sustainable forestry.",
        "Credit lines for low carbon agriculture, sustainable forestry").split(";")

    # check subsector and sector
    sec_subsec_set = set()

    df_sub = df.dropna(subset=["subsector"])
    for index, row in df_sub.iterrows():
        for i in str(row["subsector"]).split(";"):
            try:
                if i.split(":")[0] not in row["sector"]:
                    # print(row["A"])
                    sec_subsec_set.add(row["A"])
            except:
                # print("??")
                # print(row["A"])
                sec_subsec_set.add(row["A"])
    # print(sec_subsec_set)
    print("sec_subsec_set")
    print(len(sec_subsec_set))
    s = list(sec_subsec_set)
    s.sort()
    print(s)

    # check Sector-Instrument and Instrument
    ist_set = set()

    df_sub = df.dropna(subset=["Sector-Instrument"])
    for index, row in df_sub.iterrows():
        for i in str(row["Sector-Instrument"]).split(";"):
            try:
                if i.split(":")[0] not in row["Instrument"]:
                    # print(row["A"])
                    ist_set.add(row["A"])
            except:
                # print("??")
                # print(row["A"])
                ist_set.add(row["A"])
    # print(ist_set)
    print("ist_set")
    print(len(ist_set))

    s = list(ist_set)
    s.sort()
    print(s)

    inter_ist_set = ist_set.intersection(sec_subsec_set)
    print(inter_ist_set)

    # check Sector-Instrument and sector

    ist_sec_set = set()
    ist_sec_set1 = set()

    df_sub = df.dropna(subset=["Sector-Instrument"])
    for index, row in df_sub.iterrows():
        instru = []
        sector = row["sector"]
        try:
            for s in sector.split(';'):
                if s == "Multi-sector":
                    pass
                elif s == "Energy systems":
                    instru += energy
                elif s == "Transport":
                    instru += transport
                elif s == "Buildings":
                    instru += buildings
                elif s == "Industry":
                    instru += industry
                elif s == "AFOLU":
                    instru += afolu
        except:
            # print("??")
            # print(row["A"])
            ist_sec_set1.add(row["A"])

        for i in str(row["Sector-Instrument"]).split(";"):
            try:
                if i.split(":")[1] not in instru:
                    # print(i.split(":")[1])
                    # print(row["A"])
                    ist_sec_set.add(row["A"])
            except:
                # print("??")
                # print(row["A"])
                ist_sec_set1.add(row["A"])
    # print(ist_sec_set)
    print("ist_sec_set")
    print(len(ist_sec_set))

    s = list(ist_sec_set)
    s.sort()
    print(s)

    print("union")
    s = list(sec_subsec_set.union(ist_set, ist_sec_set))
    print(len(s))
    s.sort()
    print(s)
