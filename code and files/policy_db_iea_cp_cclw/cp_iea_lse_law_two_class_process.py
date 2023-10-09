import re

import pandas as pd
import numpy as np


def get_cp_data():
    cp_df = pd.read_excel("cp_sector_region_instrument_annex_objective_result.xlsx")
    return cp_df


def get_iea_data():
    iea_df = pd.read_excel("iea_sector_region_instrument_annex_objective_result.xlsx")
    return iea_df


def get_lse_data():
    lse_df = pd.read_excel("lse_sector_region_instrument_annex_objective_result.xlsx")
    return lse_df


# 保存处理文件
def save(df, db):
    df.to_excel("{}_sector_region_instrument_annex_objective_law_result.xlsx".format(db), encoding='utf-8', index=False)


if __name__ == '__main__':
    # law_word_group = "Tax Credit;Tax Exemption;Excise Duty;Excise Tax;NOM-001-ENER;NOM-002-SEDE".lower()
    # law = "law;Laws;Act;Acts;Code;Regulations;Regulation;Resolution;Decree;Decrees;Sub-Decree;Decree-Law;Order;Orders;Rules;Rule;Legislation;Prohibition;Ban;amend;amendment;amending;Revision;Ordinance;Ordinances;Bill;endorsements;endorsement;Directive;Directives;MEPS;SANS;Standards;Standard;Act-Programme;Obligation;Taxation;Tax;Bonus;Awards;Award;Principles;Principle;Tariff;Tariffs;Subsidy;Subsidies;Reimbursement;Mandatory;Taxing;mandate;Levy;Cess;Duty;CO2-tax".lower()
    # strategy_plan_target_word_group = "White Paper;White Papers;Road Map;Nationally Determined Contribution;Intended Nationally Determined Contribution;Carbon Neutral".lower()
    # strategy_plan_target = "Plan;Plans;Programme;Programmes;Program;Programs;Initiative;Vision;municipalities;Targets;Target;Commitment;Strategy;Strategies;Strategic;Agreement;Agreements;Agenda;Accord;Decision;Decisions;Policy;Policies;Roadmap;Route;note;Budget;Scheme;Deal;Report;Reporting;Instruction;Pact;Notification;Notice;Concept;Guide;Guideline;Guidelines;Blueprint;INDC;NDC;Proclamation;Framework;Incentive;Incentives;Voluntary;Audit;Audits;Projects;Project;Planned;Fund;Funding;Invest;Promotion;Aid;Campaign;planned;Campaigns;Requirements;Support".lower()

    with open("law_keywords.txt") as f:
        all_keywords = f.read().lower().split('\n')
        print(all_keywords)
        law_word_group = all_keywords[0]
        law = all_keywords[1]
        strategy_plan_target_word_group = all_keywords[2]
        strategy_plan_target = all_keywords[3]

    # iea
    iea_df = get_iea_data()
    iea_df["Type"].fillna("", inplace=True)
    law_strategy_list = [''] * len(iea_df["Policy"].to_list())
    for num, row in iea_df.iterrows():
        if len([i for i in row["Type"].split(";") if
                i.strip() in ["Climate change strategies", "Long-term low emissions development strategy (LT-LEDS)",
                              "National climate change strategy", "Strategic plans"]]) > 0:
            law_strategy_list[num] = "strategy plan and target"
        elif len([i for i in row["Type"].split(";") if i.strip() == "Framework legislation"]) > 0:
            law_strategy_list[num] = "law"
        else:
            policy = row["Policy"].lower().replace("(", ' ').replace(")", ' ').replace(",", ' ').replace(".",
                                                                                                         ' ').replace(
                ";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')
            if any(i for i in law_word_group.split(";") if len(re.findall(i, policy)) > 0):
                law_strategy_list[num] = "law"
            elif any(i for i in strategy_plan_target_word_group.split(";") if len(re.findall(i, policy)) > 0):
                law_strategy_list[num] = "strategy plan and target"
            elif any(i for i in law.split(";") if i in policy.split(" ")):
                law_strategy_list[num] = "law"
            elif any(i for i in strategy_plan_target.split(";") if i in policy.split(" ")):
                law_strategy_list[num] = "strategy plan and target"
            else:
                law_strategy_list[num] = "unknown"

    iea_df["law or strategy"] = law_strategy_list
    save(iea_df, "iea")

    # cp
    cp_df = get_cp_data()
    cp_df["Policy Title"].fillna("", inplace=True)
    cp_df["Type of policy instrument"].fillna("", inplace=True)
    law_strategy_list = [''] * len(cp_df["Policy Title"].to_list())
    for num, row in cp_df.iterrows():
        if any([i for i in ["Political & non-binding climate strategy", "Strategic planning"] if
                i in row["Type of policy instrument"]]):
            law_strategy_list[num] = "strategy plan and target"
        elif any([i for i in ["Formal & legally binding climate strategy", "Coordinating body for climate strategy",
                              "Formal & legally binding energy efficiency target"] if
                  i in row["Type of policy instrument"]]):
            law_strategy_list[num] = "law"
        else:
            policy = row["Policy Title"].lower().replace("(", ' ').replace(")", ' '). \
                replace(",", ' ').replace(".", ' ').replace(";", ' ').replace("-", ' ').replace(":", ' ').replace("/",
                                                                                                                  ' ')
            if any(i for i in law_word_group.split(";") if len(re.findall(i, policy)) > 0):
                law_strategy_list[num] = "law"
            elif any(i for i in strategy_plan_target_word_group.split(";") if len(re.findall(i, policy)) > 0):
                law_strategy_list[num] = "strategy plan and target"
            elif any(i for i in law.split(";") if i in policy.split(" ")):
                law_strategy_list[num] = "law"
            elif any(i for i in strategy_plan_target.split(";") if i in policy.split(" ")):
                law_strategy_list[num] = "strategy plan and target"
            else:
                law_strategy_list[num] = "unknown"

    cp_df["law or strategy"] = law_strategy_list
    save(cp_df, "cp")

    # lse
    lse_df = get_lse_data()
    lse_df["Title"].fillna("", inplace=True)
    law_strategy_list = ["strategy plan and target"] * len(lse_df["Title"].to_list())
    for num, row in lse_df.iterrows():
        policy = row["Title"].lower().replace("(", ' ').replace(")", ' ').replace(",", ' ').replace(".", ' ').replace(
            ";", ' ').replace("-", ' ').replace(":", ' ').replace("/", ' ')
        # if row["Title"] == "Royal Decree no. 8/2011 (Oil and Gas Law)":
        #     print("Royal Decree no. 8/2011 (Oil and Gas Law)")
        #     print(any(i for i in strategy_plan_target_word_group.split(";") if len(re.findall(i, policy)) > 0))
        #     print('*' * 30)
        #     print(any(i for i in law.split(";") if i in policy.split(" ")))
        if any(i for i in law_word_group.split(";") if len(re.findall(i, policy)) > 0):
            law_strategy_list[num] = "law"
        elif any(i for i in strategy_plan_target_word_group.split(";") if len(re.findall(i, policy)) > 0):
            law_strategy_list[num] = "strategy plan and target"
        elif any(i for i in law.split(";") if i in policy.split(" ")):
            law_strategy_list[num] = "law"
        elif any(i for i in strategy_plan_target.split(";") if i in policy.split(" ")):
            law_strategy_list[num] = "strategy plan and target"

    lse_df["law or strategy"] = law_strategy_list
    save(lse_df, "lse")
