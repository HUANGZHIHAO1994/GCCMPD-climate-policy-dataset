import pandas as pd
import spacy
import geonamescache
from tqdm import tqdm
import shutil


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

    df = pd.read_excel("/home/zhhuang/climate_policy_paper/code/data/ALL_POLICIES_EN.xlsx")
    df['Policy_Content'].fillna('', inplace=True)

    scope_map = {"National, Bilateral, Subnational": 'SubNational', 'Multilateral': 'International',
                 'Bilateral': 'International', 'Bilateral, Multilateral': 'International',
                 'National, Subnational': 'SubNational', 'National, Other': 'National',
                 'National, Bilateral': 'SubNational', 'National, Multilateral': 'International',
                 'Other': 'Unknown', "National": "National", "International": "International",
                 "Subnational": "SubNational", "SubNational": "SubNational", "Subnational region": "Subnational region",
                 'Unknown': 'Unknown', 'Covering two or more countries': "International", 'Local': 'SubNational',
                 'Regional': 'Subnational region', 'National': 'National', '': 'Unknown'}

    df["Scope"].fillna('Unknown', inplace=True)
    df["Scope"] = df["Scope"].map(scope_map)
    scope = df["Scope"].to_list()

    bar = tqdm(range(len(df)), desc='National City NER', ncols=150)
    for _, index_row in zip(bar, df.iterrows()):
        index, row = index_row
        if row["Scope"] in ["National", 'Unknown']:
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
    with pd.ExcelWriter("ALL_POLICIES_EN.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        df.to_excel(writer, index=False)
    shutil.copy("ALL_POLICIES_EN.xlsx", '/home/zhhuang/climate_policy_paper/code/data/ALL_POLICIES_EN.xlsx')
