import pandas as pd
import json
from tqdm import tqdm
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import spacy

from nltk import data

data.path.append(r"/home/zhhuang/climate_policy_paper/code/data/nltk_data")


def replace_str_by_index(doc, start, end):
    if len(start) <= 1:
        str_re = doc[:start[0]].text + ' ' + doc[end[-1] + 1:].text
    else:
        str_re = doc[:start[0]].text
        # print(str_re)
        for s, e in zip(end[:-1], start[1:]):
            str_temp = ' ' + doc[s + 1:e].text
            # print(str_temp)
            str_re += str_temp
        str_re = str_re + ' ' + doc[end[-1] + 1:].text

    return str_re


def load_stopwords():
    stopwords = []
    with open('/home/zhhuang/climate_policy_paper/code/data/stopwords.txt', 'r', encoding='utf8') as file:
        for line in file:
            stopwords.append(line.strip())
    stopwords += ['mee', 'gov', 'cn', 'republic', '“', 'cal', '”', 'law', 'regulation', 'decree', 'ministry', 'art',
                  'issue', 'party', 'council', 'provision', 'unite', 'kingdom', 'european', 'federation', 'ministerial',
                  'directive', 'europe', 'declaration', 'provision']
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


def normalize(texts, dlist):
    stopwords = load_stopwords()
    wnl = WordNetLemmatizer()
    processed_texts = []

    nlp = spacy.load('en_core_web_trf')

    bar = tqdm(range(len(texts)), desc='Preprocessing ...', ncols=150)
    for _, num_text in zip(bar, enumerate(texts)):
        num, text = num_text
        # for text in texts:

        # 1. web, year, %, ‰, like 1991-2007，2025，2.5%
        n_text = re.sub(
            r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)",
            '', text)
        n_text = re.sub(r'(\d{4}(-\d{4})?)|([-+]?\d+(.\d+)?%)', '', n_text)
        n_text = re.sub(r'([-+]?\d+(.\d+)?‰)', '', n_text)
        n_text = re.sub(r'(\d)+', '', n_text)

        # 2. NER
        '''
        'EVENT',
        'FAC',
        '''
        start = []
        end = []
        doc = nlp(n_text)
        for ent in doc.ents:
            if ent.label_ in ['GPE', 'ORG', 'PERSON', 'DATE', 'NORP', 'LAW', 'LOC', 'MONEY', 'PRODUCT', 'TIME',
                              'PERCENT', 'ORDINAL', 'LANGUAGE', 'CARDINAL', 'QUANTITY', 'WORK_OF_ART', 'EVENT', 'FAC']:
                start.append(ent.start)
                end.append(ent.end)

        if start:
            n_text = replace_str_by_index(doc, start, end)

        # 3. converting all characters to lowercase
        n_text = n_text.lower()
        n_text = re.sub(r'g\?co2/km', '', n_text)
        n_text = re.sub(r'm2\s?/year', '', n_text)
        n_text = re.sub(r'\(.+?\)', ' ', n_text)
        n_text = re.sub(r'\[.+?\]', ' ', n_text)
        n_text = n_text.replace("..", '.')
        n_text = n_text.replace(" •", '.')
        n_text = n_text.replace('‘', "'")
        n_text = n_text.replace("``", " ")
        n_text = n_text.replace("''", " ")
        n_text = n_text.replace("nº", 'no')
        n_text = n_text.replace("/", ' ')
        replace_list = ["european union", "ec european", "european parliament", "islamic republic", "mee gov cn",
                        "interministerial committee", "panchayat raj", "commission", " mra ", " mahrh ", " mecv ",
                        " masa ", " mme ", "interministerial", " mce ", " medd ", " mica ", " pres ", " pm ", " mef ",
                        " metd ", " mhu ", " mid ", " minagri ", " mpmef ", " mpmp  ", " micpme ", " mjldlh ", " sgm ",
                        " dggufe ", " sa ", " dc ", " pr ", " mah ", "european", 'charter', 'treaty', 'deplete',
                        'provision', "®", "sepã", "¢", "€", "ž", "¢", 'u.s.', ' ec ', 'amending', 'amendment', 'amend',
                        'amended', ' km ', ' kwh ', ' btu ', "''", ' mw ', '``', ' mtcoe ', " mefpcp ", " dgddi ",
                        " dgid ", " dgtcp ", " rgf ", " f35034 ", " meft ", " mem ", " mea ", " mef ", " mic ", " met ",
                        " mmeems ", " mefepepn ", " mcpea ", " agri ", " mats ", " mihu ", " muha ", " cj ", " rbm ",
                        " mispc ", " ms ", " mdlaat ", " dghc ", " dnsp ", " dgnsp ", " dclr ", " ecn-dd", " cab ",
                        " min ", " ecn-t", " jeb ", " ecn-ef ", " bnme ", " tt-btc ", " mlhl ", " ecntljeb ",
                        'co2', ' kw ', ' kv ', ' co2-eq ', ' mton ', ' swh ', ' twh ', ' gwh ', '‰', '¥', '°c', ' kpa ',
                        ' hdd ', ' cdd ', 'kwh/m', '°f', '≤', '≥', '<', '>', '=', ' gw ', ' kp ', ' niger ', ' sidf ',
                        ' pner ', ' nlccc ', ' sce ', ' dpe ', ' gpn ', ' sti ', ' msi ', ' sids ', ' ktoe ', ' mtoe ',
                        ' nsee ', ' sgcie ', ' bep ', ' dfid ', ' kyrgyz ', ' gj ', ' sce ', ' gujarat ', ' scfi ',
                        ' qd ', ' ttg ', ' kva ', ' tcvn ', ' bau ', ' ruen ',
                        " Ⅰ ", " Ⅱ ", " Ⅲ ", " Ⅳ ", " Ⅴ ", " Ⅵ ", " Ⅶ ", " Ⅷ ", " Ⅸ ", " Ⅹ ", " Ⅺ ", " Ⅻ ", " XIII ",
                        " XIV ", " XV ", " XVI ", " XVII ", " XVIII ", " XIX ", " XX "]
        n_text = n_text.replace("co-operative", 'cooperative')
        n_text = n_text.replace("co-operation", 'cooperation')

        for i in replace_list:
            n_text = n_text.replace(i, '')

        # 4.stopwords (punctuation and symbols)
        words = [word for word in word_tokenize(n_text) if word not in stopwords]

        # 5.lemmatization
        words = list(lemmatize(words, wnl))

        n_text = ' '.join(words)


        #         # 5.geo
        #         geo = []
        #         doc = nlp(' '.join(words))
        #         for ent in doc.ents:
        #             if ent.label_ in ['GPE','ORG','PERSON','DATE', 'NORP','LAW','LOC']:
        #                 geo.append(ent.text)

        #         words = ' '.join(words)
        #         if geo:
        #             for g in geo:
        #                 words = words.replace(g, '')
        # words = ' '.join(words)
        # processed_texts.append(words)
        #                 print(ent.text)

        if len(n_text.split()) > 5:
            processed_texts.append(n_text)
        else:
            dlist.append(num)

    return processed_texts, dlist


def process():
    #     df = pd.read_excel('policy_db_complete.xlsx', sheet_name='all_policies_dedup')
    df = pd.read_excel('/home/zhhuang/climate_policy_paper/code/data/all_policies_mitigation_result.xlsx')
    try:
        df.rename(columns={"Unnamed: 0": "Index"}, inplace=True)
    except:
        pass
    df.dropna(subset=['Policy_Content'], inplace=True)

    df["Policy_Content"] = df["Policy_Content"].str.replace(
        'IEA/IRENA Global Renewable Energy Policies and Measures Database © OECD/IEA and IRENA, [November 2020]', '',
        regex=False)
    # df["Policy_Content"] = df["Policy_Content"] = df["Policy_Content"].str.lower()
    df["Policy_Content"] = df["Policy_Content"].str.replace('\n', ' ', regex=False)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'<a href.+?>', ' ', regex=True)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'<ul style.+?>', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'<.+?>', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace('&nbsp;', ' ', regex=False)

    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(source:.+?\)', ' ', regex=True)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(http:.+?\)', ' ', regex=True)
    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(Reference.+?\)', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'\(.+?\)', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'\[.+?\]', ' ', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r' •', '.', regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'‘', "'", regex=True)
    df["Policy_Content"] = df["Policy_Content"].str.replace(r'’', "'", regex=True)

    # df["Policy_Content"] = df["Policy_Content"].str.replace(r'/', " ", regex=True)

    df.drop(df[df["Policy_Content"] == ' '].index, inplace=True)

    df.dropna(subset=['Year'], inplace=True)
    df["Year"] = df["Year"].apply(int)
    df.drop(df[df['Year'] == 0].index, inplace=True)
    df["Year"] = df["Year"].apply(str)

    df = df[["Index", 'Policy', 'Policy_Content', 'Year', 'ISO_code', 'IPCC_Region', 'Annex']]
    # df = df[['Policy', 'Policy_Content', 'Year', 'Country']]
    df = df.reset_index(drop=True)
    # df["docs"] = [''] * len(df)
    del_list = []

    # bar = tqdm(range(len(df)), desc='Preprocessing ...', ncols=150)
    # for _, num_row in zip(bar, df.iterrows()):
    #     num, row = num_row
    #     # print(f"{df['Policy']} {df['Policy_Content']}")
    docs, del_list = normalize([f"{row['Policy']} {row['Policy_Content']}" for num, row in df.iterrows()], del_list)
    # topic_doc = normalize(f"{row['Policy']} {row['Policy_Content']}")
    # df.loc[num, "docs"] = topic_doc
    # if topic_doc:
    #     pass
    # else:
    #     del_list.append(num)

    topic_df = df.drop(del_list)
    topic_df = topic_df.reset_index(drop=True)
    topic_df["docs"] = docs

    with pd.ExcelWriter("Topic_docs_time_country_expand.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        topic_df.to_excel(writer, index=False)


if __name__ == '__main__':
    process()
