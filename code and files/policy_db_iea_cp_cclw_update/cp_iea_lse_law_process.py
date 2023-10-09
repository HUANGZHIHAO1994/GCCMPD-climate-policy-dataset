import re
import pandas as pd
import numpy as np
import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))


def get_dict():
    with open("law_soft_law_strategy_title_dict.json", "r") as f:
        map_title_dict = json.load(f)
    with open("law_soft_law_strategy_content_dict.json", "r") as f:
        map_content_dict = json.load(f)
    return map_title_dict, map_content_dict


def get_cp_data():
    cp_df = pd.read_excel("cp_sector_region_instrument_annex_objective_result.xlsx")
    return cp_df


def get_iea_data():
    iea_df = pd.read_excel("iea_sector_region_instrument_annex_objective_result.xlsx")
    return iea_df


def get_lse_data():
    lse_df = pd.read_excel("lse_sector_region_instrument_annex_objective_result.xlsx")
    return lse_df


def save(df, db):
    with pd.ExcelWriter("{}_sector_region_instrument_annex_objective_law_result.xlsx".format(db)) as writer:
        df.to_excel(writer, index=False)


def lse_law_process(soft_hard_law_title_dict, soft_hard_law_content_dict):
    lse_df = get_lse_data()
    lse_df["Title"].fillna("", inplace=True)
    lse_df["Description"].fillna("", inplace=True)
    lse_df["Type"].fillna("", inplace=True)
    lse_df["Document Types"].fillna("", inplace=True)

    lse_df["Policy Type"] = lse_df["Type"]
    law_strategy_list = ["Other Strategy Plan or Target"] * len(lse_df["Title"].to_list())

    for num, row in lse_df.iterrows():
        if row["Document Types"] in ['Constitution']:
            law_strategy_list[num] = "Constitution"
        elif row["Document Types"] in \
                ['Act', 'Law', 'Decree Law', 'Law, Decree', 'Law, Act', 'Law, Plan', 'Law, Strategy']:
            law_strategy_list[num] = "Law/Act"
        elif row["Document Types"] in \
                ['Royal Decree, Decree Law', 'Royal Decree', 'Decree', 'Decree, Royal Decree',
                 'Directive, Decree/Order/Ordinance', 'Decree/Order/Ordinance', 'Decree, Strategy',
                 'Decree/Order/Ordinance, Strategy, Accord', 'Plan, Decree/Order/Ordinance',
                 'Decree/Order/Ordinance, Strategy']:
            law_strategy_list[num] = "Decree/Order/Ordinance"
        elif row["Document Types"] in \
                ['Decision', 'Eu Decision', 'Eu Directive', 'Eu Regulation, Eu Directive', 'Regulation/Rules',
                 'Directive', 'Eu Regulation', 'Eu Directive, Eu Decision', 'Plan, Regulation/Rules',
                 'Resolution, Regulation/Rules']:
            law_strategy_list[num] = "Regulation/Directive/Decision"
        elif row["Document Types"] in \
                ['Programme, Strategy', 'Programme, Plan', 'Action Plan', 'Radmap', 'Programme',
                 'Action Plan, Strategy', 'Road Map/Vision', 'Road Map/Vision/Agenda', 'Road Map/Vision, Policy',
                 'Plan', 'Plan, Policy', 'Plan, Strategy']:
            law_strategy_list[num] = "Preparatory Instruments"
        elif row["Document Types"] in ['Framework', 'Framework, Policy']:
            law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
        elif row["Document Types"] in \
                ['Policy, Resolution', 'Resolution', 'Resolution, Strategy', 'Plan, Resolution']:
            law_strategy_list[num] = "Steering Instruments"
        else:
            # Title
            policy = row["Title"].lower(). \
                replace("(", ' ').replace(")", ' ').replace(",", ' ').replace("\"", ' ').replace("'", ' '). \
                replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')
            # Content
            policy_content = row["Description"].lower(). \
                replace("(", ' ').replace(")", ' ').replace(",", ' ').replace("\"", ' ').replace("'", ' '). \
                replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')

            break_judge = False
            for hardlaw in ['Constitution', 'International Law', 'Law/Act', 'Decree/Order/Ordinance',
                            'Regulation/Directive/Decision']:
                if break_judge:
                    break
                law_keywords = soft_hard_law_title_dict[hardlaw].lower().split(';')
                for keyword in law_keywords:
                    if ' ' in keyword:
                        if len(re.findall(keyword, policy)) > 0:
                            law_strategy_list[num] = hardlaw
                            break_judge = True
                            break
                    else:
                        if keyword in policy.split(" "):
                            law_strategy_list[num] = hardlaw
                            break_judge = True
                            break

            for softlaw in ["Decisional Notices and Communications", "Steering Instruments", "Preparatory Instruments",
                            "Decisional Guidelines, Codes and Frameworks", "Informative Instruments",
                            "Interpretative Communications and Notices"]:
                if break_judge:
                    break
                softlaw_keywords = soft_hard_law_title_dict[softlaw].lower().split(';')
                for keyword in softlaw_keywords:
                    if ' ' in keyword:
                        if len(re.findall(keyword, policy)) > 0:
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break
                    else:
                        if keyword in policy.split(" "):
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break
            if not break_judge:
                if len(re.findall(r'(?:19|20)\d{2}\s*-\s*(?:19|20)\d{2}\s*', row["Title"].lower())) > 0:
                    law_strategy_list[num] = "Preparatory Instruments"
                elif len(re.findall(r'(?:19|20)\d{2}/\d{2}\s*-\s*(?:19|20)\d{2}/\d{2}\s*', row["Title"].lower())) > 0:
                    law_strategy_list[num] = "Preparatory Instruments"
                # elif "strategy" in row["Title"].lower():
                #     law_strategy_list[num] = "Preparatory Instruments"
                # elif ("aim" in row["Description"].lower()) or ("seek" in row["Description"].lower()) or (
                #         "vision" in row["Description"].lower()):
                #     law_strategy_list[num] = "Preparatory Instruments"

            # hard law "this"/"the" in policy content
            for hl_this in ['Law/Act', 'Decree/Order/Ordinance', 'Regulation/Directive/Decision']:
                if break_judge:
                    break
                if hl_this == 'Law/Act':
                    for i in 'Law/Act/Legislation'.lower().split("/"):
                        if (("the" + " " + i + " ") in policy_content) or (("this" + " " + i + " ") in policy_content):
                            law_strategy_list[num] = hl_this
                            break_judge = True
                            break
                else:
                    for i in hl_this.lower().split("/"):
                        if (("the" + " " + i + " ") in policy_content) or (("this" + " " + i + " ") in policy_content):
                            law_strategy_list[num] = hl_this
                            break_judge = True
                            break

            if not break_judge:
                # distinct: Steering Instruments, Decisional Guidelines, Codes and Frameworks
                # judgement: connection to existing Community law
                for strdcs in ["Steering Instruments", "Decisional Guidelines, Codes and Frameworks"]:
                    if break_judge:
                        break
                    softlaw_content_keywords = soft_hard_law_content_dict[strdcs].lower().split(';')
                    for keyword in softlaw_content_keywords:
                        if break_judge:
                            break
                        if ' ' in keyword:
                            if len(re.findall(keyword, policy)) > 0:
                                for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                                'Decree/Order/Ordinance', 'Regulation/Directive/Decision']:
                                    if break_judge:
                                        break
                                    law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                                    for kw in law_keywords:
                                        if ' ' in kw:
                                            if len(re.findall(kw, policy_content)) > 0:
                                                law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                                break_judge = True
                                                break
                                        else:
                                            if kw in policy_content.split(" "):
                                                law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                                break_judge = True
                                                break

                                if not break_judge:
                                    law_strategy_list[num] = "Steering Instruments"
                                    break_judge = True
                                    break
                        else:
                            if keyword in policy.split(" "):
                                for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                                'Decree/Order/Ordinance', 'Regulation/Directive/Decision']:
                                    if break_judge:
                                        break
                                    law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                                    for kw in law_keywords:
                                        if ' ' in kw:
                                            if len(re.findall(kw, policy_content)) > 0:
                                                law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                                break_judge = True
                                                break
                                        else:
                                            if kw in policy_content.split(" "):
                                                law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                                break_judge = True
                                                break

                                if not break_judge:
                                    law_strategy_list[num] = "Steering Instruments"
                                    break_judge = True
                                    break

            if not break_judge:
                # Soft Law use Policy Content
                for softlaw in ["Steering Instruments", "Decisional Guidelines, Codes and Frameworks",
                                "Decisional Notices and Communications", "Preparatory Instruments",
                                "Informative Instruments", "Interpretative Communications and Notices"]:
                    if break_judge:
                        break

                    if softlaw in ["Steering Instruments", "Decisional Guidelines, Codes and Frameworks"]:
                        softlaw_content_keywords = soft_hard_law_content_dict[softlaw].lower().split(';') + \
                                                   soft_hard_law_title_dict[softlaw].lower().split(';')
                        for keyword in softlaw_content_keywords:
                            if ' ' in keyword:
                                if len(re.findall(keyword, policy_content)) > 0:
                                    for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                                    'Decree/Order/Ordinance', 'Regulation/Directive/Decision',
                                                    'Kyoto protocol']:
                                        if break_judge:
                                            break
                                        if hardlaw == 'Kyoto protocol':
                                            law_keywords = ['kyoto protocol']
                                        else:
                                            law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                                        for kw in law_keywords:
                                            if ' ' in kw:
                                                if len(re.findall(kw, policy_content)) > 0:
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break
                                            else:
                                                if kw in policy_content.split(" "):
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break

                                    if not break_judge:
                                        law_strategy_list[num] = "Steering Instruments"
                                        break_judge = True
                                        break
                            else:
                                if keyword in policy_content.split(" "):
                                    for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                                    'Decree/Order/Ordinance', 'Regulation/Directive/Decision',
                                                    'Kyoto protocol']:
                                        if break_judge:
                                            break
                                        if hardlaw == 'Kyoto protocol':
                                            law_keywords = ['kyoto protocol']
                                        else:
                                            law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                                        for kw in law_keywords:
                                            if ' ' in kw:
                                                if len(re.findall(kw, policy_content)) > 0:
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break
                                            else:
                                                if kw in policy_content.split(" "):
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break

                                    if not break_judge:
                                        law_strategy_list[num] = "Steering Instruments"
                                        break_judge = True
                                        break

                    else:
                        softlaw_content_keywords = soft_hard_law_content_dict[softlaw].lower().split(';')
                        for keyword in softlaw_content_keywords:
                            if ' ' in keyword:
                                if len(re.findall(keyword, policy_content)) > 0:
                                    law_strategy_list[num] = softlaw
                                    break_judge = True
                                    break
                            else:
                                if keyword in policy_content.split(" "):
                                    law_strategy_list[num] = softlaw
                                    break_judge = True
                                    break

    lse_df["law or strategy"] = law_strategy_list
    save(lse_df, "lse")


def iea_law_process(soft_hard_law_title_dict, soft_hard_law_content_dict):
    iea_df = get_iea_data()
    iea_df["Policy"].fillna("", inplace=True)
    iea_df["Policy_Content"].fillna("", inplace=True)
    iea_df["Type"].fillna("", inplace=True)
    law_strategy_list = ["Other Strategy Plan or Target"] * len(iea_df["Policy"].to_list())
    policy_type_list = ["executive"] * len(iea_df["Policy"].to_list())

    for num, row in iea_df.iterrows():
        if row["Country"] == "Australia":
            # Title
            policy = row["Policy"].replace("ACT", 'Australian Capital Territory').lower(). \
                replace("(", ' ').replace(")", ' ').replace(",", ' ').replace("\"", ' ').replace("'", ' '). \
                replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')
            # Content
            policy_content = row["Policy_Content"].replace("ACT", 'Australian Capital Territory').lower(). \
                replace("(", ' ').replace(")", ' ').replace(",", ' ').replace("\"", ' ').replace("'", ' '). \
                replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')
        else:
            # Title
            policy = row["Policy"].lower(). \
                replace("(", ' ').replace(")", ' ').replace(",", ' ').replace("\"", ' ').replace("'", ' '). \
                replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')
            # Content
            policy_content = row["Policy_Content"].lower(). \
                replace("(", ' ').replace(")", ' ').replace(",", ' ').replace("\"", ' ').replace("'", ' '). \
                replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')

        break_judge = False
        for hardlaw in ['Constitution', 'International Law', 'Law/Act', 'Decree/Order/Ordinance',
                        'Regulation/Directive/Decision']:
            if break_judge:
                break
            law_keywords = soft_hard_law_title_dict[hardlaw].lower().split(';')
            for keyword in law_keywords:
                if ' ' in keyword:
                    if len(re.findall(keyword, policy)) > 0:
                        law_strategy_list[num] = hardlaw
                        if hardlaw in ['Constitution', 'International Law', 'Law/Act']:
                            policy_type_list[num] = "legislative"
                        break_judge = True
                        break
                else:
                    if keyword in policy.split(" "):
                        law_strategy_list[num] = hardlaw
                        if hardlaw in ['Constitution', 'International Law', 'Law/Act']:
                            policy_type_list[num] = "legislative"
                        break_judge = True
                        break

        if not break_judge:
            for softlaw in ["Decisional Notices and Communications", "Interpretative Communications and Notices"]:
                if break_judge:
                    break
                softlaw_keywords = soft_hard_law_title_dict[softlaw].lower().split(';')
                for keyword in softlaw_keywords:
                    if ' ' in keyword:
                        if len(re.findall(keyword, policy)) > 0:
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break
                    else:
                        if keyword in policy.split(" "):
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break

        # hard law "this"/"the" in policy content
        for hl_this in ['Law/Act', 'Decree/Order/Ordinance', 'Regulation/Directive/Decision']:
            if break_judge:
                break
            if hl_this == 'Law/Act':
                for i in 'Law/Act/Legislation'.lower().split("/"):
                    if (("the" + " " + i + " ") in policy_content) or (("this" + " " + i + " ") in policy_content):
                        law_strategy_list[num] = hl_this
                        policy_type_list[num] = "legislative"
                        break_judge = True
                        break
            else:
                for i in hl_this.lower().split("/"):
                    if (("the" + " " + i + " ") in policy_content) or (("this" + " " + i + " ") in policy_content):
                        law_strategy_list[num] = hl_this
                        break_judge = True
                        break

        if not break_judge:
            for softlaw in ["Steering Instruments", "Preparatory Instruments",
                            "Decisional Guidelines, Codes and Frameworks", "Informative Instruments"]:
                if break_judge:
                    break
                softlaw_keywords = soft_hard_law_title_dict[softlaw].lower().split(';')
                for keyword in softlaw_keywords:
                    if ' ' in keyword:
                        if len(re.findall(keyword, policy)) > 0:
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break
                    else:
                        if keyword in policy.split(" "):
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break
            if not break_judge:
                if len(re.findall(r'(?:19|20)\d{2}\s*-\s*(?:19|20)\d{2}\s*', row["Policy"].lower())) > 0:
                    law_strategy_list[num] = "Preparatory Instruments"
                elif len(re.findall(r'(?:19|20)\d{2}/\d{2}\s*-\s*(?:19|20)\d{2}/\d{2}\s*', row["Policy"].lower())) > 0:
                    law_strategy_list[num] = "Preparatory Instruments"
                # elif "strategy" in row["Title"].lower():
                #     law_strategy_list[num] = "Preparatory Instruments"
                # elif ("aim" in row["Description"].lower()) or ("seek" in row["Description"].lower()) or (
                #         "vision" in row["Description"].lower()):
                #     law_strategy_list[num] = "Preparatory Instruments"

        # distinct: Steering Instruments, Decisional Guidelines, Codes and Frameworks
        # judgement: connection to existing Community law
        for strdcs in ["Steering Instruments", "Decisional Guidelines, Codes and Frameworks"]:
            if break_judge:
                break
            softlaw_content_keywords = soft_hard_law_content_dict[strdcs].lower().split(';')
            for keyword in softlaw_content_keywords:
                if break_judge:
                    break
                if ' ' in keyword:
                    if len(re.findall(keyword, policy)) > 0:
                        if any([i in row["Type"] for i in
                                ['Market design rules', 'Energy market regulation',
                                 'Energy trading regulations', 'Regulation']]):
                            law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                            break_judge = True
                            break
                        for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                        'Decree/Order/Ordinance', 'Regulation/Directive/Decision', 'Kyoto protocol']:
                            if break_judge:
                                break
                            if hardlaw == 'Kyoto protocol':
                                law_keywords = ['kyoto protocol']
                            else:
                                law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                            for kw in law_keywords:
                                if ' ' in kw:
                                    if len(re.findall(kw, policy_content)) > 0:
                                        law_strategy_list[
                                            num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break
                                else:
                                    if kw in policy_content.split(" "):
                                        law_strategy_list[
                                            num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break

                        if not break_judge:
                            law_strategy_list[num] = "Steering Instruments"
                            break_judge = True
                            break
                else:
                    if keyword in policy.split(" "):
                        if any([i in row["Type"] for i in
                                ['Market design rules', 'Energy market regulation',
                                 'Energy trading regulations', 'Regulation']]):
                            law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                            break_judge = True
                            break
                        for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                        'Decree/Order/Ordinance', 'Regulation/Directive/Decision', 'Kyoto protocol']:
                            if break_judge:
                                break
                            if hardlaw == 'Kyoto protocol':
                                law_keywords = ['kyoto protocol']
                            else:
                                law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                            for kw in law_keywords:
                                if ' ' in kw:
                                    if len(re.findall(kw, policy_content)) > 0:
                                        law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break
                                else:
                                    if kw in policy_content.split(" "):
                                        law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break

                        if not break_judge:
                            law_strategy_list[num] = "Steering Instruments"
                            break_judge = True
                            break

        # Type in IEA is not very accurate
        if not break_judge:
            if any([i in row["Type"] for i in
                    ['Long-term low emissions development strategy (LT-LEDS)', 'Nationally Determined Contribution',
                     'Major infrastructure plan', 'Technology roadmaps', 'Urban planning', 'Strategic plans',
                     'Public voluntary programmes']]):
                law_strategy_list[num] = "Preparatory Instruments"
            elif any([i in row["Type"] for i in
                      ['Negotiated agreements (public-private sector)', 'Unilateral commitments (private sector)',
                       'Government provided advice', 'International collaboration']]):
                law_strategy_list[num] = "Steering Instruments"
            elif any([i in row["Type"] for i in
                      ['Sustainable finance frameworks', 'Framework legislation']]):
                law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
            elif any([i in row["Type"] for i in
                      ['Building code (Prescriptive)', 'Building codes (performance-based)',
                       'Sectoral standards', 'Building codes and standards', 'Codes and standards',
                       'Product-based MEPS', 'Minimum energy performance standards',
                       'Prescriptive requirements and standards', 'Safety standards', 'Emission standards',
                       'Fuel quality standards']]):
                if any([i in row["Type"] for i in
                        ['Market design rules', 'Energy market regulation',
                         'Energy trading regulations', 'Regulation']]):
                    law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                else:
                    for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                    'Decree/Order/Ordinance', 'Regulation/Directive/Decision']:
                        if break_judge:
                            break
                        law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                        for keyword in law_keywords:
                            if ' ' in keyword:
                                if len(re.findall(keyword, policy_content)) > 0:
                                    law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                    break_judge = True
                                    break
                            else:
                                if keyword in policy_content.split(" "):
                                    law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                    break_judge = True
                                    break

                    if not break_judge:
                        law_strategy_list[num] = "Steering Instruments"
            elif any([i in row["Type"] for i in
                      ['Information campaigns', 'Public information', 'Consumer information']]):
                law_strategy_list[num] = "Informative Instruments"

            # elif row["Type"] in \
            #         ['Procedural requirements', 'Rights', 'Pollution liability', 'finance and taxation',
            #          'Obligations on average types of sales / output', 'Compliance requirements',
            #          'Performance-based payments', 'Tax credits and exemptions',
            #          'Measurement, calibration, equipment requirements', 'Payments and transfers', 'Feebate',
            #          'Enforcement', 'Excise taxes', 'Luxury tax', 'Rights, permits and licenses', 'Road usage charges',
            #          'Equipment sales obligation', 'Vehicle registration tax',
            #          'Externality taxation', 'Prohibition', 'Mandatory energy management system',
            #          'Use and activity charges', 'Other regulatory instruments',
            #          'Associated pollutant limitations (SOx, VOCs, etc.)', 'Leak detection and repair requirements',
            #          'Metering and connection requirements', 'Pollution rights', 'Payments, finance and taxation',
            #          'GHG taxation', 'Prevenative maintenance requirements', 'Recordkeeping requirements',
            #          'Renewable / Non-fossil energy obligations', 'Energy efficiency / Fuel economy obligations',
            #          'Carbon tax', 'Mandatory reporting', 'Notice requirements', 'Congestion charge', 'Parking charges',
            #          'Taxes, fees and charges', 'permits and licenses', 'Company car tax',
            #          'Public disclosure requirements', 'Mandatory technology use', 'Technology bans / phase outs',
            #          'Resource rights', 'Import tax', 'Endorsement labels', 'Use / activity restrictions',
            #          'Permitting processes', 'Other polluant liabilities', 'Product taxation']:
            #     law_strategy_list[num] = "Hard Law"

            # elif row["Type"] in \
            #         ['Negotiated agreements (public-private sector)', 'Grants', 'Finance', 'Inducement prizes',
            #          'Unilateral commitments (private sector)', 'Public procurement', 'Feed-in tariffs/premiums',
            #          'Price controls (incl. social tariffs)', 'Time-of-use tariffs', 'Accelerated depreciation',
            #          'Funds to sub-national governments', 'Awards', 'Operational funding for institutions',
            #          'Government provided advice', 'International collaboration', 'Loans (incl. concessional loans)',
            #          'Insurance', 'Loans / debt finance', 'Investment tax incentives', 'Co-funding via investment fund',
            #          'Loan guarantee', 'Education and training']:
            #     law_strategy_list[num] = "Steering Instruments"

            else:
                # Soft Law use Policy Content
                for softlaw in ["Steering Instruments", "Decisional Guidelines, Codes and Frameworks",
                                "Decisional Notices and Communications", "Preparatory Instruments",
                                "Informative Instruments", "Interpretative Communications and Notices"]:
                    if break_judge:
                        break

                    if softlaw in ["Steering Instruments", "Decisional Guidelines, Codes and Frameworks"]:
                        if break_judge:
                            break
                        softlaw_content_keywords = soft_hard_law_content_dict[softlaw].lower().split(';') + \
                                                   soft_hard_law_title_dict[softlaw].lower().split(';')
                        for keyword in softlaw_content_keywords:
                            if ' ' in keyword:
                                if len(re.findall(keyword, policy_content)) > 0:
                                    if any([i in row["Type"] for i in
                                            ['Market design rules', 'Energy market regulation',
                                             'Energy trading regulations', 'Regulation']]):
                                        law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break
                                    for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                                    'Decree/Order/Ordinance', 'Regulation/Directive/Decision',
                                                    'Kyoto protocol']:
                                        if break_judge:
                                            break
                                        if hardlaw == 'Kyoto protocol':
                                            law_keywords = ['kyoto protocol']
                                        else:
                                            law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                                        for kw in law_keywords:
                                            if ' ' in kw:
                                                if len(re.findall(kw, policy_content)) > 0:
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break
                                            else:
                                                if kw in policy_content.split(" "):
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break

                                    if not break_judge:
                                        law_strategy_list[num] = "Steering Instruments"
                                        break_judge = True
                                        break
                            else:
                                if keyword in policy_content.split(" "):
                                    if any([i in row["Type"] for i in
                                            ['Market design rules', 'Energy market regulation',
                                             'Energy trading regulations', 'Regulation']]):
                                        law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break
                                    for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                                    'Decree/Order/Ordinance', 'Regulation/Directive/Decision',
                                                    'Kyoto protocol']:
                                        if break_judge:
                                            break
                                        if hardlaw == 'Kyoto protocol':
                                            law_keywords = ['kyoto protocol']
                                        else:
                                            law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                                        for kw in law_keywords:
                                            if ' ' in kw:
                                                if len(re.findall(kw, policy_content)) > 0:
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break
                                            else:
                                                if kw in policy_content.split(" "):
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break

                                    if not break_judge:
                                        law_strategy_list[num] = "Steering Instruments"
                                        break_judge = True
                                        break
                    else:
                        softlaw_content_keywords = soft_hard_law_content_dict[softlaw].lower().split(';')
                        for keyword in softlaw_content_keywords:
                            if ' ' in keyword:
                                if len(re.findall(keyword, policy_content)) > 0:
                                    law_strategy_list[num] = softlaw
                                    break_judge = True
                                    break
                            else:
                                if keyword in policy_content.split(" "):
                                    law_strategy_list[num] = softlaw
                                    break_judge = True
                                    break

    iea_df["law or strategy"] = law_strategy_list
    iea_df["Policy Type"] = policy_type_list
    save(iea_df, "iea")


def cp_law_process(soft_hard_law_title_dict, soft_hard_law_content_dict):
    cp_df = get_cp_data()
    cp_df["Policy name"].fillna("", inplace=True)
    cp_df["Policy description"].fillna("", inplace=True)
    cp_df["Type of policy instrument"].fillna("", inplace=True)
    law_strategy_list = ["Other Strategy Plan or Target"] * len(cp_df["Policy Title"].to_list())
    policy_type_list = ["executive"] * len(cp_df["Policy Title"].to_list())

    for num, row in cp_df.iterrows():
        # Title
        policy = row["Policy name"].lower(). \
            replace("(", ' ').replace(")", ' ').replace(",", ' ').replace("\"", ' ').replace("'", ' '). \
            replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')
        # Content
        policy_content = row["Policy description"].lower(). \
            replace("(", ' ').replace(")", ' ').replace(",", ' ').replace("\"", ' ').replace("'", ' '). \
            replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')

        break_judge = False
        for hardlaw in ['Constitution', 'International Law', 'Law/Act', 'Decree/Order/Ordinance',
                        'Regulation/Directive/Decision']:
            if break_judge:
                break
            law_keywords = soft_hard_law_title_dict[hardlaw].lower().split(';')
            for keyword in law_keywords:
                if ' ' in keyword:
                    if len(re.findall(keyword, policy)) > 0:
                        law_strategy_list[num] = hardlaw
                        if hardlaw in ['Constitution', 'International Law', 'Law/Act']:
                            policy_type_list[num] = "legislative"
                        break_judge = True
                        break
                else:
                    if keyword in policy.split(" "):
                        law_strategy_list[num] = hardlaw
                        if hardlaw in ['Constitution', 'International Law', 'Law/Act']:
                            policy_type_list[num] = "legislative"
                        break_judge = True
                        break

        # if any([i in row["Type of policy instrument"] for i in
        #         ['Formal & legally binding GHG reduction target',
        #          'Formal & legally binding energy efficiency target',
        #          'Formal & legally binding climate strategy',
        #          'Formal & legally binding renewable energy target']]):
        #     law_strategy_list[num] = "Hard Law"
        #     break_judge = True

        if not break_judge:
            for softlaw in ["Decisional Notices and Communications", "Interpretative Communications and Notices"]:
                if break_judge:
                    break
                softlaw_keywords = soft_hard_law_title_dict[softlaw].lower().split(';')
                for keyword in softlaw_keywords:
                    if ' ' in keyword:
                        if len(re.findall(keyword, policy)) > 0:
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break
                    else:
                        if keyword in policy.split(" "):
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break

        # hard law "this"/"the" in policy content
        for hl_this in ['Law/Act', 'Decree/Order/Ordinance', 'Regulation/Directive/Decision']:
            if break_judge:
                break
            if hl_this == 'Law/Act':
                for i in 'Law/Act/Legislation'.lower().split("/"):
                    if (("the" + " " + i + " ") in policy_content) or (("this" + " " + i + " ") in policy_content):
                        law_strategy_list[num] = hl_this
                        policy_type_list[num] = "legislative"
                        break_judge = True
                        break
            else:
                for i in hl_this.lower().split("/"):
                    if (("the" + " " + i + " ") in policy_content) or (("this" + " " + i + " ") in policy_content):
                        law_strategy_list[num] = hl_this
                        break_judge = True
                        break

        if not break_judge:
            for softlaw in ["Steering Instruments", "Preparatory Instruments",
                            "Decisional Guidelines, Codes and Frameworks", "Informative Instruments"]:
                if break_judge:
                    break
                softlaw_keywords = soft_hard_law_title_dict[softlaw].lower().split(';')
                for keyword in softlaw_keywords:
                    if ' ' in keyword:
                        if len(re.findall(keyword, policy)) > 0:
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break
                    else:
                        if keyword in policy.split(" "):
                            law_strategy_list[num] = softlaw
                            break_judge = True
                            break
            if not break_judge:
                if len(re.findall(r'(?:19|20)\d{2}\s*-\s*(?:19|20)\d{2}\s*', row["Policy name"].lower())) > 0:
                    law_strategy_list[num] = "Preparatory Instruments"
                elif len(re.findall(r'(?:19|20)\d{2}/\d{2}\s*-\s*(?:19|20)\d{2}/\d{2}\s*',
                                    row["Policy name"].lower())) > 0:
                    law_strategy_list[num] = "Preparatory Instruments"
                # elif "strategy" in row["Title"].lower():
                #     law_strategy_list[num] = "Preparatory Instruments"
                # elif ("aim" in row["Description"].lower()) or ("seek" in row["Description"].lower()) or (
                #         "vision" in row["Description"].lower()):
                #     law_strategy_list[num] = "Preparatory Instruments"

        # distinct: Steering Instruments, Decisional Guidelines, Codes and Frameworks
        # judgement: connection to existing Community law
        for strdcs in ["Steering Instruments", "Decisional Guidelines, Codes and Frameworks"]:
            if break_judge:
                break
            softlaw_content_keywords = soft_hard_law_content_dict[strdcs].lower().split(';')
            for keyword in softlaw_content_keywords:
                if break_judge:
                    break
                if ' ' in keyword:
                    if len(re.findall(keyword, policy)) > 0:
                        for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                        'Decree/Order/Ordinance', 'Regulation/Directive/Decision', 'Kyoto protocol']:
                            if break_judge:
                                break
                            if hardlaw == 'Kyoto protocol':
                                law_keywords = ['kyoto protocol']
                            else:
                                law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                            for keyword in law_keywords:
                                if ' ' in keyword:
                                    if len(re.findall(keyword, policy_content)) > 0:
                                        law_strategy_list[
                                            num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break
                                else:
                                    if keyword in policy_content.split(" "):
                                        law_strategy_list[
                                            num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break

                        if not break_judge:
                            law_strategy_list[num] = "Steering Instruments"
                            break_judge = True
                            break
                else:
                    if keyword in policy_content.split(" "):
                        for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                        'Decree/Order/Ordinance', 'Regulation/Directive/Decision', 'Kyoto protocol']:
                            if break_judge:
                                break
                            if hardlaw == 'Kyoto protocol':
                                law_keywords = ['kyoto protocol']
                            else:
                                law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                            for keyword in law_keywords:
                                if ' ' in keyword:
                                    if len(re.findall(keyword, policy_content)) > 0:
                                        law_strategy_list[
                                            num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break
                                else:
                                    if keyword in policy_content.split(" "):
                                        law_strategy_list[
                                            num] = "Decisional Guidelines, Codes and Frameworks"
                                        break_judge = True
                                        break

                        if not break_judge:
                            law_strategy_list[num] = "Steering Instruments"
                            break_judge = True
                            break

        if not break_judge:
            if any([i in row["Type of policy instrument"] for i in
                    ['Codes and standards', 'Sectoral standards', 'Product standards', 'Building codes and standards',
                     'Industrial air pollution standards', 'Vehicle fuel-economy and emissions standards',
                     'Vehicle air pollution standards', 'Performance label', 'Comparison label']]):
                for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                'Decree/Order/Ordinance', 'Regulation/Directive/Decision']:
                    if break_judge:
                        break
                    law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                    for keyword in law_keywords:
                        if ' ' in keyword:
                            if len(re.findall(keyword, policy_content)) > 0:
                                law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                break_judge = True
                                break
                        else:
                            if keyword in policy_content.split(" "):
                                law_strategy_list[num] = "Decisional Guidelines, Codes and Frameworks"
                                break_judge = True
                                break

                if not break_judge:
                    law_strategy_list[num] = "Steering Instruments"

            # elif any([i in row["Type of policy instrument"] for i in
            #           ['Procurement rules', 'Energy and other taxes', 'Regulatory Instruments', 'User charges',
            #            'Other mandatory requirements', 'Endorsement label', 'CO2 taxes']]):
            #     law_strategy_list[num] = "Hard Law"

            elif any([i in row["Type of policy instrument"] for i in
                      ['Energy efficiency target', 'Strategic planning', 'Public voluntary schemes',
                       'Obligation schemes', 'Political & non-binding GHG reduction target', 'Research programme',
                       'Political & non-binding renewable energy target',
                       'Political & non-binding energy efficiency target', 'Tendering schemes']]):
                law_strategy_list[num] = "Preparatory Instruments"
            # elif any([i in row["Type of policy instrument"] for i in
            #           ['Grants and subsidies', 'Economic instruments', 'RD&D funding', 'Tax relief',
            #            'Retirement premium', 'Feed-in tariffs or premiums', 'Advice or aid in implementation',
            #            'Fiscal or financial incentives', 'GHG emissions allowances', 'Removal of fossil fuel subsidies',
            #            'Research & Development and Deployment (RD&D)', 'Loans', 'Funds to sub-national governments',
            #            'Policy support', 'Direct investment', 'Negotiated agreements (public-private sector)',
            #            'Demonstration project', 'Unilateral commitments (private sector)', 'Voluntary approaches']]):
            #     law_strategy_list[num] = "Steering Instruments"
            elif any([i in row["Type of policy instrument"] for i in
                      ['Negotiated agreements (public-private sector)', 'Demonstration project',
                       'Unilateral commitments (private sector)', 'Voluntary approaches']]):
                law_strategy_list[num] = "Steering Instruments"
            elif any([i in row["Type of policy instrument"] for i in
                      ['Information provision', 'Information and education']]):
                law_strategy_list[num] = "Informative Instruments"
            else:
                # Soft Law use Policy Content
                for softlaw in ["Steering Instruments", "Decisional Guidelines, Codes and Frameworks",
                                "Decisional Notices and Communications", "Preparatory Instruments",
                                "Informative Instruments", "Interpretative Communications and Notices"]:
                    if break_judge:
                        break

                    if softlaw in ["Steering Instruments", "Decisional Guidelines, Codes and Frameworks"]:
                        softlaw_content_keywords = soft_hard_law_content_dict[softlaw].lower().split(';') + \
                                                   soft_hard_law_title_dict[softlaw].lower().split(';')
                        for keyword in softlaw_content_keywords:
                            if ' ' in keyword:
                                if len(re.findall(keyword, policy_content)) > 0:
                                    for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                                    'Decree/Order/Ordinance', 'Regulation/Directive/Decision',
                                                    'Kyoto protocol']:
                                        if break_judge:
                                            break
                                        if hardlaw == 'Kyoto protocol':
                                            law_keywords = ['kyoto protocol']
                                        else:
                                            law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                                        for kw in law_keywords:
                                            if ' ' in kw:
                                                if len(re.findall(kw, policy_content)) > 0:
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break
                                            else:
                                                if kw in policy_content.split(" "):
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break

                                    if not break_judge:
                                        law_strategy_list[num] = "Steering Instruments"
                                        break_judge = True
                                        break
                            else:
                                if keyword in policy_content.split(" "):
                                    for hardlaw in ['Constitution', 'International Law', 'Law/Act',
                                                    'Decree/Order/Ordinance', 'Regulation/Directive/Decision',
                                                    'Kyoto protocol']:
                                        if break_judge:
                                            break
                                        if hardlaw == 'Kyoto protocol':
                                            law_keywords = ['kyoto protocol']
                                        else:
                                            law_keywords = soft_hard_law_content_dict[hardlaw].lower().split(';')
                                        for kw in law_keywords:
                                            if ' ' in kw:
                                                if len(re.findall(kw, policy_content)) > 0:
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break
                                            else:
                                                if kw in policy_content.split(" "):
                                                    law_strategy_list[
                                                        num] = "Decisional Guidelines, Codes and Frameworks"
                                                    break_judge = True
                                                    break

                                    if not break_judge:
                                        law_strategy_list[num] = "Steering Instruments"
                                        break_judge = True
                                        break
                    else:
                        softlaw_content_keywords = soft_hard_law_content_dict[softlaw].lower().split(';')
                        for keyword in softlaw_content_keywords:
                            if ' ' in keyword:
                                if len(re.findall(keyword, policy_content)) > 0:
                                    law_strategy_list[num] = softlaw
                                    break_judge = True
                                    break
                            else:
                                if keyword in policy_content.split(" "):
                                    law_strategy_list[num] = softlaw
                                    break_judge = True
                                    break

    cp_df["law or strategy"] = law_strategy_list
    cp_df["Policy Type"] = policy_type_list
    save(cp_df, "cp")


if __name__ == '__main__':
    soft_hard_law_title_dict, soft_hard_law_content_dict = get_dict()

    lse_law_process(soft_hard_law_title_dict, soft_hard_law_content_dict)
    iea_law_process(soft_hard_law_title_dict, soft_hard_law_content_dict)
    cp_law_process(soft_hard_law_title_dict, soft_hard_law_content_dict)
