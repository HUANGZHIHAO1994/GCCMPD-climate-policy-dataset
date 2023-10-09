import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_cp_data():
    data = pd.read_excel("cp_sector_result.xlsx")
    return data


def get_iea_data():
    data = pd.read_excel("iea_sector_result.xlsx")
    return data


def get_lse_data():
    data = pd.read_excel("lse_sector_result.xlsx")
    return data


def get_country_data():
    data = pd.read_excel("Countries_Code.xlsx")
    return data


def get_region_data():
    data = pd.read_excel("Region.xlsx")
    return data


def get_aggregates_data():
    data = pd.read_excel("Aggregates_Code.xlsx")
    return data


def iea_region_process():
    # IEA
    iea_df = get_iea_data()
    iea_df.fillna("", inplace=True)
    iea_country = iea_df["Country"].to_list()
    iea_region_data = []
    for i in iea_country:
        if i in region_list:
            iea_region_data.append(region_dict[i])
        else:
            iea_region_data.append("")
    iea_df["IPCC_Region"] = iea_region_data

    # Short_name & Long_name dict
    iea_sname_dict = {
        country_s_name[i].lower():
            [country_s_name[i], country_l_name[i], country_code[i], country_i_group[i], country_region[i]]
        for i in range(len(country_s_name))}
    iea_lname_dict = {
        country_l_name[i].lower():
            [country_s_name[i], country_l_name[i], country_code[i], country_i_group[i], country_region[i]]
        for i in range(len(country_l_name))}
    iea_agg_sname_dict = {
        aggregates_s_name[i].lower():
            [aggregates_s_name[i], aggregates_l_name[i], aggregates_code[i], '', '']
        for i in range(len(aggregates_s_name))}
    iea_agg_lname_dict = {
        aggregates_l_name[i].lower():
            [aggregates_s_name[i], aggregates_l_name[i], aggregates_code[i], '', '']
        for i in range(len(aggregates_l_name))}
    # print(iea_sname_dict)

    iea_data = []
    for country in iea_country:
        if country == "Kyrgyzstan":
            country = "Kyrgyz Republic"
        elif country == "Viet Nam":
            country = "Vietnam"
        elif country == "Republic Of The Congo":
            country = "Democratic Republic of the Congo"
        elif country == "Bolivarian Republic Of Venezuela":
            country = "Venezuela"
        elif country == "Micronesia (Federated States Of)":
            country = "Micronesia"
        elif country == "Saint Vincent And The Grenadines":
            country = "St. Vincent and the Grenadines"
        elif country == "Chinese Taipei":
            country = "China"

        country = country.lower()
        if country in iea_lname_dict:
            iea_data.append(iea_lname_dict[country])
        elif country in iea_sname_dict:
            iea_data.append(iea_sname_dict[country])
        elif country == "niue":
            iea_data.append(["Niue", "Niue", "NIU", '', ''])
        elif country == "unknown":
            iea_data.append(["Unknown", "Unknown", '', '', ''])
        elif country in iea_agg_lname_dict:
            iea_data.append(iea_agg_lname_dict[country])
        elif country in iea_agg_sname_dict:
            iea_data.append(iea_agg_sname_dict[country])
        else:
            iea_data.append(["", "", "", "", ""])
    iea_df = package_data(iea_df, iea_data)
    save(iea_df, "iea")


def cp_region_process():
    # Climate Policy
    cp_df = get_cp_data()
    cp_df.fillna("", inplace=True)
    cp_country = cp_df["Country"].to_list()
    cp_region_data = []
    for i in cp_country:
        if i in region_list:
            cp_region_data.append(region_dict[i])
        else:
            cp_region_data.append("")
    cp_df["IPCC_Region"] = cp_region_data

    cp_country_iso = cp_df["Country ISO"].tolist()
    cp_country_code_dict = {
        country_code[i]:
            [country_s_name[i], country_l_name[i], country_code[i], country_i_group[i], country_region[i]]
        for i in range(len(country_code))}
    cp_agg_code_dict = {
        aggregates_code[i]:
            [aggregates_s_name[i], aggregates_l_name[i], aggregates_code[i], '', '']
        for i in range(len(aggregates_code))}
    cp_data = []
    for iso in cp_country_iso:
        if iso in country_code:
            cp_data.append(cp_country_code_dict[iso])
        elif iso in aggregates_code:
            cp_data.append(cp_agg_code_dict[iso])
        elif iso in ["EUE"]:
            cp_data.append(cp_agg_code_dict["EUU"])
        elif iso in ["COK"]:
            cp_data.append(['Cook Islands', 'Cook Islands', 'COK', '', ''])
        elif iso in ["NIU"]:
            cp_data.append(['Niue', 'Niue', 'NIU', '', ''])
        else:
            cp_data.append(["", "", "", "", ""])
    cp_df = package_data(cp_df, cp_data)
    save(cp_df, "cp")


def lse_region_process():
    # LSE
    lse_df = get_lse_data()
    lse_df.fillna("", inplace=True)
    lse_geography = lse_df["Geography"].to_list()
    lse_region_data = []
    for i in lse_geography:
        if i in region_list:
            lse_region_data.append(region_dict[i])
        else:
            lse_region_data.append("")
    lse_df["IPCC_Region"] = lse_region_data

    lse_geography_iso = lse_df["Geography ISO"].tolist()
    lse_country_code_dict = {
        country_code[i]:
            [country_s_name[i], country_l_name[i], country_code[i], country_i_group[i], country_region[i]]
        for i in range(len(country_code))}
    lse_agg_code_dict = {
        aggregates_code[i]:
            [aggregates_s_name[i], aggregates_l_name[i], aggregates_code[i], '', '']
        for i in range(len(aggregates_code))}
    lse_data = []
    for iso in lse_geography_iso:
        if iso in country_code:
            lse_data.append(lse_country_code_dict[iso])
        elif iso in aggregates_code:
            lse_data.append(lse_agg_code_dict[iso])
        elif iso in ["EUR"]:
            lse_data.append(lse_agg_code_dict["EUU"])
        elif iso in ["TWN"]:
            lse_data.append(lse_country_code_dict["CHN"])
        elif iso in ["COK"]:
            lse_data.append(['Cook Islands', 'Cook Islands', 'COK', '', ''])
        elif iso in ["NIU"]:
            lse_data.append(['Niue', 'Niue', 'NIU', '', ''])
        else:
            lse_data.append(["", "", "", "", ""])
    lse_df = package_data(lse_df, lse_data)
    save(lse_df, "lse")


# Concat data frame
def package_data(df, data):
    df_data = pd.DataFrame(data)
    # print(df_data)
    df["Short_name"] = df_data[0]
    df["Long_name"] = df_data[1]
    df["ISO_code"] = df_data[2]
    df["Income_Group"] = df_data[3]
    df["WB_Region"] = df_data[4]
    return df


def save(df, file_name):
    with pd.ExcelWriter('{}_sector_region_result.xlsx'.format(file_name)) as writer:
        df.to_excel(writer, index=False)


if __name__ == '__main__':
    country_df = get_country_data()
    aggregates_df = get_aggregates_data()

    region_df = get_region_data()
    region_df["Countries"] = region_df["Countries"].apply(
        lambda x: [i.strip() for i in x.replace(" (the)", "").split(",")])

    # print(region_df["Regions"])
    north_america_country_list = region_df.loc[region_df["Regions"] == "North America", "Countries"].values[0]
    north_america_country_list.append("United States")
    # print(region_df.loc[region_df["Regions"] == "North America", "Countries"])
    region_df.loc[0, "Countries"] = str(north_america_country_list)
    # print(region_df.loc[region_df["Regions"] == "North America", "Countries"].values[0])

    europe_country_list = region_df.loc[region_df["Regions"] == "Europe", "Countries"].values[0]
    europe_country_list.append("United Kingdom")
    europe_country_list.append("Czech Republic")
    europe_country_list.append("Bosnia And Herzegovina")
    europe_country_list.append("Slovak Republic")
    europe_country_list.append("Kosovo")
    region_df.loc[1, "Countries"] = str(europe_country_list)

    asia_pacific_developed_country_list = \
        region_df.loc[region_df["Regions"] == "Asia-Pacific Developed", "Countries"].values[0]
    asia_pacific_developed_country_list.append("New Zealand")
    asia_pacific_developed_country_list.append("Australia")
    region_df.loc[2, "Countries"] = str(asia_pacific_developed_country_list)

    eurasia_country_list = region_df.loc[region_df["Regions"] == "Eurasia", "Countries"].values[0]
    eurasia_country_list.append("Republic Of Moldova")
    eurasia_country_list.append("Moldova, Republic of")
    eurasia_country_list.append("Moldova")
    eurasia_country_list.append("North Macedonia (Republic of North Macedonia)")
    eurasia_country_list.append("Russia")
    eurasia_country_list.append("Macedonia, the former Yugoslav Republic of")
    region_df.loc[3, "Countries"] = str(eurasia_country_list)

    latin_america_and_caribbean_country_list = \
        region_df.loc[region_df["Regions"] == "Latin America and Caribbean", "Countries"].values[0]
    latin_america_and_caribbean_country_list.append("Plurinational State Of Bolivia")
    latin_america_and_caribbean_country_list.append("Bolivarian Republic Of Venezuela")
    latin_america_and_caribbean_country_list.append("Antigua And Barbuda")
    latin_america_and_caribbean_country_list.append("Saint Vincent And The Grenadines")
    latin_america_and_caribbean_country_list.append("Bahamas, The")
    latin_america_and_caribbean_country_list.append("Bolivia")
    latin_america_and_caribbean_country_list.append("Venezuela")
    latin_america_and_caribbean_country_list.append("Venezuela, Bolivarian Republic of")
    latin_america_and_caribbean_country_list.append("Bolivia, Plurinational State of")
    region_df.loc[4, "Countries"] = str(latin_america_and_caribbean_country_list)

    africa_country_list = region_df.loc[region_df["Regions"] == "Africa", "Countries"].values[0]
    africa_country_list.append("Republic Of The Congo")
    africa_country_list.append("Democratic Republic Of The Congo")
    africa_country_list.append("Democratic Republic of Congo")
    africa_country_list.append("Congo, the Democratic Republic of the")
    africa_country_list.append("United Republic Of Tanzania")
    africa_country_list.append("Tanzania, United Republic of")
    africa_country_list.append("Cape Verde")
    africa_country_list.append("Libyan Arab Jamahiriya")
    region_df.loc[5, "Countries"] = str(africa_country_list)

    middle_east_country_list = region_df.loc[region_df["Regions"] == "Middle East", "Countries"].values[0]
    middle_east_country_list.append("Islamic Republic Of Iran")
    middle_east_country_list.append("Iran")
    middle_east_country_list.append("Syria")
    region_df.loc[6, "Countries"] = str(middle_east_country_list)

    eastern_asia_country_list = region_df.loc[region_df["Regions"] == "Eastern Asia", "Countries"].values[0]
    eastern_asia_country_list.append("Korea")
    eastern_asia_country_list.append("Korea, North")
    eastern_asia_country_list.append("South Korea")
    eastern_asia_country_list.append("Republic of Korea")
    eastern_asia_country_list.append("Democratic People's Republic of Korea")
    eastern_asia_country_list.append("People's Republic Of China")
    eastern_asia_country_list.append("Chinese Taipei")
    eastern_asia_country_list.append("Taiwan")
    region_df.loc[7, "Countries"] = str(eastern_asia_country_list)

    southern_asia_country_list = region_df.loc[region_df["Regions"] == "Southern Asia", "Countries"].values[0]
    southern_asia_country_list.append("India")
    southern_asia_country_list.append("Sri Lanka")
    region_df.loc[8, "Countries"] = str(southern_asia_country_list)

    south_east_asia_and_developing_pacific_country_list = \
        region_df.loc[region_df["Regions"] == "South-East Asia and developing Pacific", "Countries"].values[0]
    south_east_asia_and_developing_pacific_country_list.append("Micronesia (Federated States Of)")
    south_east_asia_and_developing_pacific_country_list.append("Micronesia")
    south_east_asia_and_developing_pacific_country_list.append("Micronesia, Federated States of")
    south_east_asia_and_developing_pacific_country_list.append("Vietnam")
    region_df.loc[9, "Countries"] = str(south_east_asia_and_developing_pacific_country_list)

    region_dict = region_df.to_dict(orient="records")
    # print(region_dict)

    # Country:Region dict
    region_dict = {j: i["Regions"] for i in region_dict for j in eval(i["Countries"])}
    # Country list
    region_list = list(region_dict.keys())
    country_df["Income Group"].fillna("", inplace=True)

    country_s_name = country_df["Short Name"].tolist()
    country_l_name = country_df["Long Name"].tolist()
    country_code = country_df["Code"].tolist()
    country_i_group = country_df["Income Group"].tolist()
    country_region = country_df["Region"].tolist()

    aggregates_s_name = aggregates_df["Short Name"].tolist()
    aggregates_l_name = aggregates_df["Long Name"].tolist()
    aggregates_code = aggregates_df["Code"].tolist()

    iea_region_process()
    cp_region_process()
    lse_region_process()
