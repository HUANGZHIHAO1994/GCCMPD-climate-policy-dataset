import pandas as pd
import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':
    df = pd.read_csv("cp.csv")

    # ================== View the instrument classification in cp ==================
    # print(set(df["Type of policy instrument"].str.replace(';', ',').str.cat(sep=',').split(',')))
    # print(set(
    #     [x.strip() for x in
    #      list(set(df["Type of policy instrument"].str.replace(';', ',').str.cat(sep=',').split(',')))]))
    # print(len(set(
    #     [x.strip() for x in
    #      list(set(df["Type of policy instrument"].str.replace(';', ',').str.cat(sep=',').split(',')))])))

    # ================== update database should use set diff ==================
    # df_old = pd.read_csv("cp_old.csv")
    # key_old = set([x.strip() for x in
    #                list(set(df_old["Type of policy instrument"].str.replace(';', ',').str.cat(sep=',').split(',')))])
    # key_new = set([x.strip() for x in
    #                list(set(df["Type of policy instrument"].str.replace(';', ',').str.cat(sep=',').split(',')))])
    # print(key_new - key_old)

    # ================== Notes ==================
    # First element of list: judge whether to use Sector to provide a basis for the third
    # First one "" means skip, "No" means No need to use Sector
    # Second element of list: Instrument
    # Third element of list: Sector-Instrument

    instrument = {
        "Barrier removal": [
            {
                "Grid access and priority for renewables": [],
                "Net metering": [],
                "Removal of fossil fuel subsidies": [],
                "Removal of split incentives (landlord tenant problem)": []
            }
        ],
        "Climate strategy": [
            {
                "Coordinating body for climate strategy": [],
                "Formal & legally binding climate strategy": [],
                "Political & non-binding climate strategy": []
            }
        ],
        "Economic instruments": [
            {
                "Direct investment": [
                    "Funds to sub-national governments",
                    "Infrastructure investments",
                    "Procurement rules",
                    "RD&D funding"
                ],
                "Fiscal or financial incentives": [
                    "CO2 taxes",
                    "Energy and other taxes",
                    "Feed-in tariffs or premiums",
                    "Grants and subsidies",
                    "Loans",
                    "Retirement premium",
                    "Tax relief",
                    "Tendering schemes",
                    "User charges"
                ],
                "Market-based instruments": [
                    "GHG emission reduction crediting and offsetting mechanism",
                    "GHG emissions allowances",
                    "Green certificates",
                    "White certificates"
                ]
            }
        ],
        "Information and education": [
            {
                "Advice or aid in implementation": [],
                "Information provision": [],
                "Performance label": [
                    "Comparison label",
                    "Endorsement label"
                ],
                "Professional training and qualification": []
            }
        ],
        "Policy support": [
            {
                "Institutional creation": [],
                "Strategic planning": []
            }
        ],
        "Regulatory Instruments": [
            {
                "Auditing": [],
                "Codes and standards": [
                    "Building codes and standards",
                    "Industrial air pollution standards",
                    "Product standards",
                    "Sectoral standards",
                    "Vehicle air pollution standards",
                    "Vehicle fuel-economy and emissions standards"
                ],
                "Monitoring": [],
                "Obligation schemes": [],
                "Other mandatory requirements": []
            }
        ],
        "Research & Development and Deployment (RD&D)": [
            {
                "Demonstration project": [],
                "Research programme": [
                    "Technology deployment and diffusion",
                    "Technology development"
                ]
            }
        ],
        "Target": [
            {
                "Energy efficiency target": [
                    "Formal & legally binding energy efficiency target",
                    "Political & non-binding energy efficiency target"
                ],
                "GHG reduction target": [
                    "Formal & legally binding GHG reduction target",
                    "Political & non-binding GHG reduction target"
                ],
                "Renewable energy target": [
                    "Formal & legally binding renewable energy target",
                    "Political & non-binding renewable energy target"
                ]
            }
        ],
        "Voluntary approaches": [
            {
                "Negotiated agreements (public-private sector)": [],
                "Public voluntary schemes": [],
                "Unilateral commitments (private sector)": []
            }
        ]
    }

    cp_instrument = dict()
    for instr in instrument:
        if instr == "Barrier removal":
            cp_instrument[instr] = ['', '', '']
            for subinstr in instrument[instr][0]:
                if subinstr == "Grid access and priority for renewables":
                    cp_instrument[subinstr] = ['Sector', 'Regulatory Approaches',
                                               {"Multi-sector": "",
                                                "Energy systems": "Regulatory Approaches:Equitable access to electricity grid",
                                                "Transport": "",
                                                "Buildings": "",
                                                "Industry": "",
                                                "AFOLU": ""
                                                }]
                if subinstr == "Net metering":
                    cp_instrument[subinstr] = ['No', 'Subsidies', '']
                if subinstr == "Removal of fossil fuel subsidies":
                    cp_instrument[subinstr] = ['Sector', 'Subsidies',
                                               {"Multi-sector": "",
                                                "Energy systems": "Subsidies:Fossil fuel subsidy removal",
                                                "Transport": "",
                                                "Buildings": "",
                                                "Industry": "",
                                                "AFOLU": ""
                                                }]
                if subinstr == "Removal of split incentives (landlord tenant problem)":
                    cp_instrument[subinstr] = ['No', 'Subsidies', '']

        if instr == "Climate strategy":
            cp_instrument[instr] = ['', '', '']
            for subinstr in instrument[instr][0]:
                if subinstr == "Coordinating body for climate strategy":
                    cp_instrument[subinstr] = ['No', 'Government Provision of Public Goods or Services', '']
                else:
                    cp_instrument[subinstr] = ['', '', '']

        if instr == "Economic instruments":
            cp_instrument[instr] = ['', '', '']
            for subinstr in instrument[instr][0]:
                if subinstr == "Direct investment":
                    cp_instrument[subinstr] = ['No', 'Government Provision of Public Goods or Services', '']
                    for i in instrument[instr][0][subinstr]:
                        if i == "Funds to sub-national governments":
                            cp_instrument[i] = ['No', 'Government Provision of Public Goods or Services', '']
                        if i == "Infrastructure investments":
                            cp_instrument[i] = ['Sector', 'Government Provision of Public Goods or Services',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Government Provision of Public Goods or Services:Infrastructure expansion (district heating / cooling or common carrier)",
                                                 "Transport": "Government Provision of Public Goods or Services:Investment in alternative fuel infrastructure",
                                                 "Buildings": "Government Provision of Public Goods or Services:Public procurement of efficient buildings and appliances",
                                                 "Industry": "",
                                                 "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
                        if i == "Procurement rules":
                            cp_instrument[i] = ['Sector',
                                                'Government Provision of Public Goods or Services;Regulatory Approaches',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Government Provision of Public Goods or Services:Infrastructure expansion (district heating / cooling or common carrier)",
                                                 "Transport": "Government Provision of Public Goods or Services:Low emission vehicle procurement",
                                                 "Buildings": "Government Provision of Public Goods or Services:Public procurement of efficient buildings and appliances",
                                                 "Industry": "",
                                                 "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
                        if i == "RD&D funding":
                            cp_instrument[i] = ['No', 'Government Provision of Public Goods or Services',
                                                'Government Provision of Public Goods or Services:Research and development']

                if subinstr == "Fiscal or financial incentives":
                    cp_instrument[subinstr] = ['', '', '']
                    for i in instrument[instr][0][subinstr]:
                        if i == "CO2 taxes":
                            cp_instrument[i] = ['Sector', 'Taxes',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Taxes:Carbon taxes",
                                                 "Transport": "Taxes:Fuel taxes",
                                                 "Buildings": "Taxes:Carbon and/or energy taxes",
                                                 "Industry": "Taxes:Carbon tax or energy tax",
                                                 "AFOLU": ""}]
                        if i == "Energy and other taxes":
                            cp_instrument[i] = ['Sector', 'Taxes',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Taxes:Carbon taxes",
                                                 "Transport": "Taxes:Fuel taxes",
                                                 "Buildings": "Taxes:Carbon and/or energy taxes",
                                                 "Industry": "Taxes:Carbon tax or energy tax",
                                                 "AFOLU": "Taxes:Fertilizer or Nitrogen taxes to reduce nitrous oxide"}]
                        if i == "Feed-in tariffs or premiums":
                            cp_instrument[i] = ['Sector', 'Subsidies',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Subsidies:Feed-in-tariffs for renewable energy",
                                                 "Transport": "",
                                                 "Buildings": "",
                                                 "Industry": "",
                                                 "AFOLU": ""
                                                 }]
                        if i == "Grants and subsidies":
                            cp_instrument[i] = ['No', 'Government Provision of Public Goods or Services;Subsidies', '']
                            # Difficult to determine whether it is Subsidies or Government Provision of Public Goods or Services
                        if i == "Loans":
                            cp_instrument[i] = ['Sector', 'Subsidies',
                                                {"Multi-sector": "",
                                                 "Energy systems": "",
                                                 "Transport": "",
                                                 "Buildings": "Subsidies:Subsidized loans",
                                                 "Industry": "",
                                                 "AFOLU": "Subsidies:Credit lines for low carbon agriculture, sustainable forestry"}]
                        if i == "Retirement premium":
                            cp_instrument[i] = ['No', 'Subsidies', '']
                        if i == "Tax relief":
                            cp_instrument[i] = ['No', 'Subsidies', '']
                        if i == "Tendering schemes":
                            cp_instrument[i] = ['', '', '']
                        if i == "User charges":
                            cp_instrument[i] = ['No', 'Subsidies', '']
                            # Together with Net metering
                if subinstr == "Market-based instruments":
                    cp_instrument[subinstr] = ['', '', '']
                    for i in instrument[instr][0][subinstr]:
                        if i == "GHG emission reduction crediting and offsetting mechanism":
                            # ETS Free allowances; Carbon Credit
                            cp_instrument[i] = ['Sector', 'Tradable Allowances',
                                                {"Multi-sector": "",
                                                 "Energy systems": "",
                                                 "Transport": "Tradable Allowances:Fuel and vehicle standards",
                                                 "Buildings": "Tradable Allowances:Tradable certificates for energy efficiency improvements (white certificates)",
                                                 "Industry": "",
                                                 "AFOLU": ""}]
                        if i == "GHG emissions allowances":
                            cp_instrument[i] = ['Sector', 'Tradable Allowances',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Tradable Allowances:Emissions trading",
                                                 "Transport": "Tradable Allowances:Fuel and vehicle standards",
                                                 "Buildings": "Tradable Allowances:Tradable certificates for energy efficiency improvements (white certificates)",
                                                 "Industry": "Tradable Allowances:Emissions trading",
                                                 "AFOLU": "Tradable Allowances:Emission credis under CDM"}]
                        if i == "Green certificates":
                            cp_instrument[i] = ['Sector', 'Tradable Allowances',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Tradable Allowances:Tradable Green Certificates",
                                                 "Transport": "",
                                                 "Buildings": "",
                                                 "Industry": "Tradable Allowances:Tradable Green Certificates",
                                                 "AFOLU": ""}]
                        if i == "White certificates":
                            cp_instrument[i] = ['Sector', 'Tradable Allowances',
                                                {"Multi-sector": "",
                                                 "Energy systems": "",
                                                 "Transport": "",
                                                 "Buildings": "Tradable Allowances:Tradable certificates for energy efficiency improvements (white certificates)",
                                                 "Industry": "",
                                                 "AFOLU": ""}]

        if instr == "Information and education":
            cp_instrument[instr] = ['', '', '']
            for subinstr in instrument[instr][0]:
                if subinstr == "Advice or aid in implementation":
                    cp_instrument[subinstr] \
                        = ['Sector', 'Information Programmes',
                           {"Multi-sector": "",
                            "Energy systems": "",
                            "Transport": "",
                            "Buildings": "Information Programmes:Energy advice programmes",
                            "Industry": "",
                            "AFOLU": ""}]
                if subinstr == "Information provision":
                    cp_instrument[subinstr] \
                        = ['No', 'Information Programmes', '']
                if subinstr == "Performance label":
                    cp_instrument[subinstr] = ['Sector', 'Information Programmes',
                                               {"Multi-sector": "",
                                                "Energy systems": "",
                                                "Transport": "Information Programmes:Vehicle efficiency labelling",
                                                "Buildings": "Information Programmes:Labelling programmes",
                                                "Industry": "",
                                                "AFOLU": ""}]
                    for i in instrument[instr][0][subinstr]:
                        if i:
                            cp_instrument[i] = ['Sector', 'Information Programmes',
                                                {"Multi-sector": "",
                                                 "Energy systems": "",
                                                 "Transport": "Information Programmes:Fuel labelling",
                                                 "Buildings": "Information Programmes:Labelling programmes",
                                                 "Industry": "",
                                                 "AFOLU": ""}]

                if subinstr == "Professional training and qualification":
                    cp_instrument[subinstr] = ['Sector', 'Government Provision of Public Goods or Services',
                                               {"Multi-sector": "",
                                                "Energy systems": "",
                                                "Transport": "",
                                                "Buildings": "",
                                                "Industry": "Government Provision of Public Goods or Services:Training and education",
                                                "AFOLU": ""}]

        if instr == "Policy support":
            cp_instrument[instr] = ['', '', '']
            for subinstr in instrument[instr][0]:
                if subinstr == "Institutional creation":
                    cp_instrument[subinstr] = ['No', 'Government Provision of Public Goods or Services', '']
                if subinstr == "Strategic planning":
                    cp_instrument[subinstr] = ['No', 'Government Provision of Public Goods or Services', '']

        if instr == "Regulatory Instruments":
            cp_instrument[instr] = ['', '', '']
            for subinstr in instrument[instr][0]:
                if subinstr == "Auditing":
                    cp_instrument[subinstr] = ['Sector', 'Information Programmes',
                                               {"Multi-sector": "",
                                                "Energy systems": "",
                                                "Transport": "",
                                                "Buildings": "Information Programmes:Energy audits",
                                                "Industry": "Information Programmes:Energy audits",
                                                "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
                if subinstr == "Codes and standards":
                    cp_instrument[subinstr] = ['Sector', 'Regulatory Approaches',
                                               {"Multi-sector": "",
                                                "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
                                                "Transport": "Regulatory Approaches:GHG emission performance standards",
                                                "Buildings": "Regulatory Approaches:Building codes and standards",
                                                "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
                                                "AFOLU": "Regulatory Approaches:Air and water pollution control GHG precursors"
                                                }]
                    for i in instrument[instr][0][subinstr]:
                        if i == "Building codes and standards":
                            cp_instrument[i] = ['No', 'Regulatory Approaches',
                                                'Regulatory Approaches:Building codes and standards']
                        if i == "Industrial air pollution standards":
                            cp_instrument[i] = ['Sector', 'Regulatory Approaches',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
                                                 "Transport": "Regulatory Approaches:GHG emission performance standards",
                                                 "Buildings": "",
                                                 "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
                                                 "AFOLU": "Regulatory Approaches:Air and water pollution control GHG precursors"
                                                 }]
                        if i == "Product standards":
                            cp_instrument[i] = ['Sector', 'Regulatory Approaches',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
                                                 "Transport": "Regulatory Approaches:Fuel quality standards",
                                                 "Buildings": "Regulatory Approaches:Equipment and appliance standards",
                                                 "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
                                                 "AFOLU": "Regulatory Approaches:Air and water pollution control GHG precursors"
                                                 }]
                        if i == "Sectoral standards":
                            cp_instrument[i] = ['Sector', 'Information Programmes;Regulatory Approaches',
                                                {"Multi-sector": "",
                                                 "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
                                                 "Transport": "Regulatory Approaches:GHG emission performance standards",
                                                 "Buildings": "Regulatory Approaches:Building codes and standards",
                                                 "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
                                                 "AFOLU": "Regulatory Approaches:Air and water pollution control GHG precursors"
                                                 }]
                        if i == "Vehicle air pollution standards":
                            cp_instrument[i] = ['No', 'Regulatory Approaches',
                                                'Regulatory Approaches:GHG emission performance standards']
                        if i == "Vehicle fuel-economy and emissions standards":
                            cp_instrument[i] = ['No', 'Regulatory Approaches',
                                                'Regulatory Approaches:Fuel economy performance standards;Regulatory Approaches:GHG emission performance standards']
                if subinstr == "Monitoring":
                    cp_instrument[subinstr] = ['Sector', 'Information Programmes',
                                               {"Multi-sector": "",
                                                "Energy systems": "",
                                                "Transport": "",
                                                "Buildings": "Information Programmes:Energy audits",
                                                "Industry": "Information Programmes:Energy audits",
                                                "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
                if subinstr == "Obligation schemes":
                    cp_instrument[subinstr] = ['No', 'Regulatory Approaches', '']
                if subinstr == "Other mandatory requirements":
                    cp_instrument[subinstr] = ['No', 'Regulatory Approaches', '']

        if instr == "Research & Development and Deployment (RD&D)":
            cp_instrument[instr] = ['Sector', 'Government Provision of Public Goods or Services',
                                    {"Multi-sector": "",
                                     "Energy systems": "Government Provision of Public Goods or Services:Research and development",
                                     "Transport": "",
                                     "Buildings": "",
                                     "Industry": "",
                                     "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
            for subinstr in instrument[instr][0]:
                cp_instrument[subinstr] = ['Sector', 'Government Provision of Public Goods or Services',
                                           {"Multi-sector": "",
                                            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
                                            "Transport": "",
                                            "Buildings": "",
                                            "Industry": "",
                                            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
                for i in instrument[instr][0][subinstr]:
                    if i:
                        cp_instrument[i] = ['Sector', 'Government Provision of Public Goods or Services',
                                            {"Multi-sector": "",
                                             "Energy systems": "Government Provision of Public Goods or Services:Research and development",
                                             "Transport": "",
                                             "Buildings": "",
                                             "Industry": "",
                                             "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]

        if instr == "Target":
            cp_instrument[instr] = ['', '', '']
            for subinstr in instrument[instr][0]:
                cp_instrument[subinstr] = ['', '', '']
                for i in instrument[instr][0][subinstr]:
                    if i:
                        cp_instrument[i] = ['', '', '']

        if instr == "Voluntary approaches":
            cp_instrument[instr] = ['No', 'Voluntary Actions', '']
            for subinstr in instrument[instr][0]:
                cp_instrument[subinstr] = ['No', 'Voluntary Actions', '']

    with open('cp_instrument_dict.json', 'w') as f:
        json.dump(cp_instrument, f)
