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
law_soft_law_strategy['International Law'] = 'Treaties;Treaty;Covenants;Covenant'

# ****************** Law/Act ******************
law_soft_law_strategy['Law/Act'] = 'Law;Laws;Decree-Law;Act;Acts;Legislation;Legislations;Legislative;Statutes;Statute;Statutory'

# ****************** Decree/Order/Ordinance ******************
law_soft_law_strategy['Decree/Order/Ordinance'] = \
    'Ordinance;Ordinances;Order;Orders;Ordice;Decree;Decrees;Sub-Decree;Royal Decree;Royal Decrees;' \
    'Real Decreto;Portaria'

# ------------------ Regulations / Rules ------------------
law_soft_law_strategy['Regulation/Directive/Decision'] = \
    'Rules;Rule;Regulations;Regulation;Regulating;Directive;Directives;Decision;Decisions;CFR;' \
    'Prohibition;Ban;Banning;Obligation;Mandatory;Mandate;Interim Measures;Interim procedures'

# ================== Soft Law & Quasi-legislative ==================
# ------------------ Preparatory and Informative Instruments ------------------
# ****************** Preparatory Instruments ******************
law_soft_law_strategy['Preparatory Instruments'] \
    = 'Green Papers;Green Paper;White Paper;White Papers;Action Programmes;Action Programme;General Programmes;' \
      'General Programme;Action Plans;Action Plan;Action Program;Action Programs;Incentive Measures;Appropriate Measures;' \
      'Road Map;Act Programme;ENERGY STAR;Nationally determined contributions;Common Rules;Appropriate Provisions;' \
      'NDCs;NDC;Programs;Program;Programme;Programmes;Programming;Milestone;Milestones;Action;Actions;' \
      'Prepare;Preparation;Plan;Plans;Planned;Planning;Route;Roadmap;Roadmaps;Blueprint;Agenda;FYP;' \
      'Scheme;Schemes;Schedules;Schedule;Objectives;Objective;Vision;Pilot;Campaign;Campaigns;Bailout;' \
      'Goal;Goals;Budget;Targets;Target;Aimed;Aim;Aims;Report;Reporting;Package;Strategy;Strategies;Strategic;' \
      'Achieving;Achieve;Benchmark;Benchmarks;Phase;Phase-out;Statement;Trials;Tomorrow;Tests;Test;Sets;Set;Horizon'

# ****************** Informative Instruments ******************
law_soft_law_strategy['Informative Instruments'] = 'Information;Informations;.gov;Website;Info;Survey;Surveys;Catalogue'

# ------------------ Interpretative and Decisional Instruments ------------------
# ****************** Interpretative Communications and Notices ******************
law_soft_law_strategy['Interpretative Communications and Notices'] \
    = 'Communication;Communications;Interpretation;Interpretative;Instruction;Note;Notes;Case;Cases;' \
      'Concept;Explain;Explanation;Explication;Explicate;Exposition;Response'

# ****************** Decisional Notices and Communications ******************
law_soft_law_strategy['Decisional Notices and Communications'] \
    = 'Notification;Notice;Notices;Circulars;Circular;Determined;Determine;COM;Gazette'

# ****************** Decisional Guidelines, Codes and Frameworks ******************
# relate to existing Community law, P156
law_soft_law_strategy['Decisional Guidelines, Codes and Frameworks'] \
    = 'Code;Codes;Guidance;Guidances;Guide;Guides;Guideline;Guidelines;EnerGuide;Guidebook;' \
      'Standards;Standard;Standardization;Norm;Norms;Compliance;' \
      'Framework;Frameworks;Outline;Outlines;Principles;Principle;Solutions;Solution;' \
      'Level;Levels;Label;Labels;Labelling;Ecolabel;eco-label;List;Lists;Taxonomy;Directory;Booklet;' \
      'NOM;BDS;CP;NCM;NHN;MEPS;MEP;GB;GB/T;LI;LBN;KS;CNS;JS;RS;SANS;SNI;SASO;TIS;VC;NTC;EN;PROCEL;R-2000;' \
      'Tax deductions;Tax deduction;' \
      'IECC;CBES;HEC;RBES;BEES;NMECC;MUEC;MUBEC;CBECC;ECBC;AS/NZS;GSO;NSO;GOST;TCVN;S&L;50001;ISO;' \
      'Applicable;Guidelilnes;Performance Certificate'

# ------------------ Steering Instruments ------------------
law_soft_law_strategy['Steering Instruments'] \
    = 'Recommendation;Recommendations;Opinion;Opinions;Resolutions;Resolution;' \
      'Codes of Conduct;Conduct;Conclusion;Conclusions;Comments;Comment;Declaration;Declarations;Pact;Calls;' \
      'Initiative;Initiatives;Advice;Advisory;ecoENERGY;demonstration;Result;Results;' \
      'Agreement;Agreements;Protocol;Deal;Commitment;Announcement;Proclamation;' \
      'Stimulus;Stimulation;Rebates;Rebate;Refund;Free;Premium;Premiums;Partnership;Partner;Partners;' \
      'Aid;Aids;Tariff;Tariffs;Feed-in-tariffs;Feed-in-tariff;Subsidy;Subsidies;Exemption;Exemptions;Support;Supports;' \
      'Bonus;Awards;Award;Benefit;Benefits;Fund;Funds;Funded;Funding;Investing;Invest;Investment;Investments;' \
      'Steering;Memorandum;Promotion;Promote;Promoting;Incentive;Incentives;Free;Grants;Grant;Granted;' \
      'Loans;Loan;Loan Insurance;low interest loans;' \
      'Collaborating;Collaboration;Collaborative;Cooperation;Co-operation;Derogation;' \
      'Tax Credit;Tax Exemption;Tax-exemption;Kyoto Protocol;Toll;Tolls;Tax;Taxes;Taxation;VAT;Eco-Tax;' \
      'Pricing;GIS;Renovation;Co-financed;Co-financing;Finance;Financing;Financial;' \
      'Assistance;Assisted;Preferential;Proposes;Propose;Proposal;Proposals;MorSEEF;REN21;MOU'
# principles’, ‘criteria’, ‘standards’ and
# ‘recommendations’
# As the following examples show, steering instruments may lay down
# new rules, independently of an existing legal framework, or may be
# adopted in the context of such a framework, prior to, simultaneous with
# or subsequent to legislation.

# ================== Other Strategy Plan or Target ==================
# law_soft_law_strategy['Other Strategy Plan or Target'] \
#     = 'Strategy;Strategies;Strategic;Accord;Policy;Policies;Pact;Voluntary;Audit;Audits;Projects;Project'

with open('law_soft_law_strategy_dict.json', 'w') as f:
    json.dump(law_soft_law_strategy, f)
