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
    with open(os.path.join(args.data_dir, 'labels2ids.json'), 'r', encoding='utf8') as file:
        labels2ids = json.load(file)
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
        problem_type='multi_label_classification',
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

            logits = torch.sigmoid(outputs.logits)
            preds_tensor = logits.gt(0.5).int().tolist()

            preds.extend(preds_tensor)

            for b, pred in zip(batch, preds_tensor):
                _labels = [k for k in range(len(pred)) if pred[k]]
                samples.append({
                    'Policy': b['title'],
                    'Policy_Content': b['content'],
                    args.attribution: ';'.join([id2label[_l] for _l in _labels])
                })

    save_to_jsonl(os.path.join(args.save_dir, f'prediction_{args.attribution}.jsonl'), samples)


def parser():
    parser = argparse.ArgumentParser()

    # 模型配置
    parser.add_argument('--tokenizer_path',
                        default='/home/zhhuang/climate_policy_paper/models/distilroberta-base-climate-f')
    parser.add_argument('--eval_batch_size', default=32, type=int)

    # 配置类别
    parser.add_argument('--attribution', default='Instrument', type=str)

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
