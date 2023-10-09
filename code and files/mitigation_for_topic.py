import re
import pandas as pd
import numpy as np
import os


def save(all_df, filename):
    with pd.ExcelWriter(filename, engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        all_df.to_excel(writer, index=False)


if __name__ == '__main__':
    path = []
    for i in os.listdir("/home/zhhuang/climate_policy_paper/code/data/"):
        if ("move_duplicate_result_for_topic" in i) and (i.split("_")[0] == 'bm25') and (
                re.findall(r'\d+\.\d+|\d+', i.split("_")[1])):
            print(i)
            path.append(os.path.join("/home/zhhuang/climate_policy_paper/code/data/", i))
    if len(path) == 1:
        df_all_policies_dedup = pd.read_excel(path[0], sheet_name='all_policies_dedup')
    else:
        raise IOError('The file is not exist or too many files！')

    with open("/home/zhhuang/climate_policy_paper/code/policy_db_iea_cp_cclw/Mitigation and Adaptation.txt") as f:
        adaptation_keywords = f.read().lower().split('\n')[0]

    df_all_policies_dedup_adaptation = df_all_policies_dedup[
        df_all_policies_dedup['Policy'].str.contains(adaptation_keywords.replace(";", '|')) | df_all_policies_dedup[
            'Policy_Content'].str.contains(adaptation_keywords.replace(";", '|'))]

    # '|' is or
    df_all_policies_dedup_mitigation = df_all_policies_dedup[
        ~ (df_all_policies_dedup['Policy'].str.contains(adaptation_keywords.replace(";", '|')) | df_all_policies_dedup[
            'Policy_Content'].str.contains(adaptation_keywords.replace(";", '|')))]

    save(df_all_policies_dedup_mitigation,
         '/home/zhhuang/climate_policy_paper/code/data/all_policies_mitigation_result_for_topic.xlsx')
    save(df_all_policies_dedup_adaptation,
         '/home/zhhuang/climate_policy_paper/code/data/all_policies_adaptation_result_for_topic.xlsx')
