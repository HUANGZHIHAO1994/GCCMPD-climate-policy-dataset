import pandas as pd
import numpy as np


def get_data():
    df = pd.read_excel("iea.xlsx")
    return df


def data_process(df):
    # 先过滤出LearnMore中有（in Chinese）和analisis的数据
    # http://www.mineco.es/
    first_filter = df[df['LearnMore'].apply(lambda x: x not in ["(in Chinese)", "analisis", np.nan])]
    print(first_filter.info())

    # 按照LearnMore, Country, Year, Jurisdiction进行分组 并拼接指定字段的数据 默认是拼接到第一条
    second_filter = first_filter.groupby(["LearnMore", "Country", "Year", "Jurisdiction", "Policy"])["Topics"].apply(
        lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_2 = first_filter.groupby(["LearnMore", "Country", "Year", "Jurisdiction", "Policy"])["Type"].apply(
        lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_3 = first_filter.groupby(["LearnMore", "Country", "Year", "Jurisdiction", "Policy"])["Sectors"].apply(
        lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_4 = first_filter.groupby(["LearnMore", "Country", "Year", "Jurisdiction", "Policy"])[
        "Technologies"].apply(
        lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_5 = first_filter.groupby(["LearnMore", "Country", "Year", "Jurisdiction", "Policy"])[
        "Policy_Content"].apply(
        lambda x: "\n".join(set(x.str.cat(sep="¥¥").split("¥¥")))).reset_index()
    # second_filter_6 = first_filter.groupby(["LearnMore", "Country", "Year", "Jurisdiction"])["Policy"].apply(
    #     lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter["Type"] = second_filter_2["Type"]
    second_filter["Sectors"] = second_filter_3["Sectors"]
    second_filter["Technologies"] = second_filter_4["Technologies"]
    second_filter["Policy_Content"] = second_filter_5["Policy_Content"]
    # second_filter["Policy"] = second_filter_6["Policy"]
    # print(second_filter.info())

    # 去重LearnMore, Country, Year, Jurisdiction保留第一条数据
    third_filter = first_filter.drop_duplicates(subset=["LearnMore", "Country", "Year", "Jurisdiction", "Policy"],
                                                keep="first")
    # print(third_filter.info())

    # 删除去重后数据的"Topics","Type","Sectors","Technologies","Policy_Content"列数据数据
    fourth_filter = third_filter.drop(["Topics", "Type", "Sectors", "Technologies", "Policy_Content"], axis=1)

    # print(fourth_filter)
    # 以"LearnMore", "Country", "Year", "Jurisdiction"为键进行合并数据
    five_filter = pd.merge(second_filter, fourth_filter, on=["LearnMore", "Country", "Year", "Jurisdiction", "Policy"])
    # 和并之前过滤的掉的数据
    six_filter = df[df['LearnMore'].apply(lambda x: x in ["(in Chinese)", "analisis", np.nan])]
    result_filter = pd.concat([five_filter, six_filter])
    # print(len(result_filter))

    # 输出
    result_filter.to_excel('iea_dedup_result.xlsx', index=False)


if __name__ == '__main__':
    df = get_data()
    print(len(df))
    data_process(df)
