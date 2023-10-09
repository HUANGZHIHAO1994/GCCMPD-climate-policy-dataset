import argparse
import torch
import torch.nn as nn
import os
import json
import pandas as pd

from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_linear_schedule_with_warmup
from sklearn.metrics import f1_score, classification_report
from tqdm import tqdm

device = 'cuda' if torch.cuda.is_available() else 'cpu'


class MyDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)


def save_to_jsonl(path, samples):
    with open(path, 'w', encoding='utf8') as file:
        for sample in samples:
            file.write(json.dumps(sample) + '\n')


def record(args, infos):
    with open(os.path.join(args.log_dir, f'log_climate_bert_{args.attribution}.txt'), 'a+', encoding='utf8') as file:
        file.write(json.dumps(infos) + '\n')


def load_label2id(args):
    if args.attribution == "law or strategy":
        with open(os.path.join(args.data_dir, 'labels2ids_law_or_strategy.json'), 'r', encoding='utf8') as file:
            labels2ids = json.load(file)
    else:
        with open(os.path.join(args.data_dir, 'labels2ids.json'), 'r', encoding='utf8') as file:
            labels2ids = json.load(file)
    # with open(os.path.join(args.data_dir, 'labels2ids.json'), 'r', encoding='utf8') as file:
    #     labels2ids = json.load(file)

    return labels2ids[args.attribution]


def convert_label2id(label2id: dict):
    id2label = {}
    for label, id in label2id.items():
        id2label[id] = label
    return id2label


def convert_input_format(args, batch, tokenizer):
    batch_titles = [b['title'] for b in batch]
    batch_contents = [b['content'] for b in batch]

    outputs = tokenizer.batch_encode_plus(
        batch_text_or_text_pairs=list(zip(batch_titles, batch_contents)),
        padding=True,
        max_length=512,
        truncation=True,
        return_tensors='pt'
    )

    input_ids, attention_mask = outputs['input_ids'], outputs['attention_mask']

    return input_ids.to(device), attention_mask.to(device)


def load_excel(path):
    df = pd.read_excel(path, sheet_name='Sheet1')
    df = df[['Policy', 'Policy_Content']]
    samples = df.to_dict(orient='records')
    return samples


def read_jsonl(args, path):
    samples = []
    for sample in load_excel(path):
        samples.append({
            'title': sample['Policy'] if isinstance(sample['Policy'], str) else '',
            'content': sample['Policy_Content'] if isinstance(sample['Policy_Content'], str) else '',
        })

    return samples


def test(args):
    label2id = load_label2id(args)
    id2label = convert_label2id(label2id)
    args.num_labels = len(label2id)

    # 设置模型
    model = AutoModelForSequenceClassification.from_pretrained(
        os.path.join(args.save_dir, f'best_climate_bert_{args.attribution}'),
        problem_type='single_label_classification',
        num_labels=args.num_labels).to(device)
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_path)

    # 加载数据
    testset = read_jsonl(args, os.path.join(args.data_dir, 'ALL_POLICIES_EN.xlsx'))
    test_loader = DataLoader(MyDataset(testset), batch_size=args.eval_batch_size, shuffle=False, collate_fn=lambda x: x)

    samples = []
    preds = []

    model.eval()
    with torch.no_grad():
        bar = tqdm(range(len(test_loader)), desc='Testing', ncols=150)
        for i, batch in zip(bar, test_loader):

            input_ids, attention_mask = convert_input_format(args, batch, tokenizer)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )

            logits = outputs.logits
            prediction = torch.argmax(logits, dim=-1)
            preds.extend(prediction.tolist())

            # 保存
            for b, pred in zip(batch, prediction.tolist()):
                samples.append({
                    'Policy': b['title'],
                    'Policy_Content': b['content'],
                    args.attribution: id2label[pred]
                })

    save_to_jsonl(os.path.join(args.save_dir, f'prediction_{args.attribution}.jsonl'), samples)


def parser():
    parser = argparse.ArgumentParser()

    # 模型配置
    parser.add_argument('--tokenizer_path',
                        default='/home/zhhuang/climate_policy_paper/models/distilroberta-base-climate-f')
    parser.add_argument('--eval_batch_size', default=32, type=int)

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
    test(args)


if __name__ == '__main__':
    main()

    """
    -----sector-----
                    precision    recall  f1-score   support

Energy systems       0.75      0.79      0.77       775
  Multi-sector       0.73      0.69      0.71       769
      Industry       0.60      0.59      0.60       273
     Buildings       0.83      0.78      0.81       498
         AFOLU       0.70      0.81      0.75       148
     Transport       0.83      0.80      0.81       458

     micro avg       0.76      0.75      0.75      2921
     macro avg       0.74      0.74      0.74      2921
  weighted avg       0.76      0.75      0.75      2921
   samples avg       0.82      0.83      0.75      2921

    --------Instrument-------
                                                      precision    recall  f1-score   support

                                                       1.00      1.00      1.00         0
                           Regulatory Approaches       0.75      0.72      0.74       882
                               Voluntary Actions       0.67      0.43      0.52        75
                             Tradable Allowances       0.94      0.65      0.77        23
Government Provision of Public Goods or Services       0.85      0.87      0.86      1418
                                           Taxes       0.67      0.54      0.60       142
                          Information Programmes       0.71      0.67      0.69       689
                                       Subsidies       0.79      0.79      0.79       693

                                       micro avg       0.79      0.76      0.78      3922
                                       macro avg       0.80      0.71      0.74      3922
                                    weighted avg       0.78      0.76      0.77      3922
                                     samples avg       0.82      0.81      0.76      3922
    """
