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
    'Arrangements;Arrangement;' \
    'Prepare;Preparation;Plan;Plans;Planned;Planning;Route;Roadmap;Roadmaps;Blueprint;Agenda;FYP;' \
    'Scheme;Schemes;Schedules;Schedule;Objectives;Objective;Vision;Pilot;Campaign;Campaigns;Bailout;' \
    'Goal;Goals;Budget;Targets;Target;Aimed;Aim;Aims;Report;Reporting;Package;Strategy;Strategies;Strategic;' \
    'Achieving;Achieve;Trials;Tomorrow;Horizon;' \
    'Bill;Draft;Motion;Mobility;Intention'
# FYP: Five Year Plan
# ;Activities;Activity


# ****************** Informative Instruments ******************
law_soft_law_strategy['Informative Instruments'] \
    = 'Information;Informations;Info;.gov;Website;Survey;Surveys;Progress Report;Report;Reports;Reporting;' \
      'Evaluation;Assess;Assessment;Consultation;Consult;Consulting;List;Lists;Catalogue;Publicity;Phase;Phase-out;' \
      'Establish;Established;Found;Set up;Announced;Statement;Reference'

# 任命、成立实验室、成立机构等等、到期通知、招标通知和组织机构公告
# The communications on the appointment of certain persons, the notices on the common position of
# the Council in the co-decision procedure, the notices of the date of entry into force of international agreements
# the notices of the expiry of certain anti-dumping measures are examples in this respect. As such, they
# resemble the purely informative communications.
# the notices of invitation to tender and the notices on the organisation
# giving notice of open competitions

# ------------------ Interpretative and Decisional Instruments ------------------
# ****************** Interpretative Communications and Notices ******************
law_soft_law_strategy['Interpretative Communications and Notices'] \
    = 'Communication;Communications;Interpretation;Interpretative;Interpret;' \
      'Concept;Explain;Explanation;Explication;Explicate;Exposition;Supplement;Supplements'
# ;Note;Notes;Case;Cases
# ;Instruction


# ****************** Decisional Notices and Communications ******************
law_soft_law_strategy['Decisional Notices and Communications'] \
    = 'Notification;Notice;Notices;Circulars;Circular;Gazette;Aviso;Communiqué'
# Aviso: PRT
# Communiqué: FRA

# ****************** Decisional Guidelines, Codes and Frameworks ******************
#  This very connection to existing Community law
# Not limited to Aid
law_soft_law_strategy['Decisional Guidelines, Codes and Frameworks'] \
    = 'Code;Codes;Guidance;Guidances;Guide;Guides;Guideline;Guidelines;Guidelilnes;EnerGuide;Guidebook;Determination;' \
      'Framework;Frameworks;Outline;Outlines'

# ------------------ Steering Instruments ------------------
law_soft_law_strategy['Steering Instruments'] \
    = 'Recommendation;Recommendations;Opinion;Opinions;Resolutions;Resolution;Acknowledgements;Acknowledge;' \
      'Conclusion;Conclusions;ENERGY STAR;Comments;Comment;Declaration;Declarations;' \
      'Recognitions;Recognition;Recognize;Recognises;Confirmations;Confirmation;Confirm;Desirability;' \
      'Covenants;Covenant;Debate;Pact;Call;Calls;Partnership;Partner;Partners;' \
      'Initiative;Initiatives;Advice;Advisory;Proposes;Propose;Proposal;Proposals;Advocates;Advocate;' \
      'ecoENERGY;Demonstration;Result;Results;Evidence;View;' \
      'Suggestion;Suggest;Idea;Observation;Say;Calling upon;Inviting;Steering;MOU;MoC;Memorandum;' \
      'Agreement;Agreements;Protocol;Deal;Commitment;Announcement;Proclamation;Shall;' \
      'Collaborating;Collaboration;Collaborative;Cooperation;Co-operation'

# ‘principles’, ‘criteria’, ‘standards’ and ‘recommendations’
# As the following examples show, steering instruments may lay down new rules,
# independently of an existing legal framework,
# or may be adopted in the context of such a framework, prior to, simultaneous with or subsequent to legislation.

# ================== Other Strategy Plan or Target ==================
# law_soft_law_strategy['Other Strategy Plan or Target'] \
#     = 'Strategy;Strategies;Strategic;Accord;Policy;Policies;Pact;Voluntary;Audit;Audits;Projects;Project'

with open('law_soft_law_strategy_title_dict.json', 'w') as f:
    json.dump(law_soft_law_strategy, f)
