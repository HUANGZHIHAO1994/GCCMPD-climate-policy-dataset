import pandas as pd
import json
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from nltk import data

data.path.append(r"/home/zhhuang/climate_policy_paper/code/data/nltk_data")


def load_stopwords():
    stopwords = []
    with open('stopwords.txt', 'r', encoding='utf8') as file:
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

    for text in texts:
        # 1.去除年份和%，如1991-2007，2025，2.5%
        n_text = re.sub(r'(\d{4}(-\d{4})?)|([-+]?\d+(.\d+)?%)', '', str(text))

        # 2.converting all characters to lowercase 小写
        n_text = n_text.lower()

        # 3.stopwords 停用词 (包含punctuation and symbols 标点和符号)
        words = [word for word in word_tokenize(n_text) if word not in stopwords]

        processed_texts.append(' '.join(words))

        # # 4.lemmatization 词形还原
        # words = list(lemmatize(words, wnl))

        # # 5.removing fewer than five characters 去除5个单词以内的
        # if len(words) > 5:
        #     processed_texts.append(' '.join(words))
        # else:
        #     processed_texts.append('')

    return processed_texts


def load_excel():
    df = pd.read_excel('policy_db_complete.xlsx', sheet_name='all_policies_dedup')
    df = df[['Policy', 'Policy_Content', 'law or strategy', 'Policy Type', 'sector', 'subsector', 'Instrument',
             'Sector-Instrument', 'objective', 'subobjective', 'Jurisdiction_standard_amend']]
    #     # df.dropna(subset=['Policy_Content'], inplace=True)
    #     df["Policy_Content"] = df["Policy_Content"] = df["Policy_Content"].str.lower()
    #     df["Policy_Content"] = df["Policy_Content"].str.replace('\n', ' ', regex=False)
    #     # df["Policy_Content"] = df["Policy_Content"].str.replace(r'<a href.+?>', ' ', regex=True)
    #     # df["Policy_Content"] = df["Policy_Content"].str.replace(r'<ul style.+?>', ' ', regex=True)
    #     df["Policy_Content"] = df["Policy_Content"].str.replace(r'<.+?>', ' ', regex=True)
    #     df["Policy_Content"] = df["Policy_Content"].str.replace('&nbsp;', ' ', regex=False)
    #     df["Policy_Content"] = df["Policy_Content"].str.replace(
    #         'IEA/IRENA Global Renewable Energy Policies and Measures Database © OECD/IEA and IRENA, [November 2020]', '',
    #         regex=False)
    #     # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(source:.+?\)', ' ', regex=True)
    #     # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(http:.+?\)', ' ', regex=True)
    #     # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(Reference.+?\)', ' ', regex=True)
    #     df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(.+?\)', ' ', regex=True)
    #     df["Policy_Content"] = df["Policy_Content"].str.replace(r'\[.+?\]', ' ', regex=True)

    #     policy_content = normalize(df["Policy_Content"].to_list())
    #     df["Policy_Content"] = policy_content

    #     policy_title = normalize(df["Policy"].to_list())
    #     df["Policy"] = policy_title

    samples = df.to_dict(orient='records')

    return samples


def get_label(samples):
    labels2ids = {}
    for sample in samples:
        for key in sample:
            if key not in ['Policy', 'Policy_Content']:

                if key not in labels2ids:
                    labels2ids[key] = set()

                label = sample[key]
                if isinstance(label, str):
                    for _label in label.split(';'):
                        if _label == "":
                            print(sample)
                        labels2ids[key].add(_label)

    final = {}

    for key in labels2ids:
        final[key] = {l: i for i, l in enumerate(list(labels2ids[key]))}

    with open('labels2ids.json', 'w', encoding='utf8') as file:
        json.dump(final, file, indent=4)

    return final


def save_jsonl(path, samples):
    with open(path, 'w', encoding='utf8') as file:
        for sample in samples:
            file.write(json.dumps(sample) + '\n')


if __name__ == '__main__':
    samples = load_excel()
    labels2ids = get_label(samples)

    train, test = train_test_split(samples, test_size=0.15, random_state=0)
    save_jsonl('train.jsonl', train)
    save_jsonl('test.jsonl', test)
