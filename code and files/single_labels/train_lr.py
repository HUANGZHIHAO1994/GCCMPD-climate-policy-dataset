import argparse
import os
import json
import joblib
import time
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.multiclass import OneVsRestClassifier


def load_label2id(args):
    if args.attribution == "law or strategy":
        with open(os.path.join(args.data_dir, 'labels2ids_law_or_strategy.json'), 'r', encoding='utf8') as file:
            labels2ids = json.load(file)
    elif args.attribution == "Jurisdiction_standard_amend":
        with open(os.path.join(args.data_dir, 'labels2ids_jurisdiction.json'), 'r', encoding='utf8') as file:
            labels2ids = json.load(file)
    else:
        with open(os.path.join(args.data_dir, 'labels2ids.json'), 'r', encoding='utf8') as file:
            labels2ids = json.load(file)
    # with open(os.path.join(args.data_dir, 'labels2ids.json'), 'r', encoding='utf8') as file:
    #     labels2ids = json.load(file)
    return labels2ids[args.attribution]


def read_jsonl(args, path, label2id):
    samples = []
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            sample = json.loads(line.strip())  # 加载数据
            label = sample[args.attribution]

            samples.append({
                'title': sample['Policy'] if isinstance(sample['Policy'], str) else '',
                'content': sample['Policy_Content'] if isinstance(sample['Policy_Content'], str) else '',
                'label': label2id[label]
            })

    return samples


def train(args):
    label2id = load_label2id(args)
    args.num_labels = len(label2id)

    if args.attribution == "law or strategy":
        trainset = read_jsonl(args, os.path.join(args.data_dir, 'train_law_or_strategy.jsonl'), label2id)
    elif args.attribution == "Jurisdiction_standard_amend":
        trainset = read_jsonl(args, os.path.join(args.data_dir, 'train_jurisdiction.jsonl'), label2id)
    else:
        trainset = read_jsonl(args, os.path.join(args.data_dir, 'train.jsonl'), label2id)

    # trainset = read_jsonl(args, os.path.join(args.data_dir, 'train.jsonl'), label2id)

    # 特征化
    if os.path.exists(os.path.join(args.save_dir, 'vectorizer.pkl')):
        vectorizer = joblib.load(os.path.join(args.save_dir, 'vectorizer.pkl'))
    else:
        vectorizer = TfidfVectorizer()
        vectorizer.fit([f"{sample['title']} {sample['content']}" for sample in trainset])
        joblib.dump(vectorizer, os.path.join(args.save_dir, 'vectorizer.pkl'))

    features = vectorizer.transform([f"{sample['title']} {sample['content']}" for sample in trainset])
    features = features.todense()
    features = np.asarray(features)

    print('完成特征化...')

    # 降维
    if os.path.exists(os.path.join(args.save_dir, 'pca.pkl')):
        pca = joblib.load(os.path.join(args.save_dir, 'pca.pkl'))
    else:
        pca = PCA(n_components=1000)
        pca.fit(features)
        joblib.dump(pca, os.path.join(args.save_dir, 'pca.pkl'))

    features = pca.transform(features)

    print('完成降维...')

    model = OneVsRestClassifier(LogisticRegression())
    model.fit(features, [sample['label'] for sample in trainset])
    joblib.dump(model, os.path.join(args.save_dir, f'lr_{args.attribution}.pkl'))

    print('完成模型训练...')


def test(args):
    label2id = load_label2id(args)
    args.num_labels = len(label2id)

    if args.attribution == "law or strategy":
        testset = read_jsonl(args, os.path.join(args.data_dir, 'test_law_or_strategy.jsonl'), label2id)
    elif args.attribution == "Jurisdiction_standard_amend":
        testset = read_jsonl(args, os.path.join(args.data_dir, 'test_jurisdiction.jsonl'), label2id)
    else:
        testset = read_jsonl(args, os.path.join(args.data_dir, 'test.jsonl'), label2id)
    # testset = read_jsonl(args, os.path.join(args.data_dir, 'test.jsonl'), label2id)

    vectorizer = joblib.load(os.path.join(args.save_dir, 'vectorizer.pkl'))
    pca = joblib.load(os.path.join(args.save_dir, 'pca.pkl'))
    model = joblib.load(os.path.join(args.save_dir, f'lr_{args.attribution}.pkl'))

    # 特征化
    features = vectorizer.transform([f"{sample['title']} {sample['content']}" for sample in testset])
    features = features.todense()
    features = np.asarray(features)

    print('完成特征化...')

    # 降维
    features = pca.transform(features)

    print('完成降维...')

    # 模型预测
    preds = model.predict(features)
    labs = [sample['label'] for sample in testset]

    report = classification_report(labs, preds, target_names=list(label2id.keys()), zero_division=1, output_dict=True)
    print(report)

    df = pd.DataFrame(report).transpose()
    df.to_csv(os.path.join(args.save_dir, f'lr_test_result_{args.attribution}.csv'), index=True)


def parser():
    parser = argparse.ArgumentParser()

    # 模式配置
    parser.add_argument('--do_train', action='store_true', help="Whether to run training.")
    parser.add_argument('--do_test', action='store_true', help="Whether to run evaluating.")

    # 配置类别
    parser.add_argument('--attribution', default='law or strategy', type=str)  # ['law or strategy', 'Policy Type']

    # 数据配置
    parser.add_argument('--data_dir', default='../data/')
    parser.add_argument('--save_dir', default='./model_save')
    parser.add_argument('--log_dir', default='./log/')

    # 其他配置
    parser.add_argument('--flag', default='sample', type=str)

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
        train(args)

    if args.do_test:
        test(args)


if __name__ == '__main__':
    main()
