import pandas as pd
import numpy as np


def get_data():
    df = pd.read_csv("cp.csv")
    return df


def data_process(df):
    first_filter = df[df["Source or references"].apply(lambda x: x not in [np.nan])]
    # print(first_filter.info())
    # 按照"Type of policy instrument","Sector name","Policy description","Policy type","Policy stringency","Policy objective"进行分组 并拼接指定字段的数据 默认是拼接到第一条
    second_filter = \
        first_filter.groupby(["Source or references", "Country", "Date of decision", "Jurisdiction", "Policy Title"])[
            "Type of policy instrument"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_2 = \
        first_filter.groupby(["Source or references", "Country", "Date of decision", "Jurisdiction", "Policy Title"])[
            "Sector name"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_3 = \
        first_filter.groupby(["Source or references", "Country", "Date of decision", "Jurisdiction", "Policy Title"])[
            "Policy description"].apply(lambda x: "\n".join(set(x.str.cat(sep="¥¥").split("¥¥")))).reset_index()
    second_filter_4 = \
        first_filter.groupby(["Source or references", "Country", "Date of decision", "Jurisdiction", "Policy Title"])[
            "Policy type"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_5 = \
        first_filter.groupby(["Source or references", "Country", "Date of decision", "Jurisdiction", "Policy Title"])[
            "Policy objective"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    # second_filter_6 = first_filter.groupby(["Source or references", "Country", "Date of decision", "Jurisdiction"])[
    #     "Policy Title"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter["Sector name"] = second_filter_2["Sector name"]
    second_filter["Policy description"] = second_filter_3["Policy description"]
    second_filter["Policy type"] = second_filter_4["Policy type"]
    second_filter["Policy objective"] = second_filter_5["Policy objective"]
    # second_filter["Policy Title"] = second_filter_6["Policy Title"]
    # print(first_filter.info())

    # 去重"Type of policy instrument","Sector name","Policy description","Policy type","Policy stringency","Policy objective"保留第一条数据
    third_filter = first_filter.drop_duplicates(
        subset=["Source or references", "Country", "Date of decision", "Jurisdiction", "Policy Title"],
        keep="first")

    # 删除去重后数据的"Type of policy instrument","Sector name","Policy description","Policy type","Policy stringency","Policy objective"列数据数据
    fourth_filter = third_filter.drop(
        ["Type of policy instrument", "Sector name", "Policy description", "Policy type", "Policy objective"], axis=1)

    # 以"Type of policy instrument","Sector name","Policy description","Policy type","Policy stringency","Policy objective"为键进行合并数据
    five_filter = pd.merge(second_filter, fourth_filter,
                           on=["Source or references", "Country", "Date of decision", "Jurisdiction", "Policy Title"])

    six_filter = df[df["Source or references"].apply(lambda x: x in [np.nan])]
    result_filter = pd.concat([five_filter, six_filter])
    print(len(result_filter))
    # 指定生成的Excel表格名称
    file_path = pd.ExcelWriter('cp_dedup_result.xlsx')
    # 输出
    result_filter.to_excel(file_path, index=False)
    # 保存表格
    file_path.save()


if __name__ == '__main__':
    df = get_data()
    print(len(df))
    data_process(df)
