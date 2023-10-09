import pandas as pd
import numpy as np
import os
import sys
import re


def get_data():
    data_result = pd.read_excel("/home/zhhuang/climate_policy_paper/code/data/all_policies_mitigation_result.xlsx")
    return data_result


if __name__ == '__main__':
    df = get_data()
    try:
        df.rename(columns={"Unnamed: 0": "Index"}, inplace=True)
    except:
        pass
    try:
        df.rename(columns={"A": "Index"}, inplace=True)
    except:
        pass
    try:
        df.rename(columns={"Scope": "Jurisdiction"}, inplace=True)
    except:
        pass

    policy_df = df[["Index", "Policy", "Policy_Content", "Source"]]
    additional_infor_df = df[["Index", "Policy_raw", "Policy_Content_raw", "Year", "URL"]]
    dup_similar_df = df[["Index", "group_policy_number", "bm25_score_first", "bm25_policy_first", "bm25_index_first"]]
    character_df = df[["Index", "sector", "objective", "Instrument", "Policy Type", "law or strategy"]]
    country_jurisdiction_df = df[
        ["Index", "ISO_code", "Jurisdiction", "IPCC_Region", "Short_name", "Long_name", "Income_Group", "WB_Region",
         "Annex"]]
    with pd.ExcelWriter("/home/zhhuang/climate_policy_paper/code/data/mysql_Policy.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        policy_df.to_excel(writer, index=False)
    with pd.ExcelWriter("/home/zhhuang/climate_policy_paper/code/data/mysql_Additional_Information.xlsx",
                        engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        additional_infor_df.to_excel(writer, index=False)
    with pd.ExcelWriter("/home/zhhuang/climate_policy_paper/code/data/mysql_Similarity_Information.xlsx",
                        engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        dup_similar_df.to_excel(writer, index=False)
    with pd.ExcelWriter("/home/zhhuang/climate_policy_paper/code/data/mysql_Characteristic.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        character_df.to_excel(writer, index=False)
    with pd.ExcelWriter("/home/zhhuang/climate_policy_paper/code/data/mysql_Country_Jurisdiction.xlsx",
                        engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        country_jurisdiction_df.to_excel(writer, index=False)

    topic_df = pd.read_excel("/home/zhhuang/climate_policy_paper/code/Topic_country_expand.xlsx")
    topic_df = topic_df[["Index", "Topic", "Name", "Top_n_words", "Probability", "Representative_document"]]
    with pd.ExcelWriter("/home/zhhuang/climate_policy_paper/code/data/mysql_Topic.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        topic_df.to_excel(writer, index=False)
