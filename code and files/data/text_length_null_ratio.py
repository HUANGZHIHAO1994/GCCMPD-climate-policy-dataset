import pandas as pd
import numpy as np


def policy_after_fill():
    print("================== After fill Policy Content:  ==================")
    df = pd.read_excel('policy_db_complete.xlsx', sheet_name='all_policies_dedup')
    df = df[['Policy', 'Policy_Content', 'db_source']]
    # df.dropna(subset=['Policy_Content'], inplace=True)
    df["Policy_Content"] = df["Policy_Content"] = df["Policy_Content"].str.lower()
    df["Policy_Content"] = df["Policy_Content"].str.replace('\n', ' ', regex=False)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'<a href.+?>', ' ', regex=True)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'<ul style.+?>', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'<.+?>', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace('&nbsp;', ' ', regex=False)
    df["Policy_Content"] = df["Policy_Content"].str.replace(
        'IEA/IRENA Global Renewable Energy Policies and Measures Database © OECD/IEA and IRENA, [November 2020]', '',
        regex=False)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(source:.+?\)', ' ', regex=True)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(http:.+?\)', ' ', regex=True)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(Reference.+?\)', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(.+?\)', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'\[.+?\]', ' ', regex=True)

    df_iea = df[df['db_source'] == 'IEA']
    df_cp = df[df['db_source'] == 'Climate Policy']
    df_lse = df[df['db_source'] == 'LSE']

    print("================== Nan:  ==================")
    print(df_iea['Policy_Content'].isnull().sum())
    print(df_cp['Policy_Content'].isnull().sum())
    print(df_lse['Policy_Content'].isnull().sum())

    # df_iea.fillna('', inplace=True)
    # df_cp.fillna('', inplace=True)
    # df_lse.fillna('', inplace=True)

    print("================== Average length:  ==================")
    df_iea_policy_content = df_iea['Policy_Content'].fillna('')
    df_cp_policy_content = df_cp['Policy_Content'].fillna('')
    df_lse_policy_content = df_lse['Policy_Content'].fillna('')

    print(np.mean(df_iea_policy_content.apply(lambda x: len(x.split()))))
    print(np.mean(df_cp_policy_content.apply(lambda x: len(x.split()))))
    print(np.mean(df_lse_policy_content.apply(lambda x: len(x.split()))))

    print("================== Length < 10 :  ==================")
    df_iea_short = df_iea_policy_content.apply(lambda x: len(x.split()) < 10).value_counts()
    df_cp_short = df_cp_policy_content.apply(lambda x: len(x.split()) < 10).value_counts()
    df_lse_short = df_lse_policy_content.apply(lambda x: len(x.split()) < 10).value_counts()
    print(df_iea_short)
    print(df_cp_short)
    print(df_lse_short)

    print("================== Length < 10 ratio:  ==================")

    print(df_iea_short / df_iea_short.sum())
    print(df_cp_short / df_cp_short.sum())
    print(df_lse_short / df_lse_short.sum())


def policy_before_fill():
    print("================== Before fill Policy Content:  ==================")
    df = pd.read_excel('policy_db_complete.xlsx', sheet_name='raw_data')
    df = df[['Policy', 'Policy_Content', 'db_source']]
    # df.dropna(subset=['Policy_Content'], inplace=True)
    df["Policy_Content"] = df["Policy_Content"] = df["Policy_Content"].str.lower()
    df["Policy_Content"] = df["Policy_Content"].str.replace('\n', ' ', regex=False)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'<a href.+?>', ' ', regex=True)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'<ul style.+?>', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'<.+?>', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace('&nbsp;', ' ', regex=False)
    df["Policy_Content"] = df["Policy_Content"].str.replace(
        'IEA/IRENA Global Renewable Energy Policies and Measures Database © OECD/IEA and IRENA, [November 2020]', '',
        regex=False)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(source:.+?\)', ' ', regex=True)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(http:.+?\)', ' ', regex=True)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(Reference.+?\)', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(.+?\)', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'\[.+?\]', ' ', regex=True)

    df_iea = df[df['db_source'] == 'IEA']
    df_cp = df[df['db_source'] == 'Climate Policy']
    df_lse = df[df['db_source'] == 'LSE']

    print("================== Nan:  ==================")
    print(df_iea['Policy_Content'].isnull().sum())
    print(df_cp['Policy_Content'].isnull().sum())
    print(df_lse['Policy_Content'].isnull().sum())

    # df_iea.fillna('', inplace=True)
    # df_cp.fillna('', inplace=True)
    # df_lse.fillna('', inplace=True)

    df_iea_policy_content = df_iea['Policy_Content'].fillna('')
    df_cp_policy_content = df_cp['Policy_Content'].fillna('')
    df_lse_policy_content = df_lse['Policy_Content'].fillna('')

    print("================== Average length:  ==================")
    print(np.mean(df_iea_policy_content.apply(lambda x: len(x.split()))))
    print(np.mean(df_cp_policy_content.apply(lambda x: len(x.split()))))
    print(np.mean(df_lse_policy_content.apply(lambda x: len(x.split()))))

    print("================== Length < 10 :  ==================")
    df_iea_short = df_iea_policy_content.apply(lambda x: len(x.split()) < 10).value_counts()
    df_cp_short = df_cp_policy_content.apply(lambda x: len(x.split()) < 10).value_counts()
    df_lse_short = df_lse_policy_content.apply(lambda x: len(x.split()) < 10).value_counts()
    print(df_iea_short)
    print(df_cp_short)
    print(df_lse_short)

    print("================== Length < 10 ratio:  ==================")

    print(df_iea_short / df_iea_short.sum())
    print(df_cp_short / df_cp_short.sum())
    print(df_lse_short / df_lse_short.sum())


if __name__ == '__main__':
    policy_after_fill()
    policy_before_fill()
