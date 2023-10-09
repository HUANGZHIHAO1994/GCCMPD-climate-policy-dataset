import pandas as pd
import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':
    df = pd.read_excel("iea.xlsx")

    # ================== View the sector classification in IEA ==================
    # print(set(df["Sectors"].str.cat(sep=';').split(';')))
    # print(len(set(df["Sectors"].str.cat(sep=';').split(';'))))

    # ================== Notes ==================
    # First element of list: Sector
    # Second element of list: Sub-sector
    # First one "" means skip, such as Demand response can be electricity or transport, invalid judgment
    # Second one "" means only Sector

    iea_sector = dict()
    iea_sector['Economy-wide (Multi-sector)'] = ['Multi-sector', '']
    iea_sector['Accomodation and food services'] = ['Buildings', 'Buildings:Non-residential']
    iea_sector['Administration and offices'] = ['Buildings', 'Buildings:Non-residential']
    iea_sector['Agriculture'] = ['AFOLU', '']
    iea_sector['Agriculture, Fisheries, Forestry and Hunting'] = ['AFOLU', '']
    iea_sector['Air transport'] = ['Transport', 'Transport:Domestic Aviation']
    iea_sector['Ammonia'] = ['Industry', 'Industry:Chemicals']
    # Ammonia production (gross CO2)
    # CO2-ammonia stored in urea
    iea_sector['Appartment in high-rise building'] = ['Buildings', 'Buildings:Residential']
    iea_sector['Appartment in low-rise building'] = ['Buildings', 'Buildings:Residential']
    iea_sector['Attached house'] = ['Buildings', 'Buildings:Residential']
    iea_sector['Biodiesel'] = ['Transport', '']
    # Also could be Energy systems: Oil production (biom.)
    iea_sector['Bioethanol'] = ['Transport', '']
    # Also could be Industry: Chemicals
    iea_sector['Biofuel production'] = ['Transport', '']
    # Also could be Energy systems: Oil production (biom.)
    iea_sector['Buildings'] = ['Buildings', '']
    iea_sector['Buses - Rapid transit and intercity service'] = ['Transport', 'Transport:Road']
    iea_sector['Buses and minibuses - Local and urban service'] = ['Transport', 'Transport:Road']
    iea_sector['Chemical and petrochemicals'] = ['Industry', 'Industry:Chemicals']
    iea_sector['Coal and lignite mining'] = ['Energy systems', 'Energy systems:Coal mining fugitive emissions']
    iea_sector['Coal secondary products production'] = ['Energy systems',
                                                        'Energy systems:Coal mining fugitive emissions']
    # Fuel transformation of solid fuels (BKB Plants, coal liquefaction, patent fuel plants)
    iea_sector['Combined heat and power'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Construction'] = ['Buildings', '']
    # Buildings or Industry depends on other tags
    iea_sector['Cooling production and distribution (incl. district cooling)'] \
        = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['CO2 capture'] = ['', '']
    iea_sector['CO2 transport, utilisation and storage'] = ['', '']
    iea_sector['Data centre'] = ['', '']
    iea_sector['Delivery freight (Road)'] = ['Transport', 'Transport:Road']
    iea_sector['Demand response'] = ['', '']
    iea_sector['Detached house'] = ['Buildings', 'Buildings:Residential']
    iea_sector['Distribution'] = ['', '']
    iea_sector['Domestic freight (Water)'] = ['Transport', 'Transport:Inland Shipping']
    iea_sector['Domestic passenger (Air)'] = ['Transport', 'Transport:Domestic Aviation']
    iea_sector['Downstream'] = ['', '']

    iea_sector['Education'] = ['', '']
    iea_sector['Electricity and heat generation'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Electricity distribution'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Electricity transmission'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Existing buildings and retrofits'] = ['Buildings', '']
    iea_sector['Exploration, drilling, well development and extraction'] \
        = ['Industry', 'Industry:Other industry']
    # Off-road machinery: mining (diesel)
    iea_sector['Fisheries'] = ['AFOLU', '']
    iea_sector['Food and tobacco'] = ['Industry', 'Industry:Other industry']
    iea_sector['Food retail'] = ['Industry', '']
    # refrigerators
    iea_sector['Forestry'] = ['AFOLU', '']
    iea_sector['Forestry and Hunting'] = ['AFOLU', '']
    iea_sector['Fossil fuel production'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    iea_sector['Freight transport (Air)'] = ['Transport', 'Transport:Domestic Aviation']
    iea_sector['Freight transport (Rail)'] = ['Transport', 'Transport:Rail']
    iea_sector['Freight transport (Road)'] = ['Transport', 'Transport:Road']
    iea_sector['Freight transport (Water)'] = ['Transport', 'Transport:Inland Shipping']
    iea_sector['Fuel gathering and pre-refining processing (including bitumen upgrading)'] \
        = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    iea_sector['Fuel processing and transformation'] = ['Energy systems',
                                                        'Energy systems:Oil and gas fugitive emissions']
    iea_sector['Health and social activities'] = ['', '']
    iea_sector['Heat and Utilities'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Heat and steam distribution (incl. district heating)'] \
        = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Heat generation'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Heating and Cooling'] = ['Buildings', '']
    # household appliances, Not grid or system
    iea_sector['High value chemicals'] = ['Industry', 'Industry:Chemicals']

    # may be a Multi-sector: Energy systems; Industry; Transport
    iea_sector['Hydrogen production'] = ['Multi-sector', '']
    iea_sector['Hydrogen production and supply'] = ['Multi-sector', '']
    iea_sector['Hydrogen storage'] = ['Multi-sector', '']

    iea_sector['Hydrogen transportation'] \
        = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    # Gas transmission
    iea_sector['Industry'] = ['Industry', '']
    iea_sector['Intercity rail'] = ['Transport', 'Transport:Rail']
    iea_sector['International freight (Water)'] = ['Transport', 'Transport:International Shipping']
    iea_sector['International freight (Air)'] = ['Transport', 'Transport:International Aviation']
    iea_sector['International passenger (Air)'] = ['Transport', 'Transport:International Aviation']
    iea_sector['Investment in start-ups'] = ['', '']
    iea_sector['Iron and steel'] = ['Industry', 'Industry:Metals']
    iea_sector['LNG transportation'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    # Gas transmission
    iea_sector['Liquefaction'] = ['Energy systems', 'Energy systems:Coal mining fugitive emissions']
    # Fuel transformation of gaseous fuels (GTL, Blend, (re-)gasif./Liquef., NSF)
    iea_sector['Machinery'] = ['Industry', 'Industry:Other industry']
    iea_sector['Manufacturing'] = ['Industry', '']
    iea_sector['Mass road transit'] = ['Transport', 'Transport:Road']
    iea_sector['Metal ore mining'] = ['Industry', 'Industry:Metals']
    iea_sector['Methanol'] = ['Industry', 'Industry:Chemicals']
    iea_sector['Mining and quarrying (incl. fossil fuel extraction)'] \
        = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    # IEA classifies it as Industry
    # Off-road machinery: mining (diesel)
    iea_sector['Multipurpose'] = ['', '']
    iea_sector['Natural gas'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    iea_sector['Natural gas processing'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    iea_sector['New buildings'] = ['Buildings', '']
    iea_sector['Offshore'] = ['', '']
    iea_sector['Oil and natural gas extraction'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    iea_sector['Oil and natural gas secondary products production'] \
        = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']

    # Only appear once
    iea_sector['Onshore - Conventional'] = ['', '']
    iea_sector['Onshore - Unconventional'] = ['', '']

    iea_sector['Other light manufacturing'] = ['Industry', 'Industry:Other industry']
    iea_sector['Paper, pulp and printing'] = ['Industry', 'Industry:Other industry']
    iea_sector['Passenger transport (Air)'] = ['Transport', 'Transport:Domestic Aviation']
    iea_sector['Passenger transport (Rail)'] = ['Transport', 'Transport:Rail']
    iea_sector['Passenger transport (Road)'] = ['Transport', 'Transport:Road']
    iea_sector['Pipeline transportation'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    iea_sector['Plant-based'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Power'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Power generation'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Power storage'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Power transmission and distribution'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Power, Heat and Utilities'] = ['Energy systems', 'Energy systems:Electricity & heat']
    iea_sector['Private - Individual (Road)'] = ['Transport', 'Transport:Road']
    iea_sector['Private transport companies (incl. taxis and VTCs)'] = ['Transport', 'Transport:Road']
    iea_sector['Processing'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    iea_sector['Public administration'] = ['Buildings', 'Buildings:Non-residential']
    iea_sector['Public assembly'] = ['Buildings', 'Buildings:Non-residential']
    iea_sector['Rail transport'] = ['Transport', 'Transport:Rail']
    iea_sector['Refining'] = ['Energy systems', 'Energy systems:Petroleum refining']
    iea_sector['Regasification'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    iea_sector['Repair'] = ['Buildings', '']
    iea_sector['Repair, industrial and other service activities'] = ['Buildings', '']
    iea_sector['Residential'] = ['Buildings', 'Buildings:Residential']
    iea_sector['Restaurants'] = ['Buildings', 'Buildings:Non-residential']
    iea_sector['Road transport'] = ['Transport', 'Transport:Road']
    iea_sector['SMEs'] = ['', '']
    iea_sector['Services'] = ['Buildings', 'Buildings:Non-residential']
    iea_sector['Sewerage, waste and remediation'] = ['Industry', 'Industry:Waste']
    iea_sector['Storage'] = ['', '']
    iea_sector['Textile and leather'] = ['Industry', 'Industry:Other industry']
    iea_sector['Transmission'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    # Gas transmission; Oil transmission
    iea_sector['Transport'] = ['Transport', '']
    iea_sector['Transport equipment'] = ['Transport', '']
    iea_sector['Upstream'] = ['', '']
    iea_sector['Urban and suburban rail'] = ['Transport', 'Transport:Rail']
    iea_sector['Water supply'] = ['', '']
    iea_sector['Water transport'] = ['Transport', 'Transport:Inland Shipping']
    iea_sector['Wholesale and retail'] = ['', '']
    iea_sector['industrial and other service activities'] = ['Buildings', '']
    iea_sector['Oil'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    iea_sector['CO2 transport, utilisation and storage'] = ['', '']
    iea_sector['utilisation and storage'] = ['', '']
    iea_sector['CO2 transport'] = ['', '']
    iea_sector['Information & communication'] = ['', '']
    iea_sector['Non-ferrous metals'] = ['Industry', 'Industry:Metals']
    iea_sector['Aluminium'] = ['Industry', 'Industry:Metals']
    iea_sector['Intercity road freight (Road)'] = ['Transport', 'Transport:Road']
    iea_sector['Vehicle sharing and pooling companies'] = ['Transport', 'Transport:Road']
    iea_sector['Warehousing and support for transportation activities'] = ['Transport', '']
    iea_sector['Animal-based'] = ['AFOLU', '']
    iea_sector['Non-metallic minerals'] = ['Industry', 'Industry:Other industry']
    iea_sector['Exploration'] = ['Industry', 'Industry:Other industry']
    iea_sector['drilling'] = ['Industry', 'Industry:Other industry']
    iea_sector['well development and extraction'] = ['Industry', 'Industry:Other industry']
    # Off-road machinery: mining (diesel)

    with open('iea_sector_dict.json', 'w') as f:
        json.dump(iea_sector, f)

    # ================== In doubt, manual verification is required ==================

    # iea_sector['Air transport'] = ['Transport', 'Transport:Domestic Aviation']
    # iea_sector['Freight transport (Air)'] = ['Transport', 'Transport:Domestic Aviation']

    # iea_sector['Cooling production and distribution (incl. district cooling)'] \
    #     = ['Energy systems', 'Energy systems:Electricity & heat']
    # iea_sector['Biodiesel'] = ['Energy systems', 'Energy systems:Biomass energy systems']  # Oil production (biom.)
    # iea_sector['Bioethanol'] = ['Industry', 'Industry:Chemicals']
    # iea_sector['Biofuel production'] = ['Energy systems', 'Energy systems:Biomass energy systems']
    # iea_sector['Hydrogen transportation'] = ['Energy systems', 'Energy systems:Oil and gas fugitive emissions']
    # iea_sector['Plant-based'] = ['AFOLU', 'AFOLU:Fuel combustion']
    # iea_sector['Transport equipment'] = ['Transport', '']
    # iea_sector['industrial and other service activities'] = ['Buildings', '']
