import pandas as pd
import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':
    df = pd.read_excel("iea_sector_result.xlsx")

    # ================== View the instrument classification in iea ==================
    # print(set(df["Type"].str.cat(sep=';').split(';')))
    # print(len(set(df["Type"].str.cat(sep=';').split(';'))))

    # ================== update database should use set diff ==================
    # df_old = pd.read_excel("IEA_All_Policies.xlsx")
    # key_old = set(df_old["Type"].str.cat(sep=';').split(';'))
    # key_new = set(df["Type"].str.cat(sep=';').split(';'))
    # print(key_new - key_old)

    # ================== Notes ==================
    # First element of list: judge whether to use Sector to provide a basis for the third
    # First one "" means skip, "No" means No need to use Sector
    # Second element of list: Instrument
    # Third element of list: Sector-Instrument

    sector = {"Multi-sector": "", "Energy systems": "", "Transport": "", "Buildings": "", "Industry": "", "AFOLU": ""}

    iea_instrument = dict()
    iea_instrument['Accelerated depreciation'] = ['No', 'Subsidies', '']
    iea_instrument['Associated pollutant limitations (SOx, VOCs, etc.)'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "",
            "Buildings": "",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""
            }]
    iea_instrument['Audits and inspections'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    iea_instrument['Awards'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Building code (Prescriptive)'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Regulatory Approaches:Building codes and standards",
            "Industry": "",
            "AFOLU": ""
            }]
    iea_instrument['Building codes (performance-based)'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Regulatory Approaches:Building codes and standards",
            "Industry": "",
            "AFOLU": ""
            }]
    iea_instrument['Building codes and standards'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Regulatory Approaches:Building codes and standards",
            "Industry": "",
            "AFOLU": ""
            }]
    iea_instrument['Business accelerators / Incubators'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Government Provision of Public Goods or Services:Brokerage for industrial cooperation",
            "AFOLU": ""}]
    iea_instrument['Business activity surveys'] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    # iea_instrument['Capacity auction'] \
    #     = ['No', 'Regulatory Approaches', 'Regulatory Approaches:Equitable access to electricity grid']
    iea_instrument['Capacity auction'] = ['', '', '']
    # Just one form of implementation of policy tools, which may be Subsidies or Regulatory Approaches

    iea_instrument['Carbon tax'] \
        = ['Sector', 'Taxes',
           {"Multi-sector": "",
            "Energy systems": "Taxes:Carbon taxes",
            "Transport": "",
            "Buildings": "Taxes:Carbon and/or energy taxes",
            "Industry": "Taxes:Carbon tax or energy tax",
            "AFOLU": ""}]
    iea_instrument['Climate change strategies'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Co-funding via investment fund'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Codes and standards'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""}]
    iea_instrument['Company car tax'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    iea_instrument['Comparison labels'] = ['No', 'Information Programmes', '']
    iea_instrument['Compliance requirements'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Congestion charge'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    # iea_instrument['Congestion charge'] \
    #     = ['Sector', 'Taxes',
    #        {"Multi-sector": "",
    #         "Energy systems": "",
    #         "Transport": "Taxes:Congestion charges, vehicle registration fees, road tolls",
    #         "Buildings": "",
    #         "Industry": "",
    #         "AFOLU": ""}]
    iea_instrument['Contracts for difference'] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    # support for R&D

    iea_instrument['Consumer information'] = ['No', 'Information Programmes', '']
    iea_instrument['Education and training'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Government Provision of Public Goods or Services:Training and education",
            "AFOLU": ""}]
    iea_instrument['Emission Trading Scheme'] \
        = ['Sector', 'Tradable Allowances',
           {"Multi-sector": "",
            "Energy systems": "Tradable Allowances:Emissions trading",
            "Transport": "Tradable Allowances:Fuel and vehicle standards",
            "Buildings": "Tradable Allowances:Tradable certificates for energy efficiency improvements (white certificates)",
            "Industry": "Tradable Allowances:Emissions trading",
            "AFOLU": "Tradable Allowances:Emission credis under CDM"}]
    iea_instrument['Emission standards'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "Regulatory Approaches:GHG emission performance standards",
            "Buildings": "",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": "Regulatory Approaches:Air and water pollution control GHG precursors"
            }]
    iea_instrument['Emissions estimates'] = ['No', 'Information Programmes', '']
    iea_instrument['Endorsement labels'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Labelling programmes",
            "Industry": "",
            "AFOLU": "Information Programmes:Certification schemes for sustainable forest practices"}]
    iea_instrument['Energy / CO2 performance certification: Comparison'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Labelling programmes",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    iea_instrument['Energy / CO2 performance labels'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Labelling programmes",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    # iea_instrument['Energy auction'] \
    #     = ['Sector', 'Tradable Allowances;Regulatory Approaches',
    #        {"Multi-sector": "",
    #         "Energy systems": "Tradable Allowances:Emissions trading;Regulatory Approaches:Equitable access to electricity grid",
    #         "Transport": "Tradable Allowances:Fuel and vehicle standards",
    #         "Buildings": "Tradable Allowances:Tradable certificates for energy efficiency improvements (white certificates)",
    #         "Industry": "Tradable Allowances:Emissions trading",
    #         "AFOLU": "Tradable Allowances:Emission credis under CDM"}]
    iea_instrument['Energy auction'] = ['', '', '']
    # Just one form of implementation of Instruments, may be Subsidies Tradable Allowances or Regulatory Approaches
    iea_instrument['Energy efficiency / Fuel economy obligations'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "Regulatory Approaches:Fuel economy performance standards",
            "Buildings": "Regulatory Approaches:Mandates for energy retailers to assist customers invest in energy efficiency",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""
            }]
    iea_instrument['Energy market regulation'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Energy trading regulations'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Enforcement'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Environmental Impact Assessment'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Environmental impact assessment'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Equipment sales obligation'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "",
            "Buildings": "Regulatory Approaches:Equipment and appliance standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""
            }]
    iea_instrument['Equity'] = ['', '', '']
    iea_instrument['Excise taxes'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    iea_instrument['Externality taxation'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    iea_instrument['Feebate'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Subsidies:Feebates",
            "Buildings": "",
            "Industry": "",
            "AFOLU": ""
            }]
    iea_instrument['Feed-in tariffs/premiums'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "Subsidies:Feed-in-tariffs for renewable energy",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": ""}]
    iea_instrument['Finance'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Framework legislation'] = ['No', 'Government Provision of Public Goods or Services', '']
    # iea_instrument['Fuel quality standards'] = ['No', 'Regulatory Approaches',
    #                                             'Regulatory Approaches:Fuel quality standards']
    iea_instrument['Fuel quality standards'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Regulatory Approaches:Fuel quality standards",
            "Buildings": "",
            "Industry": "",
            "AFOLU": ""
            }]
    iea_instrument['Funds to sub-national governments'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['GHG taxation'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    # iea_instrument['GHG emissions liability'] \
    #     = ['Sector', 'Regulatory Approaches',
    #        {"Multi-sector": "",
    #         "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
    #         "Transport": "Regulatory Approaches:GHG emission performance standards",
    #         "Buildings": "",
    #         "Industry": "",
    #         "AFOLU": ""
    #         }]
    iea_instrument['GHG emissions liability'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Government provided advice'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Information Programmes:Energy advice programmes",
            "Industry": "",
            "AFOLU": ""}]
    iea_instrument['Grants'] = ['No', 'Government Provision of Public Goods or Services', '']
    # Sometimes Subsidies are included

    iea_instrument['Import tax'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    iea_instrument['Inducement prizes'] = ['No', 'Government Provision of Public Goods or Services', '']
    # Sometimes Subsidies are included

    iea_instrument['Industrial clusters'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Government Provision of Public Goods or Services:Brokerage for industrial cooperation",
            "AFOLU": ""}]
    iea_instrument['Information and education'] \
        = ['No', 'Government Provision of Public Goods or Services;Information Programmes', '']
    iea_instrument['Information campaigns'] = ['No', 'Information Programmes', '']
    iea_instrument['Insurance'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "Subsidies:Capital subsidies and insurance for 1st generation Carbon Dioxide Capture and Storage (CCS)",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": ""}]
    iea_instrument['Intellectual property regimes'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['International collaboration'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Investment in start-ups'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Investment in assets'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Infrastructure expansion (district heating / cooling or common carrier)",
            "Transport": "Government Provision of Public Goods or Services:Investment in alternative fuel infrastructure",
            "Buildings": "Government Provision of Public Goods or Services:Public procurement of efficient buildings and appliances",
            "Industry": "",
            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
    iea_instrument['Investment tax incentives'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Subsidies:Fiscal incentives",
            "AFOLU": ""}]

    # Capacity building
    iea_instrument['Knowledge networks'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
    iea_instrument['Knowledge sharing'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
    iea_instrument['Knowledge sharing requirements'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
    iea_instrument['Leak detection and repair requirements'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Loan guarantee'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Subsidies:Subsidized loans",
            "Industry": "",
            "AFOLU": "Subsidies:Credit lines for low carbon agriculture, sustainable forestry"}]
    iea_instrument['Loans (incl. concessional loans)'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Subsidies:Subsidized loans",
            "Industry": "",
            "AFOLU": "Subsidies:Credit lines for low carbon agriculture, sustainable forestry"}]
    iea_instrument['Loans / debt finance'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Subsidies:Subsidized loans",
            "Industry": "",
            "AFOLU": "Subsidies:Credit lines for low carbon agriculture, sustainable forestry"}]
    iea_instrument['Long-term low emissions development strategy (LT-LEDS)'] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Luxury tax'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    iea_instrument['Major infrastructure plan'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Infrastructure expansion (district heating / cooling or common carrier)",
            "Transport": "Government Provision of Public Goods or Services:Investment in alternative fuel infrastructure",
            "Buildings": "Government Provision of Public Goods or Services:Public procurement of efficient buildings and appliances",
            "Industry": "",
            "AFOLU": ""}]
    iea_instrument['Mandatory energy management system'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Regulatory Approaches:Energy management systems",
            "AFOLU": ""}]
    iea_instrument['Mandatory reporting'] \
        = ['Sector', 'Information Programmes;Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    iea_instrument['Mandatory technology use'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "Regulatory Approaches:Fuel quality standards",
            "Buildings": "",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""}]
    iea_instrument['Market design rules'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Matchmaking between investors and firms'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Government Provision of Public Goods or Services:Brokerage for industrial cooperation",
            "AFOLU": ""}]
    iea_instrument['Measurement, calibration, equipment requirements'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Regulatory Approaches:Equipment and appliance standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""}]
    iea_instrument['Metering and connection requirements'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Minimum energy performance standards'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "Regulatory Approaches:Fuel economy performance standards",
            "Buildings": "Regulatory Approaches:Equipment and appliance standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""
            }]
    iea_instrument['Monitoring'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    iea_instrument['National climate change strategy'] = ['', '', '']
    iea_instrument['Nationally Determined Contribution'] = ['', '', '']
    iea_instrument['Negotiated agreements (public-private sector)'] = ['No', 'Voluntary Actions', '']
    iea_instrument['Notice requirements'] = ['No', 'Information Programmes;Regulatory Approaches', '']
    iea_instrument['Obligations on average types of sales / output'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['On-bill finance'] = ['', '', '']
    iea_instrument['Operational funding for institutions'] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Other polluant liabilities'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Other regulatory instruments'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Parking charges'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    # iea_instrument['Parking charges'] \
    #     = ['Sector', 'Taxes',
    #        {"Multi-sector": "",
    #         "Energy systems": "",
    #         "Transport": "Taxes:Congestion charges, vehicle registration fees, road tolls",
    #         "Buildings": "",
    #         "Industry": "",
    #         "AFOLU": ""}]
    iea_instrument['Payments'] = ['', '', '']
    iea_instrument['Payments and transfers'] = ['', '', '']
    iea_instrument['Payments, finance and taxation'] = ['', '', '']
    iea_instrument['Peer-to-peer trading rules'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Performance-based payments'] = ['', '', '']
    iea_instrument['Performance-based policies'] = ['', '', '']
    # may be Subsidies Tradable Allowances or Regulatory Approaches

    iea_instrument['Permitting processes'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Pollution liability'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Pollution rights'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Prescriptive requirements and standards'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "",
            "Buildings": "Regulatory Approaches:Equipment and appliance standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""
            }]
    iea_instrument['Prevenative maintenance requirements'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Primary / Secondary education'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
            "Transport": "",
            "Buildings": "",
            "Industry": "Government Provision of Public Goods or Services:Training and education",
            "AFOLU": ""}]
    iea_instrument['Price controls (incl. social tariffs)'] = ['', '', '']
    iea_instrument['Procedural requirements'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Product certification'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    iea_instrument['Product taxation'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    iea_instrument['Product-based MEPS'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "Regulatory Approaches:Fuel economy performance standards",
            "Buildings": "Regulatory Approaches:Equipment and appliance standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""
            }]
    iea_instrument['Product import or sales bans'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Professional / Vocational training and certification'] \
        = ['Sector', 'Information Programmes;Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Research and development",
            "Transport": "",
            "Buildings": "",
            "Industry": "Government Provision of Public Goods or Services:Training and education",
            "AFOLU": ""}]
    iea_instrument['Prohibition'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Public disclosure requirements'] \
        = ['Sector', 'Information Programmes;Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits;Regulatory Approaches:Labelling and public procurement regulations",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    iea_instrument['Public information'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    iea_instrument['Public procurement'] \
        = ['Sector', 'Government Provision of Public Goods or Services',
           {"Multi-sector": "",
            "Energy systems": "Government Provision of Public Goods or Services:Infrastructure expansion (district heating / cooling or common carrier)",
            "Transport": "Government Provision of Public Goods or Services:Low emission vehicle procurement",
            "Buildings": "Government Provision of Public Goods or Services:Public procurement of efficient buildings and appliances",
            "Industry": "",
            "AFOLU": ""}]
    iea_instrument['Public voluntary programmes'] \
        = ['Sector', 'Voluntary Actions',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "",
            "Industry": "Voluntary Actions:Voluntary agreements on energy targets or adoption of energy management systems, or resource efficiency",
            "AFOLU": "Voluntary Actions:Promotion of sustainability by developing standards and educational campaigns"}]
    iea_instrument['Rebates'] = ['No', 'Subsidies', '']
    iea_instrument['Recordkeeping requirements'] = ['No', 'Information Programmes;Regulatory Approaches', '']
    iea_instrument['Regulation'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Renewable / Non-fossil energy obligations'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Renewable Portfolio Standards for renewable energy",
            "Transport": "Regulatory Approaches:Fuel quality standards",
            "Buildings": "Regulatory Approaches:Building codes and standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""
            }]
    iea_instrument['Reporting'] = ['No', 'Information Programmes', '']
    iea_instrument['Resource rights'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Resource extraction taxes and royalties'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    # iea_instrument['Resource extraction taxes and royalties'] \
    #     = ['Sector', 'Taxes',
    #        {"Multi-sector": "",
    #         "Energy systems": "Taxes:Carbon taxes",
    #         "Transport": "",
    #         "Buildings": "",
    #         "Industry": "Taxes:Carbon tax or energy tax",
    #         "AFOLU": "Taxes:Fertilizer or Nitrogen taxes to reduce nitrous oxide"}]
    iea_instrument['Rights'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Rights, permits and licenses'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Risk sharing facilities'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Road usage charges'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    # iea_instrument['Road usage charges'] \
    #     = ['Sector', 'Taxes',
    #        {"Multi-sector": "",
    #         "Energy systems": "",
    #         "Transport": "Taxes:Congestion charges, vehicle registration fees, road tolls",
    #         "Buildings": "",
    #         "Industry": "",
    #         "AFOLU": ""}]
    iea_instrument['Safety standards'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "Regulatory Approaches:Fuel quality standards",
            "Buildings": "Regulatory Approaches:Building codes and standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""
            }]
    iea_instrument['Sectoral standards'] \
        = ['Sector', 'Regulatory Approaches',
           {"Multi-sector": "",
            "Energy systems": "Regulatory Approaches:Efficiency or environmental performance standards",
            "Transport": "",
            "Buildings": "Regulatory Approaches:Building codes and standards",
            "Industry": "Regulatory Approaches:Energy efficiency standards for equipment",
            "AFOLU": ""
            }]
    iea_instrument['Standards and laws for Green Bonds'] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Strategic plans'] = ['', '', '']
    iea_instrument['Sustainable finance frameworks'] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Targets'] = ['', '', '']
    iea_instrument['Targets, plans and framework legislation'] \
        = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Tariff design'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "Subsidies:Feed-in-tariffs for renewable energy",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": ""}]
    iea_instrument['Tax credits and exemptions'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "",
            "Buildings": "Subsidies:Subsidies or tax exemptions for investment in efficient buildings, retrofits and products",
            "Industry": "",
            "AFOLU": "Subsidies:Credit lines for low carbon agriculture, sustainable forestry."}]
    iea_instrument['Taxes and charges'] = ['', '', '']
    iea_instrument['Taxes, fees and charges'] = ['', '', '']
    iea_instrument['fees and charges'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    iea_instrument['Technology bans / phase outs'] = ['No', 'Regulatory Approaches', '']
    # iea_instrument['Technology roadmaps'] \
    #     = ['Sector', 'Government Provision of Public Goods or Services',
    #        {"Multi-sector": "",
    #         "Energy systems": "Government Provision of Public Goods or Services:Research and development",
    #         "Transport": "",
    #         "Buildings": "",
    #         "Industry": "",
    #         "AFOLU": "Government Provision of Public Goods or Services:Investment in improvement and diffusion of innovative technologies in agriculture and forestry"}]
    iea_instrument['Technology roadmaps'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Technology testing method'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    iea_instrument['Third party verification'] \
        = ['Sector', 'Information Programmes',
           {"Multi-sector": "",
            "Energy systems": "",
            "Transport": "Information Programmes:Fuel labelling",
            "Buildings": "Information Programmes:Energy audits",
            "Industry": "Information Programmes:Energy audits",
            "AFOLU": "Information Programmes:Information policies to support REDD+ including monitoring, reporting and verification"}]
    iea_instrument['Time-of-use tariffs'] \
        = ['Sector', 'Subsidies',
           {"Multi-sector": "",
            "Energy systems": "Subsidies:Feed-in-tariffs for renewable energy",
            "Transport": "",
            "Buildings": "",
            "Industry": "",
            "AFOLU": ""}]
    iea_instrument['Unilateral commitments (private sector)'] = ['No', 'Voluntary Actions', '']
    iea_instrument['Urban planning'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Use / activity restrictions'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Use and activity charges'] = ['', '', '']
    iea_instrument['Taxes'] = ['No', 'Taxes', '']
    # IEA here is likely to be a tax exemption

    # iea_instrument['Use and activity charges'] \
    #     = ['Sector', 'Taxes',
    #        {"Multi-sector": "",
    #         "Energy systems": "Taxes:Carbon taxes",
    #         "Transport": "Taxes:Congestion charges, vehicle registration fees, road tolls",
    #         "Buildings": "Taxes:Carbon and/or energy taxes",
    #         "Industry": "Taxes:Waste disposal taxes or charges",
    #         "AFOLU": "Taxes:Fertilizer or Nitrogen taxes to reduce nitrous oxide"}]
    iea_instrument['Resource extraction incentives'] = ['No', 'Subsidies', '']
    iea_instrument['Wholesale tariff design'] = ['No', 'Subsidies', '']
    iea_instrument['Value added tax'] = ['No', 'Subsidies', '']
    # IEA here is a tax exemption
    # iea_instrument['Value added tax'] = ['', '', '']
    iea_instrument['Differential tax treatment'] = ['No', 'Subsidies;Taxes', '']
    iea_instrument['Vehicle registration tax'] = ['', '', '']
    # IEA here is likely to be a tax exemption

    # iea_instrument['Vehicle registration tax'] \
    #     = ['Sector', 'Taxes',
    #        {"Multi-sector": "",
    #         "Energy systems": "",
    #         "Transport": "Taxes:Congestion charges, vehicle registration fees, road tolls",
    #         "Buildings": "",
    #         "Industry": "",
    #         "AFOLU": ""}]
    iea_instrument['Voluntary approaches'] = ['No', 'Voluntary Actions', '']
    iea_instrument['Voluntary reporting'] = ['No', 'Voluntary Actions;Information Programmes', '']
    iea_instrument['Minerals list'] = ['No', 'Information Programmes', '']
    iea_instrument['Energy / CO2 performance certification'] = ['No', 'Information Programmes', '']
    iea_instrument['finance and taxation'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Information centres'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['permits and licenses'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['plans and framework legislation'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Measurement requirements'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Regulatory reform'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Scrappage scheme'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Environmental standards'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Company- or facility-level'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Equipment- or process-level'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Preventative maintenance requirements'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Average sales / output based emission standards'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Flexibility service requirements'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Per-unit emission standards'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Per-unit emission standards'] = ['No', 'Regulatory Approaches', '']
    iea_instrument['Flaring/venting (economic)'] = ['', '', '']
    iea_instrument['Flaring/venting (prescriptive)'] = ['', '', '']
    iea_instrument['Flaring/venting (performance)'] = ['', '', '']
    iea_instrument['Minerals security mechanism'] = ['', '', '']
    iea_instrument['Energy storage'] = ['', '', '']
    iea_instrument['Strategic reserves'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Institutions for sustainable finance'] = ['No', 'Government Provision of Public Goods or Services',
                                                              '']
    iea_instrument['Strategic stockpile'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['CO2 storage liability framework'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Due diligence'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['Direct equity investment'] = ['No', 'Government Provision of Public Goods or Services', '']
    iea_instrument['State-owned enterprise'] = ['', '', '']
    iea_instrument['Inclusivity and gender'] = ['', '', '']
    iea_instrument['Geological surveys'] = ['No', 'Government Provision of Public Goods or Services', '']

    with open('iea_instrument_dict.json', 'w') as f:
        json.dump(iea_instrument, f)

    # ================== In doubt, manual verification is required ==================
    # ================== insufficient: No classification of financial-related instruments ==================
    # iea_instrument['Business accelerators / Incubators'] = ['', '', '']
    # iea_instrument['Accelerated depreciation'] = ['', '', '']
    # iea_instrument['Finance'] = ['', '', '']
    # iea_instrument['Equity'] = ['', '', '']
    # iea_instrument['Co-funding via investment fund'] = ['', '', '']
    # iea_instrument['Funds to sub-national governments'] = ['', '', '']
    # iea_instrument['Insurance'] = ['', '', '']
    # iea_instrument['Investment in assets'] = ['', '', '']
    # iea_instrument['Investment tax incentives'] = ['', '', '']
    # iea_instrument['Loan guarantee'] = ['', '', '']
    # iea_instrument['Loans (incl. concessional loans)'] = ['', '', '']
    # iea_instrument['Loans / debt finance'] = ['', '', '']
    # iea_instrument['Matchmaking between investors and firms'] = ['', '', '']
    # iea_instrument['On-bill finance'] = ['', '', '']
    # iea_instrument['Operational funding for institutions'] = ['', '', '']
    # iea_instrument['Pollution liability'] = ['', '', '']
    # iea_instrument['Value added tax'] = ['', '', '']
