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


def record(args, infos):
    with open(os.path.join(args.log_dir, f'log_climate_bert_{args.attribution}.txt'), 'a+', encoding='utf8') as file:
        file.write(json.dumps(infos) + '\n')


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


def convert_label2id(label2id: dict):
    id2label = {}
    for label, id in label2id.items():
        id2label[id] = label
    return id2label


def convert_input_format(args, batch, tokenizer):
    batch_titles = [b['title'] for b in batch]
    batch_contents = [b['content'] for b in batch]

    batch_labels = [b['label'] for b in batch]

    outputs = tokenizer.batch_encode_plus(
        batch_text_or_text_pairs=list(zip(batch_titles, batch_contents)),
        padding=True,
        max_length=512,
        truncation=True,
        return_tensors='pt'
    )

    input_ids, attention_mask = outputs['input_ids'], outputs['attention_mask']
    labels = torch.LongTensor(batch_labels)

    return input_ids.to(device), attention_mask.to(device), labels.to(device)


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

    # 设置模型
    model = AutoModelForSequenceClassification.from_pretrained(args.model_path,
                                                               problem_type='single_label_classification',
                                                               num_labels=args.num_labels).to(device)
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_path)

    # 加载数据
    if args.attribution == "law or strategy":
        trainset = read_jsonl(args, os.path.join(args.data_dir, 'train_law_or_strategy.jsonl'), label2id)
        train_loader = DataLoader(MyDataset(trainset), batch_size=args.batch_size, shuffle=True, collate_fn=lambda x: x)

        testset = read_jsonl(args, os.path.join(args.data_dir, 'test_law_or_strategy.jsonl'), label2id)
        test_loader = DataLoader(MyDataset(testset), batch_size=args.eval_batch_size, shuffle=False,
                                 collate_fn=lambda x: x)
    # 加载数据
    elif args.attribution == "Jurisdiction_standard_amend":
        trainset = read_jsonl(args, os.path.join(args.data_dir, 'train_jurisdiction.jsonl'), label2id)
        train_loader = DataLoader(MyDataset(trainset), batch_size=args.batch_size, shuffle=True,
                                  collate_fn=lambda x: x)

        testset = read_jsonl(args, os.path.join(args.data_dir, 'test_jurisdiction.jsonl'), label2id)
        test_loader = DataLoader(MyDataset(testset), batch_size=args.eval_batch_size, shuffle=False,
                                 collate_fn=lambda x: x)
    else:
        trainset = read_jsonl(args, os.path.join(args.data_dir, 'train.jsonl'), label2id)
        train_loader = DataLoader(MyDataset(trainset), batch_size=args.batch_size, shuffle=True, collate_fn=lambda x: x)

        testset = read_jsonl(args, os.path.join(args.data_dir, 'test.jsonl'), label2id)
        test_loader = DataLoader(MyDataset(testset), batch_size=args.eval_batch_size, shuffle=False,
                                 collate_fn=lambda x: x)
    # trainset = read_jsonl(args, os.path.join(args.data_dir, 'train.jsonl'), label2id)
    # train_loader = DataLoader(MyDataset(trainset), batch_size=args.batch_size, shuffle=True, collate_fn=lambda x: x)
    #
    # testset = read_jsonl(args, os.path.join(args.data_dir, 'test.jsonl'), label2id)
    # test_loader = DataLoader(MyDataset(testset), batch_size=args.eval_batch_size, shuffle=False, collate_fn=lambda x: x)

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.99, 0.98), weight_decay=1e-4)
    scheduler = get_linear_schedule_with_warmup(optimizer, args.warming_up_step, len(train_loader) * args.epochs)

    best_f1_score = 0.

    # 训练阶段
    for epoch in range(args.epochs):
        bar = tqdm(range(len(train_loader)), desc='epoch:0 batch:0 | loss:0 best_macro_f1:0', ncols=150)
        for i, batch in zip(bar, train_loader):
            model.train()
            optimizer.zero_grad()

            input_ids, attention_mask, labels = convert_input_format(args, batch, tokenizer)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )

            loss = outputs.loss
            loss.backward()
            optimizer.step()
            scheduler.step()

            if (epoch * len(train_loader) + i) % args.eval_step == 0:
                score = evaluate(args, model, test_loader, tokenizer)
                if score > best_f1_score:
                    best_f1_score = score
                    model.save_pretrained(os.path.join(args.save_dir, f'best_climate_bert_{args.attribution}'))

                record(args, {
                    'epoch': epoch,
                    'batch': i,
                    'score': score,
                    'best_f1_score': best_f1_score
                })

            bar.set_description(f"epoch:{epoch} batch:{i} | loss:{loss.item():.3f} best_macro_f1:{best_f1_score:.3f}")


def evaluate(args, model, test_loader, tokenizer):
    labs = []
    preds = []

    model.eval()
    with torch.no_grad():
        for i, batch in enumerate(test_loader):
            input_ids, attention_mask, labels = convert_input_format(args, batch, tokenizer)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )

            logits = outputs.logits
            prediction = torch.argmax(logits, dim=-1)

            labs.extend(labels.tolist())
            preds.extend(prediction.tolist())

    macro_f1 = f1_score(labs, preds, average='macro', zero_division=1)

    return macro_f1


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
    if args.attribution == "law or strategy":
        testset = read_jsonl(args, os.path.join(args.data_dir, 'test_law_or_strategy.jsonl'), label2id)
        test_loader = DataLoader(MyDataset(testset), batch_size=args.eval_batch_size, shuffle=False,
                                 collate_fn=lambda x: x)
    elif args.attribution == "Jurisdiction_standard_amend":
        testset = read_jsonl(args, os.path.join(args.data_dir, 'test_jurisdiction.jsonl'), label2id)
        test_loader = DataLoader(MyDataset(testset), batch_size=args.eval_batch_size, shuffle=False,
                                 collate_fn=lambda x: x)
    else:
        testset = read_jsonl(args, os.path.join(args.data_dir, 'test.jsonl'), label2id)
        test_loader = DataLoader(MyDataset(testset), batch_size=args.eval_batch_size, shuffle=False,
                                 collate_fn=lambda x: x)
    # testset = read_jsonl(args, os.path.join(args.data_dir, 'test.jsonl'), label2id)
    # test_loader = DataLoader(MyDataset(testset), batch_size=args.eval_batch_size, shuffle=False, collate_fn=lambda x: x)

    labs = []
    preds = []

    model.eval()
    with torch.no_grad():
        bar = tqdm(range(len(test_loader)), desc='Testing', ncols=150)
        for i, batch in zip(bar, test_loader):
            input_ids, attention_mask, labels = convert_input_format(args, batch, tokenizer)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )

            logits = outputs.logits
            prediction = torch.argmax(logits, dim=-1)

            labs.extend(labels.tolist())
            preds.extend(prediction.tolist())

    report = classification_report(labs, preds, target_names=list(label2id.keys()), zero_division=1, output_dict=True)
    print(report)

    df = pd.DataFrame(report).transpose()
    df.to_csv(os.path.join(args.save_dir, f'climate_bert_test_result_{args.attribution}.csv'), index=True)


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
    parser.add_argument('--lr', default=2e-5, type=float)
    parser.add_argument('--warming_up_step', default=500, type=int)
    parser.add_argument('--epochs', default=10, type=int)
    parser.add_argument('--batch_size', default=16, type=int)

    parser.add_argument('--eval_batch_size', default=32, type=int)
    parser.add_argument('--eval_step', default=300, type=int)

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
