import pandas as pd
import numpy as np
import os
import sys


def load_excel(filename):
    data = pd.read_excel('./{}_EN.xlsx'.format(filename))
    data.fillna("", inplace=True)
    if filename == 'ECOLEX_Legislation':
        pattern = '|'.join(
            ['\(usa\)', '\(uk\)', '\(denmark\)', "\(france\)", "\(australia\)", "\(new zealand\)", "\(norway\)",
             "\(netherlands\)"])
        data['Country'] = data['Country'].str.lower().str.replace(pattern, '', regex=True).str.strip()
        data = data.drop(data[data['Country'].isin(
            ["palestinian authority"])].index).reset_index(drop=True)
    if filename == 'ECOLEX_Treaty':
        data = data.drop(['Country'], axis=1).join(
            data['Country'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename(
                'Country')).reset_index(drop=True)
        data['Country'] = data['Country'].str.strip()
        data = data.drop(data[data['Country'].isin(
            ["Kingdom of", "Dem. Rep. of", "Republic of", 'Islamic Republic of', 'Un. Rep. of',
             'Fed. States', 'Yugoslavia', 'Holy See', 'EURATOM European Atomic Energy Community',
             'Palestinian Authority', 'Réunion (France)', 'former USSR/Soviet Union',
             'Economic Community of West African States', 'Economic Community of West African States',
             'IAEA International Atomic Energy Agency', 'ECE UN Economic Commission for Europe',
             'Eastern African Community'])].index).reset_index(drop=True)
    if filename == 'APEP':
        data = data.drop(['Country'], axis=1).join(
            data['Country'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename(
                'Country')).reset_index(drop=True)
        data = data.drop(data[data['Country'].isin(["HONG KONG", "MACAU", "OTHER"])].index).reset_index(drop=True)
        # CHINA, HONG KONG, CHINA, MACAU, CHINA: dedup
        # print(data)
    if filename in ['CDR_NETS', 'CDR_CCUS']:
        data = data.drop(['Keyword'], axis=1).join(
            data['Keyword'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename(
                'Keyword')).reset_index(drop=True)
        data = data.drop(data[data['Keyword'].isin(
            ["Pore Space Ownership", "Enhanced Oil Recovery", "CCS Liability", "EU Emissions Trading Scheme",
             "Marine Sequestration", "Kyoto Protocol", "Building with Biomass", "Clean Air Act",
             "Paris Agreement", "Environmental Justice", "Convention on Biological Diversity",
             "London Convention/London Protocol", "UNFCCC", "Africa", "REDD+",
             "United Nations Convention on the Law of the Sea"])].index).reset_index(drop=True)
        # CHINA, HONG KONG, CHINA, MACAU, CHINA: dedup
        # print(data)
    return data


def get_country_data():
    data = pd.read_excel("Countries_Code.xlsx")
    return data


def get_region_data():
    data = pd.read_excel("Region.xlsx")
    return data


def get_iso_region_data():
    data = pd.read_excel("policy_db_complete.xlsx")
    data = data[['IPCC_Region', 'ISO_code']]
    return data


def get_annex_data():
    df = pd.read_excel("Annex.xlsx")
    return df


def get_aggregates_data():
    data = pd.read_excel("Aggregates_Code.xlsx")
    return data


def region_iso_annex_process(filename):
    df = load_excel(filename)
    df.fillna("", inplace=True)
    if filename in ["CDR_NETS", 'CDR_CCUS']:
        countrys = df["Keyword"].to_list()
    else:
        countrys = df["Country"].to_list()

    # region_data = []
    # for i in countrys:
    #     if i in region_list:
    #         region_data.append(region_dict[i])
    #     else:
    #         region_data.append("")
    # df["IPCC_Region"] = region_data

    if filename in ["CDR_NETS", 'CDR_CCUS', 'ECOLEX_Legislation']:
        df["Scope"] = ["National"] * len(countrys)
    elif filename in ['ECOLEX_Treaty']:
        df["Scope"] = ["International"] * len(countrys)

    if filename in ['APEP']:
        df = df.rename(columns={"single_url_2": "URL"})
    if filename in ['EEA']:
        df['Source'] = 'EEA'
        df = df.rename(columns={"Geographical_coverage": "Scope"})
        df = df.rename(columns={"URL to main reference": "URL"})
        df = df.rename(columns={"Implementation period start": "Year"})

    # Short_name & Long_name dict
    sname_dict = {
        country_s_name[i].lower():
            [country_s_name[i], country_l_name[i], country_code[i], country_i_group[i], country_region[i]]
        for i in range(len(country_s_name))}
    lname_dict = {
        country_l_name[i].lower():
            [country_s_name[i], country_l_name[i], country_code[i], country_i_group[i], country_region[i]]
        for i in range(len(country_l_name))}
    agg_sname_dict = {
        aggregates_s_name[i].lower():
            [aggregates_s_name[i], aggregates_l_name[i], aggregates_code[i], '', '']
        for i in range(len(aggregates_s_name))}
    agg_lname_dict = {
        aggregates_l_name[i].lower():
            [aggregates_s_name[i], aggregates_l_name[i], aggregates_code[i], '', '']
        for i in range(len(aggregates_l_name))}
    # print(sname_dict)

    data = []
    for country in countrys:
        country = country.lower()
        if country == "kyrgyzstan":
            country = "Kyrgyz Republic"
        elif country == "viet nam":
            country = "Vietnam"
        elif country == "republic df the congo":
            country = "Democratic Republic of the Congo"
        elif country == "bolivarian republic of venezuela":
            country = "Venezuela"
        elif country == "bolivia (plurinational state of)":
            country = "Bolivia"
        elif country == "boliv. rep. of":
            country = "Bolivia"
        elif country == "lao":
            country = "LAO PDR"
        elif country == "lao, people's dem. rep.":
            country = "LAO PDR"
        elif country == "gambia":
            country = "The Gambia"
        elif country == "bahamas":
            country = "The Bahamas"
        elif country == "micronesia (federated states of)":
            country = "Micronesia"
        elif country == "saint vincent and the grenadines":
            country = "st. vincent and the grenadines"
        elif country == "chinese taipei":
            country = "China"
        elif country == "usa":
            country = "United States"
        elif country == "hong kong, china":
            country = "China"
        elif country == "china, other":
            country = "China"
        elif country == "macau, china":
            country = "China"
        elif country == "macau (china)":
            country = "China"
        elif country == "iran (islamic republic of)":
            country = "Iran"
        elif country == "iran, islamic republic of":
            country = "Iran"
        elif country == "dpr korea":
            country = "Dem. People's Rep. Korea"
        elif country == "korea, republic of":
            country = "Korea"
        elif country == "south korea":
            country = "Korea"
        elif country == "taiwan, province of china":
            country = "China"
        elif country == "people's dem. rep.":
            country = "Dem. People's Rep. Korea"
        elif country == "korea, dem. people's rep.":
            country = "Dem. People's Rep. Korea"
        elif country == "dem. people's rep.":
            country = "Dem. People's Rep. Korea"
        elif country == "slovakia":
            country = "Slovak Republic"
        elif country == "great britain":
            country = "United Kingdom"
        elif country == "czechoslovakia":
            country = "Czech Republic"
        elif country == "puerto rico (usa)":
            country = "Puerto Rico"
        elif country == "venezuela, boliv. rep. of":
            country = "Venezuela"
        elif country == "eswatini, kingdom of":
            country = "Kingdom of Eswatini"
        elif country == "moldova, republic of":
            country = "Republic of Moldova"
        elif country == "bermuda (uk)":
            country = "The Bermudas"
        elif country == "congo, dem. rep. of":
            country = "Democratic Republic of the Congo"
        elif country == "micronesia, fed. states":
            country = "Federated States of Micronesia"
        elif country == "turks-caicos islands (uk)":
            country = "Turks and Caicos Islands"
        elif country == "cayman islands (uk)":
            country = "Cayman Islands"
        elif country == "tanzania, un. rep. of":
            country = "United Republic of Tanzania"
        elif country == "anguilla":
            country = "United Kingdom"
        elif country == "falkland islands (malvinas)":
            country = "United Kingdom"
        elif country == "jersey":
            country = "United Kingdom"
        elif country == "guernsey":
            country = "United Kingdom"
        elif country == "saint helena":
            country = "United Kingdom"
        elif country == "montserrat":
            country = "United Kingdom"
        elif country == "pitcairn":
            country = "United Kingdom"
        elif country == "turks-caicos islands":
            country = "Turks and Caicos Islands"
        elif country == "northern mariana is.":
            country = "Commonwealth of the Northern Mariana Islands"
        elif country == "sint maarten":
            country = "Kingdom of the Netherlands"
        elif country == "netherlands antilles":
            country = "Kingdom of the Netherlands"
        elif country == "serbia and montenegro":
            country = "Republic of Serbia"
        elif country == "martinique":
            country = "French Republic"
        elif country == "guadeloupe":
            country = "French Republic"
        elif country == "french guiana":
            country = "French Republic"
        elif country == "réunion":
            country = "French Republic"
        elif country == "saint barthélemy (fra)":
            country = "French Republic"
        elif country == "mayotte":
            country = "French Republic"
        elif country == "norfolk island":
            country = "Commonwealth of Australia"
        elif country == "tokelau":
            country = "New Zealand"
        elif country == "svalbard":
            country = "Norway"

        country = country.lower()
        if country in lname_dict:
            data.append(lname_dict[country])
        elif country in sname_dict:
            data.append(sname_dict[country])
        elif country == "niue":
            data.append(["Niue", "Niue", "NIU", '', ''])
        elif country == "niue (new zealand)":
            data.append(["Niue", "Niue", "NIU", '', ''])
        elif country == "saint kitts and nevis":
            data.append(["Saint Kitts and Nevis", "Saint Kitts and Nevis", "KNA", '', ''])
        elif country == "saint lucia":
            data.append(["Saint Lucia", "Saint Lucia", "LCA", '', ''])
        elif country == "sao tome and principe":
            data.append(["Sao Tome and Principe", "Sao Tome and Principe", "STP", '', ''])
        elif country == "cook islands":
            data.append(['Cook Islands', 'Cook Islands', 'COK', '', ''])
        elif country == "cook islands (new zealand)":
            data.append(['Cook Islands', 'Cook Islands', 'COK', '', ''])
        elif country == "libyan arab jamahiriya":
            data.append(['Libyan Arab Jamahiriya', 'Libyan Arab Jamahiriya', 'LBY', '', ''])
        elif country == "unknown":
            data.append(["Unknown", "Unknown", '', '', ''])
        elif country in agg_lname_dict:
            data.append(agg_lname_dict[country])
        elif country in agg_sname_dict:
            data.append(agg_sname_dict[country])
        else:
            data.append(["", "", "", "", ""])
    df = package_data(df, data)
    save(df, filename)


# Concat data frame
def package_data(df, data):
    df_data = pd.DataFrame(data)
    df["Short_name"] = df_data[0]
    df["Long_name"] = df_data[1]
    df["ISO_code"] = df_data[2]
    df["Income_Group"] = df_data[3]
    df["WB_Region"] = df_data[4]

    annex = []
    for num, row in df.iterrows():
        if row["ISO_code"] in annex_1_iso_list:
            annex.append("Annex I")
        else:
            annex.append("Non Annex I")
    df["Annex"] = annex

    region_data = []
    for num, row in df.iterrows():
        if row["ISO_code"] in iso_region_dict:
            region_data.append(iso_region_dict[row["ISO_code"]])
        else:
            region_data.append("")
    df["IPCC_Region"] = region_data
    return df


def save(df, file_name):
    with pd.ExcelWriter('{}_EN_ISO_REGION_INCOME.xlsx'.format(file_name), engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        df.to_excel(writer, index=False)


if __name__ == '__main__':
    country_df = get_country_data()
    aggregates_df = get_aggregates_data()

    region_df = get_region_data()
    region_df["Countries"] = region_df["Countries"].apply(
        lambda x: [i.strip() for i in x.replace(" (the)", "").split(",")])
    # print(region_df)

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
    # print(region_dict)

    iso_region_df = get_iso_region_data()
    iso_region_dict = iso_region_df.to_dict(orient="records")
    # ISO:Region dict
    iso_region_dict = {i["ISO_code"]: i["IPCC_Region"] for i in iso_region_dict}
    iso_region_dict['ASM'] = 'South-East Asia and developing Pacific'
    iso_region_dict['GUM'] = 'South-East Asia and developing Pacific'
    iso_region_dict['MNP'] = 'South-East Asia and developing Pacific'
    iso_region_dict['NCL'] = 'South-East Asia and developing Pacific'
    iso_region_dict['COM'] = 'Africa'
    # print(iso_region_dict)

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

    annex_df = get_annex_data()
    # print(annex_df["Annex I"])

    annex_df["Annex I"] = annex_df["Annex I"].apply(lambda x: x.strip())
    annex_country = annex_df["Annex I"].to_list()
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

    # ECOLEX_Legislation = []
    # for i in range(0, 40):
    #     ECOLEX_Legislation.append("ECOLEX_Legislation_{}".format(i))
    db = ['MEE_PRC', 'GOV_PRC', 'CDR_NETS', 'CDR_CCUS', 'CRT', 'ICAP_ETS', 'ECOLEX_Treaty', 'APEP',
          'ECOLEX_Legislation', 'EEA']
    # ['MEE_PRC', 'GOV_PRC', 'CDR_NETS', 'CDR_CCUS', 'CRT', 'ICAP_ETS', 'ECOLEX_Treaty', 'APEP', 'ECOLEX_Legislation']
    for fn in ['MEE_PRC', 'GOV_PRC', 'CDR_NETS', 'CDR_CCUS', 'CRT', 'ICAP_ETS', 'ECOLEX_Treaty', 'APEP',
               'ECOLEX_Legislation', 'EEA']:
        region_iso_annex_process(fn)
    # cp_region_process()
    # lse_region_process()
