import pandas as pd
import math
from tqdm import tqdm


def cut_df(file_name, n):
    df = pd.read_excel(file_name, sheet_name="all_policies_dedup")
    df_num = len(df)
    every_epoch_num = math.floor((df_num / n))
    for index in tqdm(range(n)):
        file_name = f'./iea_cp_cclw_{index}.csv'
        if index < n - 1:
            df_tem = df[every_epoch_num * index: every_epoch_num * (index + 1)]
        else:
            df_tem = df[every_epoch_num * index:]
        df_tem.to_csv(file_name, index=False)


if __name__ == '__main__':
    cut_df("iea_cp_cclw.xlsx", 10)
