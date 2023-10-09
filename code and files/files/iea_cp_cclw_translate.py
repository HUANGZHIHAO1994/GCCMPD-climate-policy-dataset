import re
import html
from urllib import parse
import requests
import pandas as pd
import time
import math
import os
from tqdm import tqdm

GOOGLE_TRANSLATE_URL = 'http://translate.google.com/m?q=%s&tl=%s&sl=%s'


def translate(text, to_language="auto", text_language="auto"):
    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text, to_language, text_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        return ""

    return html.unescape(result[0])


def load_csv(filename):
    data = pd.read_csv('./{}.csv'.format(filename))
    data.fillna("", inplace=True)
    # print(data.head())
    # print(data.info())
    return data


def split_text(text, length):
    text_list = []
    group_num = len(text) / int(length)
    group_num = math.ceil(group_num)  # 向上取整
    for i in range(group_num):
        tmp = text[i * int(length):i * int(length) + int(length)]
        # print(tmp)
        text_list.append(tmp)
    return text_list


def cut_df(file_name, n):
    df = pd.read_excel(file_name, sheet_name="all_policies_dedup")
    df_num = len(df)
    every_epoch_num = math.floor((df_num / n))
    for index in tqdm(range(n)):
        file_name = f'./iea_cp_cclw_{index}.csv'
        if index < n - 1:
            df_tem = df[every_epoch_num * index: every_epoch_num * (index + 1)]
        else:
            df_tem = df[every_epoch_num * index:]
        df_tem.to_csv(file_name, index=False)


if __name__ == '__main__':
    os.chdir('/content/drive/MyDrive/google_translate/files')
    # cut_df("iea_cp_cclw.xlsx", 10)
    iea_cp_cclw = []
    for i in range(0, 10):
        iea_cp_cclw.append("iea_cp_cclw_{}".format(i))
    db = iea_cp_cclw
    # for fn in db:
    for fn in iea_cp_cclw[9:]:
        df = load_csv(fn)
        policy_raw = df["Policy"].tolist()
        policy_content_raw = df["Policy_Content"].tolist()

        policy_en = []
        policy_content_en = []
        for index, policy in enumerate(policy_raw):
            if index % 500 == 0:
                print(fn, index)
            if policy:
                policy_en.append(translate(policy, to_language="en"))
            else:
                policy_en.append("")
            # time.sleep(0.2)
        # print(policy_en)
        for index, policy_content in enumerate(policy_content_raw):
            if index % 500 == 0:
                print(fn, index)
            if policy_content:
                if "：[大][中][小][打印]" in policy_content:
                    policy_content = policy_content.split("：[大][中][小][打印]")[0]
                    policy_content_raw[index] = policy_content
                if len(policy_content) >= 1000:
                    policy_content_tmp = ''
                    for i in split_text(policy_content, 1000):
                        policy_content_tmp += translate(i, to_language="en")
                    policy_content_en.append(policy_content_tmp)
                else:
                    policy_content_en.append(translate(policy_content, to_language="en"))
            else:
                policy_content_en.append("")
            # time.sleep(0.2)
        # print(policy_content_en)

        df = df.rename(columns={"Policy": "Policy_raw", "Policy_Content": "Policy_Content_raw"})
        df["Policy_Content_raw"] = policy_content_raw
        df["Policy"] = policy_en
        df["Policy_Content"] = policy_content_en

        df.to_excel('./{}_EN.xlsx'.format(fn), index=False)

        # print(os.listdir())

        # file_path = pd.ExcelWriter('./files/{}_EN.xlsx'.format(fn))
        # df.to_excel(file_path, encoding='utf-8', index=False)
        # file_path.save()
