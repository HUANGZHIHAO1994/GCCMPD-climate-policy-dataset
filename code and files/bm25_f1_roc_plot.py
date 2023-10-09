import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import warnings
from matplotlib.pyplot import MultipleLocator
from sklearn.metrics import f1_score, classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
from tqdm import tqdm

warnings.filterwarnings("ignore")

if __name__ == '__main__':
    images_path = "/home/zhhuang/climate_policy_paper/paper_images"
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    draw = [1000, 2000, 3000, 4000, 5000, 6000, 6061, 7000, 8000]
    # draw = [1000, 2000, 3000, 3050, 3100, 6000, 6061, 7000]
    bm25_max = 0.
    # /home/zhhuang/climate_policy_paper/code/files
    bm25_man_all = pd.read_excel(
        "/home/zhhuang/climate_policy_paper/code/files/policy_db_complete.xlsx", sheet_name="raw_data")
    bm25_man_dup_all = pd.read_excel(
        "/home/zhhuang/climate_policy_paper/code/files/policy_db_complete.xlsx", sheet_name="dup")
    bm25_man_dup_all = bm25_man_dup_all[bm25_man_dup_all["group_policy_number"] > 1]
    # bm25_dup_list = []
    # for idx1, idx2 in zip(bm25_man_dup_all["A"].to_list(), bm25_man_dup_all["dup_index"].to_list()):
    #     year1 = bm25_man_all[bm25_man_all["A"] == idx1]["Year"].values[0]
    #     iso1 = bm25_man_all[bm25_man_all["A"] == idx1]["ISO_code"].values[0]
    #     jud1 = bm25_man_all[bm25_man_all["A"] == idx1]["Jurisdiction_standard"].values[0]
    #
    #     year2 = bm25_man_all[bm25_man_all["A"] == idx2]["Year"].values[0]
    #     iso2 = bm25_man_all[bm25_man_all["A"] == idx2]["ISO_code"].values[0]
    #     jud2 = bm25_man_all[bm25_man_all["A"] == idx2]["Jurisdiction_standard"].values[0]
    #     if (year1 == year2) and (iso1 == iso2) and (jud1 == jud2):
    #         bm25_dup_list.append(idx1)
    #         bm25_dup_list.append(idx2)
    # print(len(set(bm25_dup_list)))
    bm25_dup_list = set(bm25_man_dup_all["A"].to_list() + bm25_man_dup_all["dup_index"].to_list())
    # print(len(bm25_dup_list))
    bm25_man_all = bm25_man_all.sort_values(by=['bm25_score_first'], ascending=False)
    # print(bm25_man_all)

    preds_dict = dict()
    # labs_dict = dict()

    a = bm25_man_all["A"].to_list()
    labs = [0] * len(a)
    for idx, p in enumerate(a):
        if p in bm25_dup_list:
            labs[idx] = 1

    optimal_rank = 0
    max_f1 = 0.
    f1 = []
    top_bm25 = []
    bar = tqdm(range(1000, 8001), desc='Optimal rank', ncols=150)
    for i in bar:
        top_bm25.append(i)
        preds = [0] * len(a)

        bm25_temp = a[:i]
        # print(bm25_temp["A"].to_list())
        # p_list_temp = set(bm25_temp["A"].to_list())
        for idx, p in enumerate(a):
            if p in bm25_temp:
                preds[idx] = 1
        if i in draw:
            preds_dict[i] = preds
        # print(sum(preds))

        macro_f1 = f1_score(labs, preds, average='macro', zero_division=1)
        f1.append(macro_f1)
        if macro_f1 > max_f1:
            max_f1 = macro_f1
            optimal_rank = i

            report = classification_report(labs, preds, zero_division=1, output_dict=True)
            print(report)

            df = pd.DataFrame(report).transpose()

    df.to_csv('/home/zhhuang/climate_policy_paper/code/model_save/optimal_rank.csv', index=True)

    fig, ax = plt.subplots(figsize=(10, 10))

    # colors = cycle(["aqua", "darkorange", "cornflowerblue"])
    for d in draw:
        #         fpr, tpr, _ = roc_curve(preds_dict[d], labs, pos_label=1)
        RocCurveDisplay.from_predictions(
            preds_dict[d],
            labs,
            name=f"ROC curve for BM25 score top {d}",
            # color=color,
            ax=ax,
        )

    plt.plot([0, 1], [0, 1], "k--", label="chance level (AUC = 0.5)")
    plt.axis("square")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC curve for BM25 ranking")
    plt.legend()
    plt.savefig('/home/zhhuang/climate_policy_paper/paper_images/bm25_rank_roc_plot.svg', dpi=1000, bbox_inches='tight')
    # plt.show()

    plt.figure(figsize=(12, 6))

    plt.plot(top_bm25, f1, color="b", linewidth=2, label="macro f1 score")
    # plt.annotate("", xy=(4166, 0.846), xytext=(1500, 0.905),
    #              arrowprops=dict(arrowstyle="->, widthA=2.0, widthB=0.5", lw=3, alpha=0.6))
    # plt.annotate("", xy=(6850, 0.74), xytext=(4166, 0.846),
    #              arrowprops=dict(arrowstyle="->, widthA=2.0, widthB=0.5", lw=3, color='red', alpha=0.6))
    # # plt.arrow(1000, 0.885, 2930 - 1000, 0.845 - 0.885, width=0.001, length_includes_head=True,head_width=0.05, head_length=0.1)
    # plt.vlines(4166, 0.74, 0.91, linestyles='dashed', colors='red', linewidth=2)
    # plt.hlines(0.848, 1500, 7000, linestyles='dashed', colors='red', linewidth=2)
    plt.title('The proportion of duplicates in the highest-N BM25 score', fontsize=18)
    plt.ylim(0.50, 0.82)
    # plt.xlim(1500, 7000)
    plt.vlines(6061, 0.50, 0.82, linestyles='dashed', colors='red', linewidth=2)
    y_major_locator = MultipleLocator(0.02)
    x_major_locator = MultipleLocator(500)
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    ax.xaxis.set_major_locator(x_major_locator)

    plt.xlabel('Top N BM25 score', fontsize=15)
    plt.ylabel('Macro F1 Score', fontsize=15)
    plt.legend()
    plt.savefig('/home/zhhuang/climate_policy_paper/paper_images/bm25_rank_f1_plot.svg', dpi=1000, bbox_inches='tight')
    # plt.show()
