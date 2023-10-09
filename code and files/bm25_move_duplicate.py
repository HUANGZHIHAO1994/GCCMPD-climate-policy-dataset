import pandas as pd
import numpy as np
from gensim.summarization.bm25 import BM25
import os
import sys
import re
from tqdm import tqdm
from nltk import data
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import spacy
import geonamescache

data.path.append(r"/home/zhhuang/climate_policy_paper/code/data/nltk_data")


def gen_dict_extract(var, key):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)


def load_stopwords():
    stopwords = []
    with open('/home/zhhuang/climate_policy_paper/code/data/stopwords.txt', 'r', encoding='utf8') as file:
        for line in file:
            stopwords.append(line.strip())
    return stopwords


def lemmatize(words, wnl: WordNetLemmatizer):
    for word, tag in pos_tag(words):
        if tag.startswith('NN'):
            yield wnl.lemmatize(word, pos='n')
        elif tag.startswith('VB'):
            yield wnl.lemmatize(word, pos='v')
        elif tag.startswith('JJ'):
            yield wnl.lemmatize(word, pos='a')
        elif tag.startswith('R'):
            yield wnl.lemmatize(word, pos='r')
        else:
            yield word


def normalize(texts):
    stopwords = load_stopwords()
    wnl = WordNetLemmatizer()
    processed_texts = []

    bar = tqdm(range(len(texts)), desc='Preprocessing ...', ncols=150)
    for _, text in zip(bar, texts):
        # 1.去除年份和%，如1991-2007，2025，2.5%
        n_text = re.sub(r'(\d{4}(-\d{4})?)|([-+]?\d+(.\d+)?%)', '', text)

        # 2.converting all characters to lowercase 小写
        n_text = n_text.lower()

        # 3.stopwords 停用词 (包含punctuation and symbols 标点和符号)
        words = [word for word in word_tokenize(n_text) if word not in stopwords]

        # 4.lemmatization 词形还原
        words = list(lemmatize(words, wnl))

        # 5.geo
        geo = []
        doc = nlp(' '.join(words))
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                if ent.text in cities:
                    pass
                else:
                    geo.append(ent.text)
            elif ent.label_ in ['DATE', 'TIME']:
                geo.append(ent.text)
        words = ' '.join(words)
        if geo:
            for g in geo:
                words = words.replace(g, '')

        processed_texts.append(words)

    return processed_texts


def get_data():
    data_result = pd.read_excel("results.xlsx")
    return data_result


def get_bm25_score(top_ratio):
    iea_cp_cclw_column = ['Year', 'Jurisdiction_standard_amend', 'db_source', 'Policy', 'ISO_code']
    column = ['Year', 'Scope', 'Source', 'Policy', 'ISO_code']
    iea_cp_cclw_df = pd.read_excel("/home/zhhuang/climate_policy_paper/code/files/policy_db_complete.xlsx",
                                   sheet_name="raw_data")
    iea_cp_cclw_df = iea_cp_cclw_df[iea_cp_cclw_column]
    iea_cp_cclw_df = iea_cp_cclw_df.rename(
        columns={"Source": 'URL', 'db_source': "Source", 'Jurisdiction_standard_amend': "Scope"})

    df_docs = pd.read_excel("results.xlsx")
    df_docs = df_docs.drop(df_docs[df_docs["Source"].isin(["IEA", "Climate Policy", "LSE"])].index)
    df_docs = df_docs[column]
    df_all = pd.concat([iea_cp_cclw_df, df_docs])
    # print(df.info())

    bm25_matrix = np.zeros((len(df_all["Policy"]), len(df_all["Policy"])))
    policy_list = normalize(df_all["Policy"].tolist())
    policy_list_raw = df_all["Policy"].tolist()
    tokenized_policy_list = [doc.split(" ") for doc in policy_list]

    # gensim
    bm25 = BM25(tokenized_policy_list)

    bar = tqdm(range(len(df_all)), desc='BM25 Matrix', ncols=150)
    for _, num_row in zip(bar, df_all.iterrows()):
        num, row = num_row
        tokenized_query = policy_list[num].split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        bm25_matrix[num] = doc_scores

    grouped = df_all.groupby(["Year", "ISO_code", "Scope"])["Policy"]

    group_policy_number = np.zeros(len(df_all["Policy"]))
    bm25_score_first = np.zeros(len(df_all["Policy"]))
    bm25_index_first = np.zeros(len(df_all["Policy"]))
    bm25_policy_first = np.empty(len(df_all["Policy"]), dtype=object)

    # ========= bm25_score_first =========
    bar = tqdm(range(len(grouped.indices)), desc='BM25 Group Dedup', ncols=150)

    for _, name_index in zip(bar, grouped.indices.items()):
        name, index = name_index
        if len(index) == 1:
            group_policy_number[index] = 1

        elif len(index) == 2:
            group_policy_number[index] = 2
            for num, idx in enumerate(index):
                scores = bm25_matrix[idx]
                other_policy_index = np.delete(index, num)
                other_policy_scores = scores[other_policy_index]
                sort_score_index = np.argsort(other_policy_scores)[::-1]
                # print(other_policy_index)
                # print(other_policy_scores)

                bm25_score_first[idx] = other_policy_scores[sort_score_index[0]]
                bm25_policy_first[idx] = policy_list_raw[other_policy_index[sort_score_index[0]]]
                bm25_index_first[idx] = other_policy_index[sort_score_index[0]]

                # del_temp = []
                # for opi_idx, i in enumerate(other_policy_index):
                #     if i in delete_list:
                #         del_temp.append(opi_idx)
                # other_policy_index = np.delete(other_policy_index, del_temp)
                # if len(other_policy_index) > 0:
                #
                #     # print(bm25_policy_first)
                #     if np.max(scores[other_policy_index]) > BM25_experience_judgment:
                #         delete_list.append(idx)

        else:
            group_policy_number[index] = len(index)

            for num, idx in enumerate(index):
                scores = bm25_matrix[idx]
                other_policy_index = np.delete(index, num)
                other_policy_scores = scores[other_policy_index]
                sort_score_index = np.argsort(other_policy_scores)[::-1]
                # print(other_policy_index[sort_score_index[0]])
                # print(policy_list[other_policy_index[sort_score_index[0]]])

                bm25_score_first[idx] = other_policy_scores[sort_score_index[0]]
                bm25_policy_first[idx] = policy_list_raw[other_policy_index[sort_score_index[0]]]
                bm25_index_first[idx] = other_policy_index[sort_score_index[0]]

                # del_temp = []
                # for opi_idx, i in enumerate(other_policy_index):
                #     if i in delete_list:
                #         del_temp.append(opi_idx)
                # other_policy_index = np.delete(other_policy_index, del_temp)
                # if len(other_policy_index) > 0:
                #
                #     # print(bm25_policy_first)
                #     if np.max(scores[other_policy_index]) > BM25_experience_judgment:
                #         delete_list.append(idx)

    df_all["group_policy_number"] = group_policy_number
    df_all["bm25_score_first"] = bm25_score_first
    df_all["bm25_policy_first"] = bm25_policy_first
    df_all["bm25_index_first"] = bm25_index_first

    with pd.ExcelWriter("/home/zhhuang/climate_policy_paper/code/data/bm25_score_move_duplicate_result.xlsx",
                        engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        df_all.to_excel(writer, index=False, sheet_name="bm25_score")

    # save(df, delete_list, BM25_experience_judgment)

    # ratio = 4107
    df_bm25 = df_all[df_all["Source"].isin(["IEA", "Climate Policy", "LSE"])]
    bm25_scr_list = df_bm25["bm25_score_first"].to_list()
    bm25_scr_list.sort()
    # ratio = int(4107 / 13298 * len(df_bm25["bm25_score_first"].to_list()))
    # iea_cp_lse_length = len(data[data["Scope"].isin(['IEA', 'Climate Policy', 'LSE'])])
    # print(bm25_scr_list[::-1])
    bm25_score = bm25_scr_list[::-1][top_ratio - 1]
    return bm25_score


def save(df_result, del_list, score):
    dup = df_result.loc[del_list, :]
    all_policy_dedup = df_result.drop(del_list)
    try:
        dup.rename(columns={"Unnamed: 0": "Index"}, inplace=True)
        all_policy_dedup.rename(columns={"Unnamed: 0": "Index"}, inplace=True)
        df_result.rename(columns={"Unnamed: 0": "Index"}, inplace=True)
    except:
        pass

    with pd.ExcelWriter("/home/zhhuang/climate_policy_paper/code/data/bm25_{}_move_duplicate_result.xlsx".format(
            score), engine='xlsxwriter',
            engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        df_result.to_excel(writer, index=False, sheet_name="data_before_dedup")
        all_policy_dedup.to_excel(writer, index=False, sheet_name="all_policies_dedup")
        dup.to_excel(writer, index=False, sheet_name="dup")


if __name__ == '__main__':
    nlp = spacy.load("en_core_web_trf")

    gc = geonamescache.GeonamesCache()

    # gets nested dictionary for countries
    countries = gc.get_countries()

    # gets nested dictionary for cities
    cities = gc.get_cities()

    cities = [*gen_dict_extract(cities, 'name')]
    countries = [*gen_dict_extract(countries, 'name')]

    # BM25_experience_judgment = get_bm25_score(6061)
    BM25_experience_judgment = 17.231989221158145

    df = get_data()
    # print(df.info())

    # ========= bm25_matrix =========
    bm25_matrix = np.zeros((len(df["Policy"]), len(df["Policy"])))
    policy_list = normalize(df["Policy"].tolist())
    policy_list_raw = df["Policy"].tolist()
    tokenized_policy_list = [doc.split(" ") for doc in policy_list]

    # gensim
    bm25 = BM25(tokenized_policy_list)

    bar = tqdm(range(len(df)), desc='BM25 Matrix', ncols=150)
    for _, num_row in zip(bar, df.iterrows()):
        num, row = num_row
        tokenized_query = policy_list[num].split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        bm25_matrix[num] = doc_scores

    grouped = df.groupby(["Year", "ISO_code", "Scope"])["Policy"]

    group_policy_number = np.zeros(len(df["Policy"]))
    bm25_score_first = np.zeros(len(df["Policy"]))
    bm25_index_first = np.zeros(len(df["Policy"]))
    bm25_policy_first = np.empty(len(df["Policy"]), dtype=object)

    # print(grouped.indices)
    # print(type(grouped.indices))

    delete_list = []
    bar = tqdm(range(len(grouped.indices)), desc='BM25 Group Dedup', ncols=150)

    for _, name_index in zip(bar, grouped.indices.items()):
        name, index = name_index
        index = index[::-1]
        if len(index) == 1:
            group_policy_number[index] = 1

        elif len(index) == 2:
            group_policy_number[index] = 2
            for num, idx in enumerate(index):
                scores = bm25_matrix[idx]
                other_policy_index = np.delete(index, num)
                other_policy_scores = scores[other_policy_index]
                sort_score_index = np.argsort(other_policy_scores)[::-1]
                # print(other_policy_index)
                # print(other_policy_scores)

                bm25_score_first[idx] = other_policy_scores[sort_score_index[0]]
                bm25_policy_first[idx] = policy_list_raw[other_policy_index[sort_score_index[0]]]
                bm25_index_first[idx] = other_policy_index[sort_score_index[0]]

                del_temp = []
                for opi_idx, i in enumerate(other_policy_index):
                    if i in delete_list:
                        del_temp.append(opi_idx)
                other_policy_index = np.delete(other_policy_index, del_temp)
                if len(other_policy_index) > 0:

                    # print(bm25_policy_first)
                    if np.max(scores[other_policy_index]) > BM25_experience_judgment:
                        delete_list.append(idx)

        else:
            group_policy_number[index] = len(index)

            for num, idx in enumerate(index):
                scores = bm25_matrix[idx]
                other_policy_index = np.delete(index, num)
                other_policy_scores = scores[other_policy_index]
                sort_score_index = np.argsort(other_policy_scores)[::-1]
                # print(other_policy_index[sort_score_index[0]])
                # print(policy_list[other_policy_index[sort_score_index[0]]])

                bm25_score_first[idx] = other_policy_scores[sort_score_index[0]]
                bm25_policy_first[idx] = policy_list_raw[other_policy_index[sort_score_index[0]]]
                bm25_index_first[idx] = other_policy_index[sort_score_index[0]]

                del_temp = []
                for opi_idx, i in enumerate(other_policy_index):
                    if i in delete_list:
                        del_temp.append(opi_idx)
                other_policy_index = np.delete(other_policy_index, del_temp)
                if len(other_policy_index) > 0:

                    # print(bm25_policy_first)
                    if np.max(scores[other_policy_index]) > BM25_experience_judgment:
                        delete_list.append(idx)

    df["group_policy_number"] = group_policy_number
    df["bm25_score_first"] = bm25_score_first
    df["bm25_policy_first"] = bm25_policy_first
    df["bm25_index_first"] = bm25_index_first

    save(df, delete_list, BM25_experience_judgment)
