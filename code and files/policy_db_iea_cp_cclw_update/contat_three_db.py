import re
import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_data(file_name):
    df = pd.read_excel(file_name)
    return df


def iea_process(df):
    df.rename(columns={"LearnMore": "Source"}, inplace=True)
    df.loc[:, "db_source"] = ["IEA" for _ in range(df.shape[0])]
    return df


def cp_process(df):
    # df = df[df["Policy objective"].apply(lambda x: len(re.findall(r"Mitigation", str(x))) > 0)]
    df["Policy objective"].fillna("", inplace=True)
    # cp_mitigation = df.loc[df["Policy objective"].str.contains("Mitigation")].copy()
    # print(cp_mitigation.info())
    df.rename(columns={"Source or references": "Source", "Implementation state": "Status",
                       "Policy description": "Policy_Content", "Date of decision": "Year",
                       "Policy name": "Policy"}, inplace=True)
    df.loc[:, "db_source"] = ["Climate Policy" for _ in range(df.shape[0])]

    cp_mitigation = df.loc[df["Policy objective"].str.contains("Mitigation")].copy()
    cp_adaptation = df[df["Policy objective"].str.contains("Adaptation")]
    cp_adaptation_or_mitigation_num = len(df[df["Policy objective"].str.contains("Adaptation|Mitigation")])
    cp_adaptation_and_mitigation_num = len(cp_mitigation) + len(cp_adaptation) - cp_adaptation_or_mitigation_num

    with open("dup_statistic.txt", 'a') as f:
        f.write("====================Adaptation and Mitigation: contact_three_db.py====================" + '\n')
        f.write('\n')
        f.write("Climate Policy Number Before Adaptation and Mitigation: " + str(len(df)) + '\n')
        f.write("Climate Policy Adaptation and Mitigation Number: " + str(cp_adaptation_and_mitigation_num) + '\n')
        f.write(
            "Climate Policy Mitigation Number: " + str(len(cp_mitigation) - cp_adaptation_and_mitigation_num) + '\n')
        f.write(
            "Climate Policy Adaptation Number: " + str(len(cp_adaptation) - cp_adaptation_and_mitigation_num) + '\n')
        f.write("Climate Policy Adaptation and Mitigation Unknown Number: " + str(
            len(df) - cp_adaptation_or_mitigation_num) + '\n')
        f.write('\n')
    return cp_mitigation, cp_adaptation


def lse_process(df):
    df["Responses"].fillna("", inplace=True)
    # lse_mitigation = df.loc[df["Responses"].str.contains("Mitigation")].copy()
    df["Events"].fillna("", inplace=True)
    df.rename(columns={"Documents": "Source",
                       "Description": "Policy_Content", "Title": "Policy"}, inplace=True)
    df.loc[:, "db_source"] = ["LSE" for _ in range(df.shape[0])]
    df.loc[:, "Jurisdiction"] = ["National" for _ in range(df.shape[0])]
    df.loc[:, "Status"] = ["" for _ in range(df.shape[0])]
    df.loc[:, "Year"] = df["Events"].apply(
        lambda x: re.findall(r"\d{1,2}/\d{1,2}/(\d{4})", str(x))[0] if len(
            re.findall(r"\d{1,2}/\d{1,2}/(\d{4})", str(x))) > 0 else str(x))

    lse_mitigation = df.loc[df["Responses"].str.contains("Mitigation")].copy()
    lse_adaptation = df[df["Responses"].str.contains("Adaptation")]
    lse_adaptation_and_mitigation_num = len(lse_mitigation) + len(lse_adaptation) - len(df)

    with open("dup_statistic.txt", 'a') as f:
        f.write("LSE Number Before Adaptation and Mitigation: " + str(len(df)) + '\n')
        f.write("LSE Adaptation and Mitigation Number: " + str(lse_adaptation_and_mitigation_num) + '\n')
        f.write("LSE Mitigation Number: " + str(len(lse_mitigation) - lse_adaptation_and_mitigation_num) + '\n')
        f.write("LSE Adaptation Number: " + str(len(lse_adaptation) - lse_adaptation_and_mitigation_num) + '\n')
        f.write('\n')
    return lse_mitigation, lse_adaptation


def contact_data(iea, cp, lse):
    iea_data = iea[
        ["Policy", "Short_name", "ISO_code", "Year", "law or strategy", "Policy Type", "IPCC_Region", "WB_Region",
         "sector", "subsector", "Instrument", "Sector-Instrument", "objective", "subobjective", "Long_name",
         "Income_Group", "Annex", "Policy_Content", "Status", "Jurisdiction", "db_source", "Source"]]
    cp_data = cp[
        ["Policy", "Short_name", "ISO_code", "Year", "law or strategy", "Policy Type", "IPCC_Region", "WB_Region",
         "sector", "subsector", "Instrument", "Sector-Instrument", "objective", "subobjective", "Long_name",
         "Income_Group", "Annex", "Policy_Content", "Status", "Jurisdiction", "db_source", "Source"]]
    lse_data = lse[
        ["Policy", "Short_name", "ISO_code", "Year", "law or strategy", "Policy Type", "IPCC_Region", "WB_Region",
         "sector", "subsector", "Instrument", "Sector-Instrument", "objective", "subobjective", "Long_name",
         "Income_Group", "Annex", "Policy_Content", "Status", "Jurisdiction", "db_source", "Source"]]
    all_data = pd.concat([iea_data, cp_data, lse_data], axis=0, ignore_index=True)
    return all_data


def save(all_df, filename):
    with pd.ExcelWriter(filename) as writer:
        all_df.to_excel(writer, index=False)


if __name__ == '__main__':
    iea_df = get_data("iea_sector_region_instrument_annex_objective_law_result.xlsx")
    cp_df = get_data("cp_sector_region_instrument_annex_objective_law_result.xlsx")
    lse_df = get_data("lse_sector_region_instrument_annex_objective_law_result.xlsx")

    iea_df = iea_process(iea_df)
    cp_df_mitigation, cp_df_adaptation = cp_process(cp_df)
    lse_df_mitigation, lse_df_adaptation = lse_process(lse_df)

    with open("Mitigation and Adaptation.txt") as f:
        adaptation_keywords = f.read().lower().split('\n')[0]
        # Adaptation_keywords = f.read().lower().split('\n')
        # print(Adaptation_keywords)
        # Adaptation_word_group = Adaptation_keywords[0]
        # Adaptation = Adaptation_keywords[1]

    # for i, v in iea_df['Policy'].str.contains(Adaptation_keywords.replace(";", '|')).iteritems():
    #     print('index: ', i, 'value: ', v)
    iea_df_adaptation = iea_df[iea_df['Policy'].str.contains(adaptation_keywords.replace(";", '|'))]

    # '|' is or
    iea_df_mitigation = iea_df[~ iea_df['Policy'].str.contains(adaptation_keywords.replace(";", '|'))]

    with open("dup_statistic.txt", 'a') as f:
        f.write("IEA Number Before Adaptation and Mitigation: " + str(len(iea_df)) + '\n')
        f.write("IEA Mitigation Number: " + str(len(iea_df_mitigation)) + '\n')
        f.write("IEA Adaptation Number: " + str(len(iea_df_adaptation)) + '\n')
        f.write('\n')

    all_data_mitigation = contact_data(iea_df_mitigation, cp_df_mitigation, lse_df_mitigation)
    all_data_adaptation = contact_data(iea_df_adaptation, cp_df_adaptation, lse_df_adaptation)
    # print(all_data_mitigation.info())

    with open("dup_statistic.txt", 'a') as f:
        f.write("All Number Before Manual: " + str(len(all_data_mitigation)) + '\n')
        f.write('\n')

    save(all_data_mitigation, 'policy_concat_mitigation_result.xlsx')
    save(all_data_adaptation, 'policy_concat_adaptation_result.xlsx')
