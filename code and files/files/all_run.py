import os
import time
import shutil

# print(os.getcwd())

start = time.perf_counter()
# First: Deep Crawl Data ==> Database.csv
for db in ['MEE_PRC', 'GOV_PRC', 'CDR_NETS', 'CDR_CCUS', 'CRT', 'ICAP_ETS', 'ECOLEX_Treaty', 'APEP',
           'ECOLEX_Legislation', 'EEA']:
    os.system("python /home/zhhuang/climate_policy_paper/code/crawl/{}_crawl.py".format(db))

# Second: Translate (Run in batches)
# Cut ECOLEX for Batch translation: ECOLEX_Legislation.csv ==> ECOLEX_Legislation_0~39.csv
os.system("python ECOLEX_cut.py")
# iea_cp_cclw.xlsx is from the policy_db_iea_cp_cclw_update process
# iea_cp_cclw.xlsx ==> iea_cp_cclw_0~9.csv
os.system("python iea_cp_cclw_cut.py")

# Database.csv ==> Database_EN.xlsx
# This step recommends running one file at a time, possibly in parallel
os.system("python policy_translate.py")

os.system("python ECOLEX_merge.py")
os.system("python iea_cp_cclw_merge.py")

# Third: Country_name iso annex income region process
os.system("python policy_db_region_iso_annex.py")
# For Topic
# os.system("policy_db_EN_merge_for_topic.py")

# Fourth: Merge as input to the prediction model
os.system("python policy_db_merge.py")

# Fiveth: Distinguishing between countries and cities through named entity recognition
os.system("python national_city_ner.py")

# shutil.copy("ALL_POLICIES_EN.xlsx", '/home/zhhuang/climate_policy_paper/code/data/ALL_POLICIES_EN.xlsx')

# Sixth: Merge Climatebert Multilabel Singlelabel results: merge_predict_result.py
# Seventh: BM25 Move Dupliactions: bm25_move_duplicate.py
# For Topic: BM25 Move Dupliactions: bm25_move_duplicate_for_topic.py

end = time.perf_counter()
print("time cost:", end - start)
