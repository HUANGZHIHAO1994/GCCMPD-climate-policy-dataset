import pandas as pd
import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':
    df = pd.read_csv("lse.csv")

    # ================== View the instrument classification in lse ==================
    # print(set(df["Instruments"].str.strip().str.replace(";  ", ';').str.replace("; ", ';').str.cat(sep=';').split(';')))
    # print(len(
    #     set(df["Instruments"].str.strip().str.replace(";  ", ';').str.replace("; ", ';').str.cat(sep=';').split(';'))))

    # ================== update database should use set diff ==================
    # df_old = pd.read_csv("lse_old.csv")
    # key_old = set(
    #     df_old["Instruments"].str.strip().str.replace(";  ", ';').str.replace("; ", ';').str.cat(sep=';').split(';'))
    # key_new = set(
    #     df["Instruments"].str.strip().str.replace(";  ", ';').str.replace("; ", ';').str.cat(sep=';').split(';'))
    # print(key_new - key_old)

    # ================== Notes ==================
    # First element of list: judge whether to use Sector to provide a basis for the third
    # First one "" means skip, "No" means No need to use Sector
    # Second element of list: Instrument
    # Third element of list: Sector-Instrument

    lse_instrument = dict()

    lse_instrument["Building codes|Regulation"] \
        = ['No', 'Regulatory Approaches', 'Regulatory Approaches:Building codes and standards']
    lse_instrument["Capacity-building - general|Capacity-building"] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
            "Transport": "",
            "Buildings": "",
            "Industry": "Government Provision of Public Goods or Services:Training and education",
            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
    lse_instrument["Climate fund|Governance and planning"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Creating bodies and institutions|Governance and planning"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Designing processes|Governance and planning"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Developing plans and strategies|Governance and planning"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Subnational and citizen participation|Governance"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["International cooperation|Governance"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Early warning systems|Direct Investment"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Other|Governance"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Disclosure obligations|Regulation"] \
        = ['Sector', 'Information Programmes;Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    lse_instrument["Ecosystem restoration and nature based solutions|Direct investment"] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": "Government Provision of Public Goods or Services:Protection of national, state, and local forests"}]
    lse_instrument["Education and training|Capacity-building"] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Government Provision of Public Goods or Services:Training and education",
            "AFOLU": ""}]
    lse_instrument["Governance and Planning|Creating bodies/institutions"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Planning|Governance"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Provision of climate funds|Direct Investment"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Processes, plans and strategies|Governance"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Governance and Planning|Developing processes"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Education, training and knowledge dissemination|Information"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Governance and Planning|MRV"] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    lse_instrument["Governance and Planning|Monitoring, Reporting, and Verification"] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    lse_instrument["Incentives|Other"] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Subsidies:Fiscal incentives",
            "AFOLU": ""}]
    lse_instrument["Insurance|Incentives"] = ['No', 'Subsidies', '']
    lse_instrument["Insurance|Economic"] = ['No', 'Subsidies', '']
    lse_instrument["International cooperation|Governance and planning"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Knowledge generation|Capacity-building"] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
    lse_instrument["Knowledge sharing and dissemination|Capacity-building"] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
    lse_instrument["Monitoring and evaluation|Governance and planning"] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    lse_instrument["Monitoring, Reporting, Verification|Governance and planning"] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    lse_instrument["Multi-level governance|Governance and planning"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Provision of climate finance|Direct investment"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Other|Direct Investment"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Nature based solutions and ecosystem restoration|Direct Investment"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Research & Development, knowledge generation|Information"] \
        = ['No', 'Government Provision of Public Goods or Services;Information Programmes', '']
    lse_instrument["Public goods - early warning systems|Direct investment"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Public goods - other|Direct investment"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Capacity building|Governance"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Regulation|Standards & obligations"] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "Regulatory Approaches:GHG emission performance standards",
            "Buildings": "Regulatory Approaches:Building codes and standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": "Regulatory Approaches:Air and water pollution control GHG precursors"
            }]
    lse_instrument["Research and development|Capacity-building"] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
    lse_instrument["Social safety nets|Direct investment"] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Standards and obligations|Regulation"] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "Regulatory Approaches:GHG emission performance standards",
            "Buildings": "Regulatory Approaches:Building codes and standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": "Regulatory Approaches:Air and water pollution control GHG precursors"
            }]
    lse_instrument["Subsidies|Economic"] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Subsidies:Fiscal incentives",
            "AFOLU": ""}]
    lse_instrument["Subsidies|Incentives"] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Subsidies:Fiscal incentives",
            "AFOLU": ""}]
    lse_instrument["Taxes|Incentives"] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Subsidies:Fiscal incentives",
            "AFOLU": ""}]
    lse_instrument["Tax incentives|Economic"] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Subsidies:Fiscal incentives",
            "AFOLU": ""}]
    lse_instrument["Zoning and spatial planning|Regulation"] = ['No', 'Regulatory Approaches', '']
    lse_instrument["Institutional mandates|Governance"] = ['No', 'Regulatory Approaches', '']
    lse_instrument["Zoning & Spatial Planning|Regulation"] = ['No', 'Regulatory Approaches', '']
    lse_instrument["Standards, obligations and norms|Regulation"] = ['No', 'Regulatory Approaches', '']
    lse_instrument["Moratoria & bans|Regulation"] = ['No', 'Regulatory Approaches', '']
    lse_instrument["Other|Economic"] = ['', '', '']
    lse_instrument["Climate finance tools|Economic"] = ['No', 'Government Provision of Public Goods or Services', '']
    lse_instrument["Standards, obligations and norms|Regulation"] = ['No', 'Regulatory Approaches', '']
    lse_instrument['MRV|Governance'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    lse_instrument['Carbon pricing & emissions trading|Economic'] \
        = ['Sector', 'Tradable Allowances',
           {"Multi-sector": "",
            "Energy systems": "Tradable Allowances:Emissions trading",
            "Transport": "Tradable Allowances:Fuel and vehicle standards",
            "Buildings": "Tradable Allowances:Tradable certificates for energy efficiency improvements (white certificates)",
            "Industry": "Tradable Allowances:Emissions trading",
            "AFOLU": "Tradable Allowances:Emission credis under CDM"}]
    lse_instrument['Green procurement|Direct Investment'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Infrastructure expansion (district heating / cooling or common carrier)",
            "Transport": "Government Provision of Public Goods or Services:Investment in alternative fuel infrastructure",
            "Buildings": "Government Provision of Public Goods or Services:Public procurement of efficient buildings and appliances",
            "Industry": "",
            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]

    with open('lse_instrument_dict.json', 'w') as f:
        json.dump(lse_instrument, f)
