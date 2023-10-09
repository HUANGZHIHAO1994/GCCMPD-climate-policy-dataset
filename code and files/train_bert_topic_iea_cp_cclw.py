import argparse
import torch
import torch.nn as nn
import os
import json
import re
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel, pipeline

from sentence_transformers import SentenceTransformer
from sklearn.metrics import f1_score, classification_report
from tqdm import tqdm
from hdbscan import HDBSCAN
from bertopic import BERTopic
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from bertopic.representation import MaximalMarginalRelevance
import spacy

from nltk import data

data.path.append(r"/home/zhhuang/climate_policy_paper/code/data/nltk_data")

device = 'cuda' if torch.cuda.is_available() else 'cpu'


def analyze(args):
    # 设置模型
    model = AutoModel.from_pretrained(args.model_path).to(device)
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_path, add_special_tokens=True)
    feature_extractor = pipeline(task='feature-extraction', model=model, tokenizer=tokenizer, device=model.device)

    df = pd.read_excel("/home/zhhuang/climate_policy_paper/code/data/Topic_docs_time_iea_cp_cclw.xlsx")
    docs, timestamp = df["docs"].to_list(), df["Year"].to_list()

    representation_model = MaximalMarginalRelevance(diversity=args.diversity)
    hdbscan_model = HDBSCAN(min_cluster_size=10, min_samples=10, cluster_selection_epsilon=0.05, metric='euclidean',
                            prediction_data=True)
    # topic_model = BERTopic(embedding_model=ASPIRE, language="english", nr_topics="auto", verbose=True,
    #                        n_gram_range=(1, 3))
    topic_model = BERTopic(embedding_model=feature_extractor, language="english", nr_topics=args.nr_topics,
                           verbose=True,
                           min_topic_size=args.min_topic_size, calculate_probabilities=True,
                           representation_model=representation_model, hdbscan_model=hdbscan_model)
    topics, probs = topic_model.fit_transform(docs)

    print(topic_model.get_topic_info())
    print(topic_model.get_document_info(docs))

    topic_model.save(os.path.join(args.save_dir, f'bert_topic_iea_cp_cclw_model'))
    # topic_model = BERTopic.load("bert_topic_model")

    topic_df = topic_model.get_document_info(docs)[
        ["Topic", "Name", "Top_n_words", "Probability", "Representative_document"]]
    topic_df['Policy'] = df["Policy"].to_list()
    topic_df['Policy_Content'] = df["Policy_Content"].to_list()
    topic_df["Year"] = df["Year"].to_list()
    #     topic_df["Country"] = df["Country"].to_list()
    topic_df["ISO"] = df["ISO_code"].to_list()
    topic_df['Annex'] = df["Annex"].to_list()
    topic_df['IPCC_Region'] = df["IPCC_Region"].to_list()

    with pd.ExcelWriter("Topic_iea_cp_cclw.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        topic_df.to_excel(writer)

    # return docs, feature_extractor, timestamp


def parser():
    parser = argparse.ArgumentParser()

    # 模式配置
    parser.add_argument('--do_train', action='store_true', help="Whether to run training.")
    parser.add_argument('--do_test', action='store_true', help="Whether to run evaluating.")

    # 模型配置
    parser.add_argument('--model_path',
                        default='/home/zhhuang/climate_policy_paper/models/distilroberta-base-climate-f')
    parser.add_argument('--tokenizer_path',
                        default='/home/zhhuang/climate_policy_paper/models/distilroberta-base-climate-f')

    parser.add_argument('--min_topic_size', default=100, type=int)
    parser.add_argument('--nr_topics', default=50, type=int)
    parser.add_argument('--diversity', default=0.2, type=int)

    # 数据配置
    parser.add_argument('--data_dir', default='./data/')
    parser.add_argument('--save_dir', default='./model_save')
    parser.add_argument('--log_dir', default='./log/')

    # 其他配置
    parser.add_argument('--flag', default='sample', type=str)
    # args = parser.parse_args(args=[])
    args = parser.parse_args()

    return args


def check_args(args):
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)


def main():
    args = parser()
    check_args(args)

    if args.do_train:
        analyze(args)

    if args.do_test:
        pass


if __name__ == '__main__':
    main()
