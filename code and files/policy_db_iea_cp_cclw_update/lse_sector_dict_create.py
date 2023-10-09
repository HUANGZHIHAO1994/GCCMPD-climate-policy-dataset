import pandas as pd
import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':
    df = pd.read_csv("lse.csv")

    # ================== View the sector classification in LSE ==================
    # print(set(df["Sectors"].str.cat(sep=',').split(',')))
    # print(set([x.strip() for x in list(set(df["Sectors"].str.cat(sep=',').split(',')))]))
    # print(len(set([x.strip() for x in list(set(df["Sectors"].str.cat(sep=',').split(',')))])))

    # ================== Notes ==================
    # First element of list: Sector
    # Second element of list: Sub-sector
    # First one "" means skip, such as Demand response can be electricity or transport, invalid judgment
    # Second one "" means only Sector

    lse_sector = dict()

    lse_sector['Economy-wide'] = ['Multi-sector', '']
    lse_sector['Transport'] = ['Transport', '']
    lse_sector['Tourism'] = ['', '']
    lse_sector['Transportation'] = ['Transport', '']
    lse_sector['Industry'] = ['Industry', '']
    lse_sector['Waste'] = ['Industry', 'Industry:Waste']
    lse_sector['Water'] = ['', '']
    lse_sector['Energy'] = ['Energy systems', '']
    lse_sector['Residential and Commercial'] = ['Buildings', 'Buildings:Residential;Buildings:Non-residential']
    lse_sector['Residential & Commercial'] = ['Buildings', 'Buildings:Residential;Buildings:Non-residential']
    lse_sector['Rural'] = ['', '']
    lse_sector['Urban'] = ['', '']
    lse_sector['Buildings'] = ['Buildings', '']
    lse_sector['Coastal zones'] = ['', '']
    lse_sector['Cross Cutting Area'] = ['', '']
    lse_sector['LULUCF'] = ['AFOLU', '']
    lse_sector['Agriculture'] = ['AFOLU', '']
    lse_sector['Health'] = ['', '']
    lse_sector['Social development'] = ['', '']
    lse_sector['Environment'] = ['', '']
    lse_sector['Finance'] = ['', '']
    lse_sector['Disaster Risk Management (Drm)'] = ['', '']
    lse_sector['Disaster Risk Management'] = ['', '']
    lse_sector['Adaptation'] = ['', '']
    lse_sector['Public Sector'] = ['', '']
    lse_sector['Other'] = ['', '']

    with open('lse_sector_dict.json', 'w') as f:
        json.dump(lse_sector, f)

    # ========= In doubt, manual verification is required =========

    # lse_sector['Residential and Commercial'] = ['Buildings', 'Buildings:Residential']
