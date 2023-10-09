import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_cp_data():
    df = pd.read_excel("cp_sector_region_instrument_result.xlsx")
    return df


def get_iea_data():
    df = pd.read_excel("iea_sector_region_instrument_result.xlsx")
    return df


def get_lse_data():
    df = pd.read_excel("lse_sector_region_instrument_result.xlsx")
    return df


def get_country_data():
    df = pd.read_excel("Countries_Code.xlsx")
    return df


def get_annex_data():
    df = pd.read_excel("Annex.xlsx")
    return df


def save(df, file_name):
    with pd.ExcelWriter('{}_sector_region_instrument_annex_result.xlsx'.format(file_name)) as writer:
        df.to_excel(writer, index=False)


def iea_annex_process():
    # IEA
    iea_df = get_iea_data()
    iea_df.fillna("", inplace=True)
    iea_annex = []
    for num, row in iea_df.iterrows():
        if row["ISO_code"] in annex_1_iso_list:
            iea_annex.append("Annex I")
        else:
            iea_annex.append("Non Annex I")
    iea_df["Annex"] = iea_annex
    save(iea_df, "iea")


def cp_annex_process():
    # Climate Policy
    cp_df = get_cp_data()
    cp_df.fillna("", inplace=True)
    cp_annex = []
    for num, row in cp_df.iterrows():
        if row["ISO_code"] in annex_1_iso_list:
            cp_annex.append("Annex I")
        else:
            cp_annex.append("Non Annex I")
    cp_df["Annex"] = cp_annex
    save(cp_df, "cp")


def lse_annex_process():
    # LSE
    lse_df = get_lse_data()
    lse_df.fillna("", inplace=True)
    lse_annex = []
    for num, row in lse_df.iterrows():
        if row["ISO_code"] in annex_1_iso_list:
            lse_annex.append("Annex I")
        else:
            lse_annex.append("Non Annex I")
    lse_df["Annex"] = lse_annex
    save(lse_df, "lse")


if __name__ == '__main__':
    country_df = get_country_data()
    annex_df = get_annex_data()
    # print(annex_df["Annex I"])

    annex_df["Annex I"] = annex_df["Annex I"].apply(lambda x: x.strip())
    annex_country = annex_df["Annex I"].to_list()

    country_s_name = country_df["Short Name"].tolist()
    country_l_name = country_df["Long Name"].tolist()
    country_code = country_df["Code"].tolist()

    country_sname_dict = {
        country_s_name[i].lower(): [country_s_name[i], country_code[i]]
        for i in range(len(country_s_name))}
    country_lname_dict = {
        country_l_name[i].lower(): [country_l_name[i], country_code[i]]
        for i in range(len(country_l_name))}

    annex_data = []
    for country in annex_country:
        country = country.lower()
        if country == "european union":
            annex_data.append("EUU")
        elif country in country_lname_dict:
            annex_data.append(country_lname_dict[country][1])
        elif country in country_sname_dict:
            annex_data.append(country_sname_dict[country][1])
        else:
            annex_data.append("")
    annex_df["ISO"] = annex_data
    annex_df.to_excel("Annex.xlsx", index=False)

    annex_1_iso_list = annex_df["ISO"].to_list()

    iea_annex_process()
    cp_annex_process()
    lse_annex_process()
