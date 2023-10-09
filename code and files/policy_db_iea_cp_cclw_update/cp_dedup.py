import pandas as pd
import numpy as np
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_data():
    data = pd.read_csv("cp.csv")
    return data


def data_process(df):
    df["Date of decision"].fillna(0, inplace=True)
    df["Start date of implementation"].fillna(0, inplace=True)
    df.fillna('', inplace=True)
    date_list = [''] * len(df["Date of decision"].to_list())
    for num, row in df.iterrows():
        if row["Date of decision"]:
            date_list[num] = row["Date of decision"]
        else:
            date_list[num] = row["Start date of implementation"]
    df["Date of decision"] = date_list
    # group by "Country ISO", "Date of decision", "Jurisdiction", "Policy name" 
    # then concat specified field like "Type of policy instrument" to the first data
    second_filter = \
        df.groupby(["Country ISO", "Date of decision", "Jurisdiction", "Policy name"])[
            "Type of policy instrument"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_2 = \
        df.groupby(["Country ISO", "Date of decision", "Jurisdiction", "Policy name"])[
            "Sector name"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_3 = \
        df.groupby(["Country ISO", "Date of decision", "Jurisdiction", "Policy name"])[
            "Policy description"].apply(lambda x: "\n".join(set(x.str.cat(sep="¥¥").split("¥¥")))).reset_index()
    second_filter_4 = \
        df.groupby(["Country ISO", "Date of decision", "Jurisdiction", "Policy name"])[
            "Policy type"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter_5 = \
        df.groupby(["Country ISO", "Date of decision", "Jurisdiction", "Policy name"])[
            "Policy objective"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    # second_filter_6 = df.groupby(["Country ISO", "Date of decision", "Jurisdiction"])[
    #     "Policy name"].apply(lambda x: ";".join(set(x.str.cat(sep=";").split(";")))).reset_index()
    second_filter["Sector name"] = second_filter_2["Sector name"]
    second_filter["Policy description"] = second_filter_3["Policy description"]
    second_filter["Policy type"] = second_filter_4["Policy type"]
    second_filter["Policy objective"] = second_filter_5["Policy objective"]
    # second_filter["Policy name"] = second_filter_6["Policy name"]
    # print(df.info())

    # drop_duplicates by "Country ISO", "Date of decision", "Jurisdiction", "Policy name"
    third_filter = df.drop_duplicates(
        subset=["Country ISO", "Date of decision", "Jurisdiction", "Policy name"],
        keep="first")

    fourth_filter = third_filter.drop(
        ["Type of policy instrument", "Sector name", "Policy description", "Policy type", "Policy objective"], axis=1)

    # merge by "Country ISO", "Date of decision", "Jurisdiction", "Policy name"
    result_filter = pd.merge(second_filter, fourth_filter,
                             on=["Country ISO", "Date of decision", "Jurisdiction", "Policy name"])

    result_filter.to_excel('cp_dedup_result.xlsx', index=False)

    with open("dup_statistic.txt", 'a') as f:
        f.write("Climate Policy Raw: " + str(len(df)) + '\n')
        f.write("Climate Policy After cp_dedup.py: " + str(len(result_filter)) + '\n')
        f.write("Climate Policy first dup: " + str(len(df) - len(result_filter)) + '\n')
        f.write('\n')


if __name__ == '__main__':
    pd.set_option('display.max_columns', 4)
    cp_df = get_data()
    print(len(cp_df))
    data_process(cp_df)
