import pandas as pd
import math
from tqdm import tqdm


def cut_df(file_name, n):
    df = pd.read_csv(file_name)
    df_num = len(df)
    every_epoch_num = math.floor((df_num / n))
    for index in tqdm(range(n)):
        file_name = f'./ECOLEX_Legislation_{index}.csv'
        if index < n - 1:
            df_tem = df[every_epoch_num * index: every_epoch_num * (index + 1)]
        else:
            df_tem = df[every_epoch_num * index:]
        df_tem.to_csv(file_name, index=False)


if __name__ == '__main__':
    cut_df('ECOLEX_Legislation.csv', 40)
