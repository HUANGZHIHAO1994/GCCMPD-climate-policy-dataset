import pandas as pd
import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':
    df = pd.read_excel("iea.xlsx")

    # ================== Reference ==================
    # ipcc_wg3_ar5_chapter15 table15.1/ipcc_wg3_ar5_chapter6 table6.7

    # ================== View the objective classification in iea ==================
    # print(set(df["Topics"].str.cat(sep=';').split(';')))
    # print(len(set(df["Topics"].str.cat(sep=';').split(';'))))

    # ================== Notes ==================
    # First element of list: objective
    # Second element of list: Sub-objective
    # First one "" means skip
    # Second one "" means only objective

    objective \
        = {'Air Quality',
           'Carbon Capture Utilisation and Storage',
           'Cities',
           'Critical Minerals',
           'Digitalisation',
           'Electrification',
           'Energy Access',
           'Energy Efficiency',
           'Energy Poverty',
           'Energy Security',
           'Energy Water Nexus',
           'Methane abatement',
           'Renewable Energy',
           'Technology R&D and innovation'}

    iea_objective = dict()

    iea_objective['Air Quality'] = ['Social;Environmental', 'Social:Health impact;Environmental:Ecosystem impact']
    iea_objective['Carbon Capture Utilisation and Storage'] = ['Environmental', 'Environmental:Ecosystem impact']
    iea_objective['Cities'] = ['Social', '']
    iea_objective['Critical Minerals'] = ['Environmental', 'Environmental:Resource/material use impact']
    iea_objective['Digitalisation'] = ['Social', 'Social:Energy/mobility access']
    iea_objective['Electrification'] = ['Social', 'Social:Energy/mobility access']
    iea_objective['Energy Access'] = ['Social', 'Social:Energy/mobility access']
    iea_objective['Energy Efficiency'] = ['Economic', 'Economic:Productivity/competitiveness']
    iea_objective['Energy Poverty'] = ['Social', 'Social:(Fuel) Poverty alleviation']
    iea_objective['Energy Security'] = ['Economic', 'Economic:Energy security']
    iea_objective['Energy Water Nexus'] = ['Environmental', 'Environmental:Water use/quality']
    iea_objective['Methane abatement'] = ['Environmental', 'Environmental:Ecosystem impact']
    iea_objective['Just Transition'] = ['', '']
    iea_objective['Renewable Energy'] = ['', '']
    # iea_objective['Renewable Energy'] \
    #     = ['Social;Economic;Environmental',
    #        'Social:Energy/mobility access;Social:Health impact;Economic:Energy security;Environmental:Ecosystem impact']
    iea_objective['Technology R&D and innovation'] = ['Economic', 'Economic:Technological spillover/innovation']

    with open('iea_objective_dict.json', 'w') as f:
        json.dump(iea_objective, f)
