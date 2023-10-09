import json
import pandas as pd
import numpy as np
import os


def get_dict(database):
    with open("{}.json".format(database), "r") as f:
        json_dict = json.load(f)
    return json_dict


if __name__ == '__main__':
    for d in ["law_soft_law_strategy_title_dict", "law_soft_law_strategy_content_dict"]:
        keywords = []
        hsl = []

        map_dict = get_dict(d)
        for i in map_dict:
            # print(i)
            hsl.append(i)
            # print(map_dict[i])
            keywords.append('; '.join(map_dict[i].split(";")))

        data = {'Hard and Soft Law': hsl,
                'Keywords': keywords}
        df = pd.DataFrame(data)
        print(df)

        with pd.ExcelWriter("{}.xlsx".format(d), engine='xlsxwriter',
                            engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
            df.to_excel(writer)
