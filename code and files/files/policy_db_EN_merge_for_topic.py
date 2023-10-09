import pandas as pd

import shutil


def get_country_data():
    data = pd.read_excel("Countries_Code.xlsx")
    return data


def get_aggregates_data():
    data = pd.read_excel("Aggregates_Code.xlsx")
    return data


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
        # data = data.drop(['Country'], axis=1).join(
        #     data['Country'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename(
        #         'Country')).reset_index(drop=True)
        data['Country'] = data['Country'].str.strip()
        data = data.drop(data[data['Country'].isin(
            ["Kingdom of", "Dem. Rep. of", "Republic of", 'Islamic Republic of', 'Un. Rep. of',
             'Fed. States', 'Yugoslavia', 'Holy See', 'EURATOM European Atomic Energy Community',
             'Palestinian Authority', 'Réunion (France)', 'former USSR/Soviet Union',
             'Economic Community of West African States', 'Economic Community of West African States',
             'IAEA International Atomic Energy Agency', 'ECE UN Economic Commission for Europe',
             'Eastern African Community'])].index).reset_index(drop=True)
    if filename == 'APEP':
        # data = data.drop(['Country'], axis=1).join(
        #     data['Country'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename(
        #         'Country')).reset_index(drop=True)
        data = data.drop(data[data['Country'].isin(["HONG KONG", "MACAU", "OTHER"])].index).reset_index(drop=True)
        # CHINA, HONG KONG, CHINA, MACAU, CHINA: dedup
        # print(data)
    if filename in ['CDR_NETS', 'CDR_CCUS']:
        # data = data.drop(['Keyword'], axis=1).join(
        #     data['Keyword'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename(
        #         'Keyword')).reset_index(drop=True)
        data = data.drop(data[data['Keyword'].isin(
            ["Pore Space Ownership", "Enhanced Oil Recovery", "CCS Liability", "EU Emissions Trading Scheme",
             "Marine Sequestration", "Kyoto Protocol", "Building with Biomass", "Clean Air Act",
             "Paris Agreement", "Environmental Justice", "Convention on Biological Diversity",
             "London Convention/London Protocol", "UNFCCC", "Africa", "REDD+",
             "United Nations Convention on the Law of the Sea"])].index).reset_index(drop=True)
    return data


def merge_for_topic_process(filename):
    df = load_excel(filename)
    df.fillna("", inplace=True)
    if filename in ["CDR_NETS", 'CDR_CCUS']:
        df = df.rename(columns={"Keyword": "Country"})
        countrys = df["Country"].to_list()
    else:
        countrys = df["Country"].to_list()
        # pass
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
    # try:
    #     df = df.rename(columns={"Country": "Short_name"})
    # except:
    #     pass
    df = df[column]
    return df


def package_data(df, data):
    df_data = pd.DataFrame(data)
    df["Short_name"] = df_data[0]
    df["Long_name"] = df_data[1]
    df["ISO_code"] = df_data[2]
    df["Income_Group"] = df_data[3]
    df["WB_Region"] = df_data[4]

    return df


if __name__ == '__main__':
    country_df = get_country_data()
    aggregates_df = get_aggregates_data()
    country_df["Income Group"].fillna("", inplace=True)

    country_s_name = country_df["Short Name"].tolist()
    country_l_name = country_df["Long Name"].tolist()
    country_code = country_df["Code"].tolist()
    country_i_group = country_df["Income Group"].tolist()
    country_region = country_df["Region"].tolist()

    aggregates_s_name = aggregates_df["Short Name"].tolist()
    aggregates_l_name = aggregates_df["Long Name"].tolist()
    aggregates_code = aggregates_df["Code"].tolist()

    country_sname_dict = {
        country_s_name[i].lower(): [country_s_name[i], country_code[i]]
        for i in range(len(country_s_name))}
    country_lname_dict = {
        country_l_name[i].lower(): [country_l_name[i], country_code[i]]
        for i in range(len(country_l_name))}

    # ECOLEX_Legislation = []
    # for i in range(0, 40):
    #     ECOLEX_Legislation.append("ECOLEX_Legislation_{}".format(i))
    db = ['MEE_PRC', 'GOV_PRC', 'CDR_NETS', 'CDR_CCUS', 'CRT', 'ICAP_ETS', 'ECOLEX_Treaty', 'APEP',
          'ECOLEX_Legislation', 'EEA']
    # ['MEE_PRC', 'GOV_PRC', 'CDR_NETS', 'CDR_CCUS', 'CRT', 'ICAP_ETS', 'ECOLEX_Treaty', 'APEP', 'ECOLEX_Legislation']

    column = ['Policy',
              'Policy_Content',
              'Year',
              'URL',  # iea_cp_cclw: Source
              'Source',  # iea_cp_cclw: db_source
              'Country',
              'ISO_code']

    iea_cp_cclw_column = ['Policy',
                          'Policy_Content',
                          'Year',
                          'Source',  # iea_cp_cclw: Source
                          'db_source',  # iea_cp_cclw: db_source
                          'Short_name',
                          'ISO_code']

    iea_cp_cclw_df = pd.read_excel('iea_cp_cclw_EN.xlsx')
    iea_cp_cclw_df = iea_cp_cclw_df[iea_cp_cclw_column]
    iea_cp_cclw_df = iea_cp_cclw_df.rename(
        columns={"Source": 'URL', 'db_source': "Source", 'Jurisdiction_standard_amend': "Scope",
                 'Short_name': "Country"})

    dfs = [iea_cp_cclw_df]
    for fn in ['MEE_PRC', 'GOV_PRC', 'CDR_NETS', 'CDR_CCUS', 'CRT', 'ICAP_ETS', 'ECOLEX_Treaty', 'APEP',
               'ECOLEX_Legislation', 'EEA']:
        df = merge_for_topic_process(fn)
        dfs.append(df)

    df_all = pd.concat(dfs)
    with pd.ExcelWriter("ALL_POLICIES_EN_FOR_TOPIC.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        df_all.to_excel(writer)

    shutil.copy("ALL_POLICIES_EN_FOR_TOPIC.xlsx", '/home/zhhuang/climate_policy_paper/code/data')
