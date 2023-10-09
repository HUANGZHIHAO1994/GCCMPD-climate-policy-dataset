import os
import time
import shutil

# print(os.getcwd())
start = time.perf_counter()

os.system("python dedup.py")
os.system("python match_update.py")

end = time.perf_counter()
print("time cost:", end - start)
