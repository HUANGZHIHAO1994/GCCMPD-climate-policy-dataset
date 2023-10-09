import os
import pandas as pd
import json


def load_samples(path):
    samples = []
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            sample = json.loads(line.strip())
            samples.append(sample)
    return samples


def load_excel(path):
    df = pd.read_excel(path, sheet_name='Sheet1')
    samples = df.to_dict(orient='records')
    return samples


multiple_root = './multiple_labels/model_save/'
single_root = './single_labels/model_save/'

full = load_excel('./data/ALL_POLICIES_EN.xlsx')

# Multi label
for name in os.listdir(multiple_root):
    if '.jsonl' in name:
        category = name.split('.')[0].split('_')[1]

        if full is None:
            full = load_samples(os.path.join(multiple_root, name))
        else:
            for i, sample in enumerate(load_samples(os.path.join(multiple_root, name))):
                full[i][category] = sample[category]

# Single Label
for name in os.listdir(single_root):
    if '.jsonl' in name:
        category = name.split('.')[0].split('_')[1]

        if full is None:
            full = load_samples(os.path.join(single_root, name))
        else:
            for i, sample in enumerate(load_samples(os.path.join(single_root, name))):
                full[i][category] = sample[category]

df = pd.DataFrame(full)

# Dealing with Constitutional and International Law

law_or_strategy = df["law or strategy"].to_list()
for index, row in df.iterrows():
    # Title
    policy = row["Policy"].lower(). \
        replace("(", ' ').replace(")", ' ').replace(",", ' ').replace("\"", ' ').replace("'", ' '). \
        replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')
    if ("constitution" in policy) or ("constitutional" in policy):
        law_or_strategy[index] = 'Constitution'
    elif ("treaties" in policy) or ("treaty" in policy):
        law_or_strategy[index] = 'International Law'

df["law or strategy"] = law_or_strategy
df.loc[df['Source'] == 'ECOLEX_Treaty', ["law or strategy"]] = 'International Law'

# Save excel
with pd.ExcelWriter('results.xlsx', engine='xlsxwriter',
                    engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
    df.to_excel(writer)
