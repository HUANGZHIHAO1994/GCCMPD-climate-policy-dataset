import os
import time
import shutil

start = time.perf_counter()

for model in ["climate_bert", "bert", "lr", "nb", "svm"]:
    for i in ["law or strategy", "Policy Type"]:
        os.system("python train_{}.py --do_train --attribution '{}'".format(model, i))

for model in ["climate_bert", "bert", "lr", "nb", "svm"]:
    for i in ["law or strategy", "Policy Type"]:
        os.system("python train_{}.py --do_test --attribution '{}'".format(model, i))

end = time.perf_counter()
print("time cost:", end - start)
