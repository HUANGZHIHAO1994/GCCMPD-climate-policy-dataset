import pandas as pd
import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':
    df = pd.read_csv("cp.csv")

    # ================== Reference ==================
    # ipcc_wg3_ar5_chapter15 table15.1/ipcc_wg3_ar5_chapter6 table6.7

    # ================== View the objective classification in cp ==================
    # print(set(df["Policy objective"].str.replace(', ', ',').str.replace(';', ',').str.cat(sep=',').split(',')))
    # print(len(set(df["Policy objective"].str.replace(', ', ',').str.replace(';', ',').str.cat(sep=',').split(','))))

    # ================== Notes ==================
    # First element of list: objective
    # Second element of list: Sub-objective
    # First one "" means skip
    # Second one "" means only objective

    objective \
        = {'Adaptation',
           'Air pollution',
           'Economic development',
           'Energy access',
           'Energy security',
           'Food security',
           'Land use',
           'Mitigation',
           'Water'}

    cp_objective = dict()
    cp_objective['Adaptation'] = ['', '']
    cp_objective['Air pollution'] = ['Social;Environmental', 'Social:Health impact;Environmental:Ecosystem impact']
    cp_objective['Economic development'] = ['Economic', '']
    cp_objective['Energy access'] = ['Social', 'Social:Energy/mobility access']
    cp_objective['Energy security'] = ['Economic', 'Economic:Energy security']
    cp_objective['Food security'] = ['Social', 'Social:Health impact;Social:Food security']
    cp_objective['Land use'] = ['Environmental', 'Environmental:Land-use competition']
    cp_objective['Mitigation'] = ['', '']
    cp_objective['Water'] = ['Social;Environmental', 'Social:Health impact;Environmental:Water use/quality']

    with open('cp_objective_dict.json', 'w') as f:
        json.dump(cp_objective, f)
