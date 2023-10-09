import json
import os
import sys

print("================== {} ==================".format(os.path.basename(sys.argv[0])))

# ================== DETAIL REFERENCE ==================
# cp_iea_lse_law_dict_create.ipynb


# ================== Categories ==================
# Three-tier Categories:
# ├── Hard Law
#  ├── Constitution (legislative)
#  ├── Statutes / Legislation
#    ├── International Law (-)
#    ├── Law/Act (almost legislative)
#    ├── Decree/Order/Ordinance (almost executive)
#    └── Common Law / Case Law (executive)
#  └── Regulations / Rules (almost executive)
# ├── Soft Law & Quasi-legislative
#  ├── Preparatory and Informative Instruments (pre-law function)
#    ├── Preparatory Instruments (pre-law function)
#    └── Informative Instruments (partially pre-law function)
#  ├── Interpretative and Decisional Instruments (post-law function)
#    ├── Interpretative Communications and Notices (post-law function)
#    ├── Decisional Notices and Communications (post-law function)
#    └── Decisional Guidelines, Codes and Frameworks (post-law function)
#  └── Steering Instruments (partially para-law function)
# └── Other Strategy Plan or Target


law_soft_law_strategy = dict()

# ================== Hard Law ==================
# ------------------ Constitution ------------------
law_soft_law_strategy['Constitution'] = 'Constitution;Constitutional'

# ------------------ Statutes / Legislation ------------------
# ****************** International Law ******************
law_soft_law_strategy['International Law'] = 'Treaties;Treaty'

# ****************** Law/Act ******************
law_soft_law_strategy['Law/Act'] = \
    'Law;Laws;Decree-Law;Bylaw;Act;Acts;Legislation;Legislations;Legislative;Statutes;Statute;Statutory;Ley;LOI;Wet'
# Ley: spanish
# LOI: FRA
# Wet: NLD (Wet wind op Zee)

# ****************** Decree/Order/Ordinance ******************
law_soft_law_strategy['Decree/Order/Ordinance'] = \
    'Ordinance;Ordinances;Order;Orders;Ordice;Decree;Decrees;Decreto;Sub-Decree;Decree-Law;Royal Decree;Royal Decrees;' \
    'Executive Decree;Executive Decrees;Presidential Decree;Presidential Decrees;Presidential Instruction;Sub-Decree;' \
    'Real Decreto;Portaria;Ökostromverordnung;DEC;Presidential Instruction'
# Portarias is Portuguese, corresponding to the Ordinance in English
# Real Decreto is Portuguese, corresponding to the Royal Decree in English
# Ökostromverordnung: Green Electricity Ordinance (AUT)
# Decreto: ITA
# Presidential Instruction: Indonesia

# ------------------ Regulations / Rules ------------------
law_soft_law_strategy['Regulation/Directive/Decision'] = \
    'Enforcement Rules;Rules;Rule;Regulations;Regulation;Regulating;Directive;Directives;Decision;Decisions;CFR;' \
    'Interim Measures;Interim Measure;Interim rules;Interim Procedures;Regulación;Règlement;Despacho Normativo'
# CFR: Code of Federal Regulations in USA
# Interim Measures;Interim procedures: legally binding in China
# Regulación: spanish
# Règlement: FRA
# Despacho Normativo: PRT


# ================== Soft Law & Quasi-legislative ==================
# ------------------ Preparatory and Informative Instruments ------------------
# ****************** Preparatory Instruments ******************
law_soft_law_strategy['Preparatory Instruments'] = \
    'Green Papers;Green Paper;White Paper;White Papers;Action Programmes;Action Programme;General Programmes;' \
    'General Programme;Action Plans;Action Plan;Action Program;Action Programs;Incentive Measures;Appropriate Measures;' \
    'Road Map;Act Programme;Nationally determined contributions;Common Rules;Appropriate Provisions;' \
    'NDCs;NDC;INDC;Programs;Program;Programme;Programmes;Programming;Milestone;Milestones;Action;Actions;Measures;' \
    'Arrangements;Arrangement;Activities;Activity;' \
    'Prepare;Preparation;Plan;Plans;Planned;Planning;Route;Roadmap;Roadmaps;Blueprint;Agenda;FYP;' \
    'Scheme;Schemes;Schedules;Schedule;Objectives;Objective;Vision;Pilot;Campaign;Campaigns;Bailout;' \
    'Goal;Goals;Budget;Targets;Target;Aimed;Aim;Aims;Report;Reporting;Package;Strategy;Strategies;Strategic;' \
    'Achieving;Achieve;Trials;Tomorrow;Horizon;' \
    'Bill;Motion;Mobility;Intention'
# FYP: Five Year Plan


# ****************** Informative Instruments ******************
law_soft_law_strategy['Informative Instruments'] \
    = 'Information;Informations;Info;Website;Survey;Surveys;Progress Report;Report;Reports;Reporting;' \
      'Evaluation;Assess;Assessment;Consultation;Consult;Consulting;List;Lists;Catalogue;Publicity;Phase;Phase-out;' \
      'Establish;Established;Found;Set up;Announced;Statement;Reference'

# ------------------ Interpretative and Decisional Instruments ------------------
# ****************** Interpretative Communications and Notices ******************
law_soft_law_strategy['Interpretative Communications and Notices'] \
    = 'Communication;Communications;Interpretation;Interpretative;Interpret;' \
      'Concept;Explain;Explanation;Explication;Explicate;Exposition;Supplement;Supplements'

# ****************** Decisional Notices and Communications ******************
law_soft_law_strategy['Decisional Notices and Communications'] \
    = 'Notification;Notice;Notices;Circulars;Circular;Gazette;Aviso;Communiqué'
# Aviso: PRT
# Communiqué: FRA

# ****************** Decisional Guidelines, Codes and Frameworks ******************
#  This very connection to existing Community law
# Not limited to Aid
law_soft_law_strategy['Decisional Guidelines, Codes and Frameworks'] \
    = 'Standards;Standard;Standardization;Standardisation;Norm;Norms;Compliance;Aid;Aids;' \
      'Level;Levels;Label;Labels;Labelling;Rating;Ecolabel;Ecolabels;Eco-label;Taxonomy;Directory;Booklet;Criteria;' \
      'Tax deductions;Tax deduction;Principles;Principle;Solutions;Solution;' \
      'NOM;BDS;CP;NCM;NHN;MEPS;MEP;GB;GB/T;LI;LBN;KS;CNS;JS;RS;SANS;SNI;SASO;TIS;VC;NTC;EN;PROCEL;R-2000;AS/NZS;QS;' \
      'IECC;CBES;HEC;RBES;BEES;NMECC;MUEC;MUBEC;STB;CBECC;ECBC;AS/NZS;GSO;NSO;GOST;NTON;TCVN;SI;S&L;PNS;50001;UNIT;ISO;' \
      'Applicable;Performance Certificate;Indexed'

# ------------------ Steering Instruments ------------------
law_soft_law_strategy['Steering Instruments'] \
    = 'Assistance;Assisted;REN21;Codes of Conduct;Code of Practice;Conduct'
# ;Stimulus;Stimulation;Rebates;Rebate;Refund;Free;Premium;Premiums;' \
# 'Tariff;Tariffs;Feed-in-tariffs;Feed-in-tariff;Subsidy;Subsidies;Exemption;Exemptions;Support;Supports;' \
# 'Bonus;Awards;Award;Benefit;Benefits;Fund;Funds;Funded;Funding;Investing;Invest;Investment;Investments;' \
# 'Promotion;Promote;Promoting;Incentive;Incentives;Free;Grants;Grant;Granted;' \
# 'Loans;Loan;Loan Insurance;low interest loans;Derogation;' \
# 'Tax Credit;Tax Exemption;Tax-exemption;Kyoto Protocol;Toll;Tolls;Tax;Taxes;Taxation;VAT;Eco-Tax;' \
# 'Pricing;GIS;Renovation;Co-financed;Co-financing;Finance;Financing;Financial;' \
# 'Preferential;MorSEEF;Indications;Indication

# principles’, ‘criteria’, ‘standards’ and
# ‘recommendations’
# As the following examples show, steering instruments may lay down
# new rules, independently of an existing legal framework, or may be
# adopted in the context of such a framework, prior to, simultaneous with or subsequent to legislation.

# ================== Other Strategy Plan or Target ==================
# law_soft_law_strategy['Other Strategy Plan or Target'] \
#     = 'Strategy;Strategies;Strategic;Accord;Policy;Policies;Pact;Voluntary;Audit;Audits;Projects;Project'

with open('law_soft_law_strategy_content_dict.json', 'w') as f:
    json.dump(law_soft_law_strategy, f)
