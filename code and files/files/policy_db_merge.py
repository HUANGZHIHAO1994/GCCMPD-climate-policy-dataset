import re
import pandas as pd
import numpy as np
import os
import shutil

column = ['Policy_raw',
          'Year',
          'Policy_Content_raw',
          'URL',  # iea_cp_cclw: Source
          'Scope',  # iea_cp_cclw: Jurisdiction_standard_amend
          'Source',  # iea_cp_cclw: db_source
          'Policy',
          'Policy_Content',
          'IPCC_Region',
          'Short_name',
          'Long_name',
          'ISO_code',
          'Income_Group',
          'WB_Region',
          'Annex']

iea_cp_cclw_column = ['Policy_raw',
                      'Year',
                      'Policy_Content_raw',
                      'Source',  # iea_cp_cclw: Source
                      'Jurisdiction_standard_amend',  # iea_cp_cclw: Source
                      'db_source',  # iea_cp_cclw: db_source
                      'Policy',
                      'Policy_Content',
                      'IPCC_Region',
                      'Short_name',
                      'Long_name',
                      'ISO_code',
                      'Income_Group',
                      'WB_Region',
                      'Annex']


def get_data(file_name):
    df = pd.read_excel('./{}_EN_ISO_REGION_INCOME.xlsx'.format(file_name))
    df = df[column]
    return df


if __name__ == '__main__':

    iea_cp_cclw_df = pd.read_excel('iea_cp_cclw_EN.xlsx')
    iea_cp_cclw_df = iea_cp_cclw_df[iea_cp_cclw_column]
    iea_cp_cclw_df = iea_cp_cclw_df.rename(
        columns={"Source": 'URL', 'db_source': "Source", 'Jurisdiction_standard_amend': "Scope"})
    db = ['MEE_PRC', 'GOV_PRC', 'CDR_NETS', 'CDR_CCUS', 'CRT', 'ICAP_ETS', 'ECOLEX_Treaty', 'APEP',
          'ECOLEX_Legislation', 'EEA']

    dfs = [iea_cp_cclw_df]
    for index, inputfile in enumerate(db):
        print(inputfile)
        dfs.append(get_data(inputfile))

    df_all = pd.concat(dfs)
    with pd.ExcelWriter("ALL_POLICIES_EN.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        df_all.to_excel(writer, index=False)

    shutil.copy("ALL_POLICIES_EN.xlsx", '/home/zhhuang/climate_policy_paper/code/data')
