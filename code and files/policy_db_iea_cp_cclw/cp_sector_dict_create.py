import pandas as pd
import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':

    df = pd.read_csv("cp.csv")

    # ================== View the sector classification in cp ==================
    # print(set(df["Sector name"].str.lstrip(' ').str.rstrip(' ').str.cat(sep=',').split(',')))
    # print(set(df["Sector name"].str.cat(sep=',').split(',')))
    # print(set([x.strip() for x in list(set(df["Sector name"].str.cat(sep=',').split(',')))]))
    # print(len(set([x.strip() for x in list(set(df["Sector name"].str.cat(sep=',').split(',')))])))

    # ================== Notes ==================
    # First element of list: Sector
    # Second element of list: Sub-sector
    # First one "" means skip, such as Demand response can be electricity or transport, invalid judgment
    # Second one "" means only Sector

    # No "Energy systems" in the sector of cp，Covered in "Electricity and heat"

    sector = {
        "Agriculture and forestry": [
            "Agricultural CH4",
            "Agricultural CO2",
            "Agricultural N2O",
            "Forestry"
        ],
        "Buildings": [
            "Appliances",
            "Construction",
            "Heating and cooling",
            "Hot water and cooking"
        ],
        "Electricity and heat": [
            "CCS",
            "Coal",
            "Gas",
            "Nuclear",
            "Oil",
            "Renewables"
        ],
        "General": [],
        "Industry": [
            "Fluorinated gases",
            "Fossil fuel exploration and production",
            "Industrial energy related",
            "Industrial N2O",
            "Industrial process CO2",
            "Negative emissions",
            "Waste CH4"
        ],
        "Transport": [
            "Air",
            "Heavy-duty vehicles",
            "Light-duty vehicles",
            "Low-emissions mobility",
            "Rail",
            "Shipping"
        ]
    }

    cp_sector = dict()
    for sec in sector:
        if sec == "Agriculture and forestry":
            cp_sector[sec] = ['AFOLU', '']
            for subsec in sector[sec]:
                cp_sector[subsec] = ['AFOLU', '']

        if sec == "Buildings":
            cp_sector[sec] = ['Buildings', '']
            for subsec in sector[sec]:
                if subsec in ["Appliances", "Hot water and cooking"]:
                    cp_sector[subsec] = ['Buildings', 'Buildings:Residential']
                else:
                    cp_sector[subsec] = ['Buildings', '']

        if sec == "Electricity and heat":
            cp_sector[sec] = ['Energy systems', 'Energy systems:Electricity & heat']
            for subsec in sector[sec]:
                cp_sector[subsec] = ['Energy systems', 'Energy systems:Electricity & heat']

        if sec == "General":
            cp_sector[sec] = ['Multi-sector', '']

        if sec == "Industry":
            cp_sector[sec] = ["Industry", '']
            for subsec in sector[sec]:
                if subsec in ["Fluorinated gases"]:
                    cp_sector[subsec] = ['Industry', 'Industry:Other industry']
                    # "Industrial N2O" "Negative emissions" "Industrial process CO2" "Industrial energy related"
                    # could also be Metals or other
                elif subsec in ["Waste CH4"]:
                    cp_sector[subsec] = ['Industry', 'Industry:Waste']
                # elif subsec in ["Industrial N2O"]:
                #     cp_sector[subsec] = ['Industry', 'Industry:Chemicals']
                elif subsec in ["Fossil fuel exploration and production"]:
                    # Off - road machinery: mining(diesel)
                    # EDGAR Database classifies it into Energy systems
                    cp_sector[subsec] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
                else:
                    cp_sector[subsec] = ['Industry', '']

        if sec == "Transport":
            cp_sector[sec] = ["Transport", '']
            for subsec in sector[sec]:
                if subsec in ["Air"]:
                    cp_sector[subsec] = ['Transport', 'Transport:Domestic Aviation']
                elif subsec in ["Heavy-duty vehicles", "Light-duty vehicles", "Low-emissions mobility"]:
                    cp_sector[subsec] = ['Transport', 'Transport:Road']
                elif subsec in ["Rail"]:
                    cp_sector[subsec] = ['Transport', 'Transport:Rail']
                elif subsec in ["Shipping"]:
                    cp_sector[subsec] = ['Transport', 'Transport:Inland Shipping']

    with open('cp_sector_dict.json', 'w') as f:
        json.dump(cp_sector, f)

    # ================== In doubt, manual verification is required ==================

    # cp_sector["Air"] = ['Transport', 'Transport:Domestic Aviation']
    # cp_sector["Shipping"] = ['Transport', 'Transport:Inland Shipping']
