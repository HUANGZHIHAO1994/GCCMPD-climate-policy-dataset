import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
from gensim.summarization.bm25 import BM25
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_data():
    data = pd.read_excel("policy_concat_mitigation_result.xlsx")
    return data


def data_process(data):
    new_df = data.copy()
    jurisdiction_map = {"City/Municipal": "SubNational", "State/Provincial": "SubNational",
                        "Regional": "Subnational region", "Subnational region": "Subnational region",
                        "City": "SubNational", "Country": "National", "National": "National",
                        "Supranational region": "International", "International": "International", "Other": "Unknown"}
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
    df = get_data()
    # print(df.info())
    df = data_process(df)

    bm25_matrix = np.zeros((len(df["Policy"]), len(df["Policy"])))
    policy_list = df["Policy"].tolist()
    tokenized_policy_list = [doc.split(" ") for doc in policy_list]

    # rank_bm25
    # bm25 = BM25Okapi(tokenized_policy_list)

    # gensim
    bm25 = BM25(tokenized_policy_list)

    for num, row in df.iterrows():
        tokenized_query = row["Policy"].split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        bm25_matrix[num] = doc_scores

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
                sort_score_index = np.argsort(other_policy_scores)
                # print(other_policy_index)
                # print(other_policy_scores)

                bm25_score_first[idx] = other_policy_scores[sort_score_index[0]]
                bm25_policy_first[idx] = policy_list[other_policy_index[sort_score_index[0]]]
                bm25_index_first[idx] = other_policy_index[sort_score_index[0]]

        else:
            group_policy_number[index] = len(index)

            for num, idx in enumerate(index):
                scores = bm25_matrix[idx]
                other_policy_index = np.delete(index, num)
                other_policy_scores = scores[other_policy_index]
                sort_score_index = np.argsort(other_policy_scores)
                # print(other_policy_index[sort_score_index[0]])
                # print(policy_list[other_policy_index[sort_score_index[0]]])

                bm25_score_first[idx] = other_policy_scores[sort_score_index[0]]
                bm25_policy_first[idx] = policy_list[other_policy_index[sort_score_index[0]]]
                bm25_score_second[idx] = other_policy_scores[sort_score_index[1]]
                bm25_policy_second[idx] = policy_list[other_policy_index[sort_score_index[1]]]
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
