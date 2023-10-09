from openpyxl import load_workbook
import os
from pymongo.errors import DuplicateKeyError
import pymongo
import json
import pandas as pd


def df2bson(df):
    """DataFrame类型转化为Bson类型"""

    data = json.loads(df.T.to_json()).values()
    return data


def database(df_data, s):
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    # client.admin.authenticate('root', '123456')
    db = client["ClimatePolicy"]
    col = db[s]

    bson_data = df2bson(df_data)

    result = col.insert_many(bson_data)


# # 连接mongodb
# uri = "mongodb://127.0.0.1:27017"
# client = pymongo.MongoClient(uri)
#
# db = client["ClimatePolicy"]


def insert_mongo(fileName):
    df = pd.read_excel(fileName)

    # 插入数据
    collection_name = fileName.split("/")[-1].split(".")[0]
    database(df, collection_name)


if __name__ == '__main__':
    # 获取excel文件的路径及文件名
    miti = "/home/zhhuang/climate_policy_paper/code/data/all_policies_mitigation_result.xlsx"
    adapt = "/home/zhhuang/climate_policy_paper/code/data/all_policies_adaptation_result.xlsx"
    topics = ["/home/zhhuang/climate_policy_paper/code/data/Topic.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_iea_cp_cclw.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_country_expand.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_except_ecolex.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_hierarchical_topics.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_hierarchical_topics_except_ecolex.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_country_expand_hierarchical_topics.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_iea_cp_cclw_hierarchical_topics.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_country_expand_topics_over_time.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_except_ecolex_topics_over_time.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_iea_cp_cclw_topics_over_time.xlsx",
              "/home/zhhuang/climate_policy_paper/code/data/Topic_topics_over_time.xlsx"]
    for f in [miti, adapt] + topics:
        insert_mongo(f)
