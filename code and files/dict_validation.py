import argparse
import os
import json
import pandas as pd

from sklearn.metrics import f1_score, classification_report
from tqdm import tqdm


def load_label2id(args):
    with open('/home/zhhuang/climate_policy_paper/code/data/labels2ids.json', 'r', encoding='utf8') as file:
        labels2ids = json.load(file)
    return labels2ids[args.attribution]


def test(args):
    label2id = load_label2id(args)
    args.num_labels = len(label2id)

    df_lab = pd.read_excel('/home/zhhuang/climate_policy_paper/code/files/policy_db_complete.xlsx',
                           sheet_name='raw_data')

    df_pred = pd.read_excel('/home/zhhuang/climate_policy_paper/code/files/policy_db_complete.xlsx',
                            sheet_name='all_policies_dedup')

    index_list = set(df_lab['A'].to_list()) & set(df_pred['A'].to_list())

    preds = []
    labs = []

    for i in index_list:
        pre_label = [0] * len(label2id)
        if isinstance(df_pred[df_pred["A"] == i][args.attribution].values[0], str):

            for l in df_pred[df_pred["A"] == i][args.attribution].values[0].split(';'):
                idx = label2id[l]
                pre_label[idx] = 1
        preds.append(pre_label)

        tru_label = [0] * len(label2id)
        if isinstance(df_lab[df_lab["A"] == i][args.attribution].values[0], str):

            for l in df_lab[df_lab["A"] == i][args.attribution].values[0].split(';'):
                idx = label2id[l]
                tru_label[idx] = 1
        labs.append(tru_label)
    report = classification_report(labs, preds, target_names=list(label2id.keys()), zero_division=1, output_dict=True)
    print(report)

    df = pd.DataFrame(report).transpose()
    df.to_csv(os.path.join(args.save_dir, f'dict_validation_{args.attribution}.csv'), index=True)


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
    parser.add_argument('--attribution', default='Instrument', type=str)

    # 数据配置
    parser.add_argument('--data_dir', default='../data/')
    parser.add_argument('--save_dir', default='./model_save')
    parser.add_argument('--log_dir', default='./log/')

    # 其他配置
    parser.add_argument('--flag', default='sample', type=str)

    args = parser.parse_args()

    return args


def main():
    args = parser()

    if args.do_test:
        test(args)


if __name__ == '__main__':
    main()
