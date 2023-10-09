import json
import pandas as pd
import numpy as np
import os

if __name__ == '__main__':
    keywords = []

    with open("Mitigation and Adaptation.txt") as f:
        adaptation_keywords = f.read().lower().split('\n')[0]

    adaptation_keywords = adaptation_keywords.replace(";", '; ')

    data = {'Mitigation and Adaptation': ["Adaption"],
            'Keywords': [adaptation_keywords]}
    df = pd.DataFrame(data)
    print(df)

    with pd.ExcelWriter("Mitigation and Adaptation.xlsx", engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
        df.to_excel(writer)
