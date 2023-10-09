import os
import time
import shutil

# print(os.getcwd())
start = time.perf_counter()

os.system("python iea_dedup.py")
os.system("python cp_dedup.py")

os.system("python iea_sector_dict_create.py")
os.system("python cp_sector_dict_create.py")
os.system("python lse_sector_dict_create.py")
os.system("python iea_sector_process.py")
os.system("python cp_sector_process.py")
os.system("python lse_sector_process.py")

os.system("python cp_iea_lse_region_process.py")

os.system("python iea_instrument_dict_create.py")
os.system("python cp_instrument_dict_create.py")
os.system("python lse_instrument_dict_create.py")
os.system("python iea_instrument_process.py")
os.system("python cp_instrument_process.py")
os.system("python lse_instrument_process.py")

os.system("python cp_iea_lse_annex_process.py")

os.system("python iea_objective_dict_create.py")
os.system("python cp_objective_dict_create.py")
os.system("python lse_objective_dict_create.py")
os.system("python iea_objective_process.py")
os.system("python cp_objective_process.py")
os.system("python lse_objective_process.py")

os.system("python cp_iea_lse_law_title_dict_create.py")
os.system("python cp_iea_lse_law_content_dict_create.py")
os.system("python cp_iea_lse_law_process.py")

os.system("python contat_three_db.py")
os.system("python concat_bm25_similar.py")

end = time.perf_counter()
print("time cost:", end - start)

update_path = os.path.join(os.getcwd(), "update_policies")
if not os.path.exists(update_path):
    os.makedirs(update_path)
shutil.move("bm25_result.xlsx", './update_policies/bm25_result.xlsx')
