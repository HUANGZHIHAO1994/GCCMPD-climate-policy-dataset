import pandas as pd
import spacy
import geonamescache
from tqdm import tqdm
import shutil
from sklearn.metrics import f1_score, classification_report


def gen_dict_extract(var, key):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)


if __name__ == '__main__':
    gc = geonamescache.GeonamesCache()

    # gets nested dictionary for countries
    countries = gc.get_countries()

    # gets nested dictionary for cities
    cities = gc.get_cities()

    cities = [*gen_dict_extract(cities, 'name')]
    countries = [*gen_dict_extract(countries, 'name')]

    nlp = spacy.load("en_core_web_trf")

    df = pd.read_excel("/home/zhhuang/climate_policy_paper/code/files/policy_db_complete.xlsx",
                       sheet_name="all_policies_dedup")
    df = df.drop(df[df["Jurisdiction_standard_amend"] == "Unknown"].index)
    print(df)
    df['Policy_Content'].fillna('', inplace=True)

    scope_lab = df["Jurisdiction_standard_amend"].to_list()
    scope = ["National"] * len(df["Jurisdiction_standard_amend"].to_list())

    bar = tqdm(range(len(df)), desc='National City NER', ncols=150)
    for _, index_row in zip(bar, df.iterrows()):
        index, row = index_row
        doc_title = nlp(row["Policy"])
        doc_content = nlp(row['Policy_Content'])

        judge = True
        citi = []
        country = []
        for ent in doc_title.ents:
            if ent.label_ == 'GPE':
                if ent.text in countries:
                    country.append(ent.text)
                elif ent.text in cities:
                    citi.append(ent.text)

        if len(set(citi)) == 1:
            scope[index] = "SubNational"
            print("SubNational: ", row["Policy"])
            judge = False
        elif len(set(citi)) > 1:
            scope[index] = "Subnational region"
            print("Subnational region: ", row["Policy"])
            judge = False
        elif len(set(country)) > 1:
            scope[index] = "International"
            print("International: ", row["Policy"])
            judge = False

        if judge:
            for ent in doc_content.ents:
                if ent.label_ == 'GPE':
                    if ent.text in cities:
                        citi.append(ent.text)
                    elif ent.text in countries:
                        country.append(ent.text)
            if len(set(citi)) == 1:
                scope[index] = "SubNational"
                print("SubNational: ", row["Policy"])
                judge = False
            elif len(set(citi)) > 1:
                scope[index] = "Subnational region"
                print("Subnational region: ", row["Policy"])
                judge = False
            elif len(set(country)) > 1:
                scope[index] = "International"
                print("International: ", row["Policy"])
                judge = False

    df["Scope"] = scope
    df = df[["Policy", 'Policy_Content', "Jurisdiction_standard_amend", "Scope"]]
    with pd.ExcelWriter("NER_TEST.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        df.to_excel(writer, index=False)
    report = classification_report(scope_lab, scope, zero_division=1)
    print(report)
