import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql


def get_db_connect(host, port, user, password, db, charset='utf8mb4'):
    conn = pymysql.connect(host=host, port=port, user=user, password=password,
                           charset=charset, autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    conn.cursor().execute('CREATE DATABASE IF NOT EXISTS %s;' % db)
    conn.select_db(db)
    return conn


# 读取文件的函数
def get_data(file_name):
    datas = pd.read_excel(file_name)
    datas.fillna("", inplace=True)
    return datas


if __name__ == '__main__':
    # 文件名
    file_name1 = "mysql_Additional_Information.xlsx"
    file_name2 = "mysql_Characteristic.xlsx"
    file_name3 = "mysql_Country_Jurisdiction.xlsx"
    file_name4 = "mysql_Policy.xlsx"
    file_name5 = "mysql_Similarity_Information.xlsx"
    file_name6 = "mysql_Topic.xlsx"
    # file_name7 = "Topic_country_expand_hierarchical_topics.xlsx"

    # 创建表的SQL语句
    sql1 = "CREATE TABLE IF NOT EXISTS Additional_Information (aid BIGINT  , Policy_raw MEDIUMTEXT, Policy_Content_raw MEDIUMTEXT,Year VARCHAR(255),URL TEXT)"
    sql2 = "CREATE TABLE IF NOT EXISTS Characteristic (cid BIGINT, sector VARCHAR(255), objective VARCHAR(255), Instrument TEXT,Policy_Type VARCHAR(255),law_or_strategy TEXT)"
    sql3 = "CREATE TABLE IF NOT EXISTS Country_Jurisdiction (cid BIGINT, ISO_code VARCHAR(255), Jurisdiction VARCHAR(255), IPCC_Region TEXT, Short_name VARCHAR(255), Long_name TEXT, Income_Group VARCHAR(255), WB_Region VARCHAR(255), Annex VARCHAR(255))"
    sql4 = "CREATE TABLE IF NOT EXISTS Policy (id BIGINT  PRIMARY KEY, Policy MEDIUMTEXT, Policy_Content MEDIUMTEXT,Source VARCHAR(255))"
    sql5 = "CREATE TABLE IF NOT EXISTS Similarity_Information (sid BIGINT  , group_policy_number INT, bm25_score_first DOUBLE, bm25_policy_first MEDIUMTEXT, bm25_index_first INT)"
    sql6 = "CREATE TABLE IF NOT EXISTS Topic (tid BIGINT, Topic INT, Topic_Name VARCHAR(255), Top_n_words MEDIUMTEXT, Probability DOUBLE, Representative_document VARCHAR(255))"
    # sql7 = "CREATE TABLE Topic_country_expand_hierarchical_topics (thid BIGINT , Parent_ID INT ,Parent_Name VARCHAR(255),Topics TEXT,Child_Left_ID INT ,Child_Left_Name VARCHAR(255),Child_Right_ID INT,Child_Right_Name  VARCHAR(255),Distance DOUBLE,Child_All TEXT)"

    # 向MySQL插入数据
    sql1_1 = "INSERT IGNORE INTO Additional_Information VALUES(%s,%s,%s,%s,%s)"
    sql1_2 = "INSERT IGNORE INTO Characteristic VALUES(%s,%s,%s,%s,%s,%s)"
    sql1_3 = "INSERT IGNORE INTO Country_Jurisdiction VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql1_4 = "INSERT IGNORE INTO Policy VALUES(%s,%s,%s,%s)"
    sql1_5 = "INSERT IGNORE INTO Similarity_Information VALUES(%s,%s,%s,%s,%s)"
    sql1_6 = "INSERT IGNORE INTO Topic VALUES(%s,%s,%s,%s,%s,%s)"
    # sql1_7 = "insert into Topic_country_expand_hierarchical_topics values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    # 获取数据
    datas1 = get_data(file_name1)
    datas2 = get_data(file_name2)
    datas3 = get_data(file_name3)
    datas4 = get_data(file_name4)
    datas5 = get_data(file_name5)
    datas6 = get_data(file_name6)
    # datas7 = get_data(file_name7)

    # 处理Topic_country_expand_hierarchical_topics.xlsx这张表 合并子节点
    # Child_Left_ID = datas7["Child_Left_ID"].tolist()
    # Child_Right_ID = datas7["Child_Right_ID"].tolist()
    # Child_All = [[str(Child_Left_ID[i]), str(Child_Right_ID[i])] for i in range(len(Child_Left_ID))]
    # datas7["Child_All"] = Child_All

    # 构造插入数据
    data1 = [list(i) for i in datas1.values]
    data2 = [list(i) for i in datas2.values]
    data3 = [list(i) for i in datas3.values]
    data4 = [list(i) for i in datas4.values]
    data5 = [list(i) for i in datas5.values]
    data6 = [list(i) for i in datas6.values]

    # 建立MySQL连接
    conn = get_db_connect(host='localhost', user='zhhuang', password='zhhuang123', port=3306, db='GCCMPD',
                          charset='utf8mb4')
    # conn = get_db_connect(host='localhost', user='zhhuang', password='123', port=3306, db='GCCMPD',
    #                       charset='utf8mb4')
    with conn.cursor() as cursor:
        # 执行SQL语句
        cursor.execute(sql4)
        cursor.execute('alter table Policy convert to character set utf8mb4 collate utf8mb4_bin;')
        cursor.executemany(sql1_4, data4)

        cursor.execute(sql6)
        cursor.execute('alter table Topic add foreign key(tid) REFERENCES Policy(id);')
        cursor.executemany(sql1_6, data6)

        cursor.execute(sql1)
        cursor.execute('alter table Additional_Information convert to character set utf8mb4 collate utf8mb4_bin;')
        cursor.execute('alter table Additional_Information ADD FOREIGN KEY (aid) REFERENCES Policy(id);')
        cursor.executemany(sql1_1, data1)

        cursor.execute(sql2)
        cursor.execute('alter table Characteristic add foreign key(cid) REFERENCES Policy(id);')
        cursor.executemany(sql1_2, data2)

        cursor.execute(sql3)
        cursor.execute('alter table Country_Jurisdiction add foreign key(cid) REFERENCES Policy(id);')
        cursor.executemany(sql1_3, data3)

        cursor.execute(sql5)
        cursor.execute('alter table Similarity_Information convert to character set utf8mb4 collate utf8mb4_bin;')
        cursor.execute('alter table Similarity_Information add foreign key(sid) REFERENCES Policy(id);')
        cursor.executemany(sql1_5, data5)

        # cursor.execute(sql7)
        # cursor.execute(
        #     'alter table Topic_country_expand_hierarchical_topics add foreign key(Child_Left_ID) REFERENCES Topic(Topic);')
        # cursor.executemany(sql1_7, datas7)
