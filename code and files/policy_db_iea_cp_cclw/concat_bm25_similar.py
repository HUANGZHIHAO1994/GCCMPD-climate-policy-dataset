import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
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

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


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
    data = pd.read_excel("policy_concat_mitigation_result.xlsx")
    return data


def data_process(data):
    new_df = data.copy()
    jurisdiction_map = {"City/Municipal": "SubNational", "State/Provincial": "SubNational",
                        "Regional": "Subnational region", "Subnational region": "Subnational region",
                        "City": "SubNational", "Country": "National", "National": "National",
                        "Supranational region": "International", "International": "International"}
    new_df["Jurisdiction"].fillna("Unknown", inplace=True)
    new_df["Jurisdiction_standard"] = new_df.loc[:, "Jurisdiction"].apply(
        lambda x: jurisdiction_map[x] if not x == "Unknown" else x)
    new_df["Year"].fillna(0, inplace=True)
    new_df["Year"] = new_df["Year"].apply(lambda x: int(x))
    new_df["ISO_code"].fillna("", inplace=True)
    return new_df


def save(data):
    data.sort_values(by=['bm25_score_first', 'bm25_score_second'], ascending=False, inplace=True)
    # df.to_excel("bm25_result.xlsx", encoding='utf-8', index=False)
    with pd.ExcelWriter("bm25_result.xlsx") as writer:
        data.to_excel(writer)


if __name__ == '__main__':
    nlp = spacy.load("en_core_web_trf")

    gc = geonamescache.GeonamesCache()

    # gets nested dictionary for countries
    countries = gc.get_countries()

    # gets nested dictionary for cities
    cities = gc.get_cities()

    cities = [*gen_dict_extract(cities, 'name')]
    countries = [*gen_dict_extract(countries, 'name')]

    df = get_data()
    # print(df.info())
    df = data_process(df)

    bm25_matrix = np.zeros((len(df["Policy"]), len(df["Policy"])))
    policy_list = normalize(df["Policy"].tolist())
    policy_list_raw = df["Policy"].tolist()
    tokenized_policy_list = [doc.split(" ") for doc in policy_list]

    # rank_bm25
    # bm25 = BM25Okapi(tokenized_policy_list)

    # gensim
    bm25 = BM25(tokenized_policy_list)

    bar = tqdm(range(len(df)), desc='BM25 Matrix', ncols=150)
    for _, num_row in zip(bar, df.iterrows()):
        num, row = num_row
        tokenized_query = policy_list[num].split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        bm25_matrix[num] = doc_scores

    # df_simi = pd.DataFrame(bm25_matrix, index=policy_list, columns=policy_list)
    # print(df_simi)
    # with pd.ExcelWriter("bm25_matrix_result.xlsx") as writer:
    #     df_simi.to_excel(writer)
    # np.savetxt('bm25_matrix.txt', bm25_matrix, delimiter=',')

    grouped = df.groupby(["Year", "ISO_code", "Jurisdiction_standard"])["Policy"]

    group_policy_number = np.zeros(len(df["Policy"]))
    bm25_score_first = np.zeros(len(df["Policy"]))
    bm25_score_second = np.zeros(len(df["Policy"]))
    bm25_index_first = np.zeros(len(df["Policy"]))
    bm25_index_second = np.zeros(len(df["Policy"]))
    bm25_policy_first = np.empty(len(df["Policy"]), dtype=object)
    bm25_policy_second = np.empty(len(df["Policy"]), dtype=object)

    # print(grouped.indices)
    # print(type(grouped.indices))
    for name, index in grouped.indices.items():
        if len(index) == 1:
            group_policy_number[index] = 1
            bm25_score_first[index] = -9999999
            bm25_score_second[index] = -9999999
            bm25_policy_first[index] = ''
            bm25_policy_second[index] = ''
            bm25_index_first[index] = -9999999
            bm25_index_second[index] = -9999999
        elif len(index) == 2:
            group_policy_number[index] = 2
            bm25_score_second[index] = -9999999
            bm25_index_second[index] = -9999999
            bm25_policy_second[index] = ''
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
                bm25_score_second[idx] = other_policy_scores[sort_score_index[1]]
                bm25_policy_second[idx] = policy_list_raw[other_policy_index[sort_score_index[1]]]
                bm25_index_first[idx] = other_policy_index[sort_score_index[0]]
                bm25_index_second[idx] = other_policy_index[sort_score_index[1]]
                # print(bm25_policy_first)

    df["group_policy_number"] = group_policy_number
    df["bm25_score_first"] = bm25_score_first
    df["bm25_score_second"] = bm25_score_second
    df["bm25_policy_first"] = bm25_policy_first
    df["bm25_index_first"] = bm25_index_first
    df["bm25_policy_second"] = bm25_policy_second
    df["bm25_index_second"] = bm25_index_second

    save(df)
