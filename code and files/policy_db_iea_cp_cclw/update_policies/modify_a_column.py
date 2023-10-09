import pandas as pd
import numpy as np

# 把(2)的指定字段改到(1)上形成(3)
# bm25_result (1).xlsx: 需修改的文件(某字段【老】版本文件 "all_policies_dedup")
# bm25_result (2).xlsx: 修改来源文件(某字段【新】版本文件 "raw_data")
# bm25_result (3).xlsx: 输出

# 读取文件
df_1 = pd.read_excel("bm25_result (1).xlsx", sheet_name="all_policies_dedup")
df_2 = pd.read_excel("bm25_result (2).xlsx")

# 修改列名
df_1.rename(columns={"A": "Index"}, inplace=True)
df_2.rename(columns={"A": "Index"}, inplace=True)
# df_1.rename(columns={"Unnamed: 0": "Index"}, inplace=True)
# df_2.rename(columns={"Unnamed: 0": "Index"}, inplace=True)

# dict_2 = df_2.loc[:, ["Index", "Policy_Content"]].to_dict(orient="records")
# dict_2 = df_2.loc[:, ["Index", "Instrument"]].to_dict(orient="records")
dict_2 = df_2.loc[:, ["Index", "Sector-Instrument"]].to_dict(orient="records")
# dict_2 = df_2.loc[:, ["Index", "sector"]].to_dict(orient="records")
# dict_2 = df_2.loc[:, ["Index", "subsector"]].to_dict(orient="records")
# dict_2 = df_2.loc[:, ["Index", "objective"]].to_dict(orient="records")
# dict_2 = df_2.loc[:, ["Index", "subobjective"]].to_dict(orient="records")
# dict_2 = df_2.loc[:, ["Index", "law or strategy"]].to_dict(orient="records")
# dict_2 = df_2.loc[:, ["Index", "Policy Type"]].to_dict(orient="records")
# print(dict_2)

# dict_1 = df_1.loc[:, ["Index", "Policy_Content"]].to_dict(orient="records")
# dict_1 = df_1.loc[:, ["Index", "Instrument"]].to_dict(orient="records")
dict_1 = df_1.loc[:, ["Index", "Sector-Instrument"]].to_dict(orient="records")
# dict_1 = df_1.loc[:, ["Index", "sector"]].to_dict(orient="records")
# dict_1 = df_1.loc[:, ["Index", "subsector"]].to_dict(orient="records")
# dict_1 = df_1.loc[:, ["Index", "objective"]].to_dict(orient="records")
# dict_1 = df_1.loc[:, ["Index", "subobjective"]].to_dict(orient="records")
# dict_1 = df_1.loc[:, ["Index", "law or strategy"]].to_dict(orient="records")
# dict_1 = df_1.loc[:, ["Index", "Policy Type"]].to_dict(orient="records")

# 从df_2提取A列表
A_list_2 = [i["Index"] for i in dict_2]
# 构造df_2的字典 字典A为键 Policy_Content为值
# A_Policy_Content_dict_2 = {i["Index"]: i["Instrument"] for i in dict_2}
A_Policy_Content_dict_2 = {i["Index"]: i["Sector-Instrument"] for i in dict_2}
# A_Policy_Content_dict_2 = {i["Index"]: i["sector"] for i in dict_2}
# A_Policy_Content_dict_2 = {i["Index"]: i["subsector"] for i in dict_2}
# A_Policy_Content_dict_2 = {i["Index"]: i["objective"] for i in dict_2}
# A_Policy_Content_dict_2 = {i["Index"]: i["subobjective"] for i in dict_2}
# A_Policy_Content_dict_2 = {i["Index"]: i["law or strategy"] for i in dict_2}
# A_Policy_Content_dict_2 = {i["Index"]: i["Policy Type"] for i in dict_2}
# A_Policy_Content_dict_2 = {i["Index"]: i["Policy_Content"] for i in dict_2}

# 构造df_1的字典 构造字典A为键 Policy_Content为值
# A_Policy_Content_dict_1 = {i["Index"]: i["Policy_Content"] for i in dict_1}
# A_Policy_Content_dict_1 = {i["Index"]: i["Instrument"] for i in dict_1}
A_Policy_Content_dict_1 = {i["Index"]: i["Sector-Instrument"] for i in dict_1}
# A_Policy_Content_dict_1 = {i["Index"]: i["sector"] for i in dict_1}
# A_Policy_Content_dict_1 = {i["Index"]: i["subsector"] for i in dict_1}
# A_Policy_Content_dict_1 = {i["Index"]: i["objective"] for i in dict_1}
# A_Policy_Content_dict_1 = {i["Index"]: i["subobjective"] for i in dict_1}
# A_Policy_Content_dict_1 = {i["Index"]: i["law or strategy"] for i in dict_1}
# A_Policy_Content_dict_1 = {i["Index"]: i["Policy Type"] for i in dict_1}

# 如果df_1的A在df_2的A的列表里 那就以A为键取A_Policy_Content_dict_2的值
# 如果不在就取以A为键取A_Policy_Content_dict_1的值
# df_Policy_Content_1 = df_1["Index"].apply(
#     lambda x: A_Policy_Content_dict_2[x] if x in A_list_2 else A_Policy_Content_dict_1[x])

df_Policy_Content_1 = df_1["Index"].apply(
    lambda x: A_Policy_Content_dict_2[x])

# df_1["Policy_Content"] = df_Policy_Content_1
# df_1["Instrument"] = df_Policy_Content_1
df_1["Sector-Instrument"] = df_Policy_Content_1
# df_1["sector"] = df_Policy_Content_1
# df_1["subsector"] = df_Policy_Content_1
# df_1["objective"] = df_Policy_Content_1
# df_1["subobjective"] = df_Policy_Content_1
# df_1["law or strategy"] = df_Policy_Content_1
# df_1["Policy Type"] = df_Policy_Content_1

# df_dup = pd.read_excel("bm25_result (1).xlsx", sheet_name="dup")
# df_dup["dup_source"].fillna("", inplace=True)

# 保存文件
file_path = pd.ExcelWriter('bm25_result (3).xlsx')
df_1.to_excel(file_path, 'all_policies_dedup', encoding='utf-8', index=False)
file_path.save()
