import json
import pandas as pd
import numpy as np
import os


def get_dict(database):
    with open("{}.json".format(database), "r") as f:
        json_dict = json.load(f)
    return json_dict


if __name__ == '__main__':
    for d in ["iea_sector_dict", "cp_sector_dict", "lse_sector_dict"]:
        keywords = []
        instrs = []
        subinstrs = []

        map_dict = get_dict(d)
        for i in map_dict:
            # print(i)
            keywords.append(i)
            # print(map_dict[i])
            instrs.append('; '.join(map_dict[i][0].split(";")))
            subsec_temp = []
            for j in map_dict[i][1].split(";"):
                if j:
                    subsec_temp.append(j.split(":")[1])
                # else:
                #     subsec_temp.append('')
            subinstrs.append('; '.join(subsec_temp))

        data = {'Keywords': keywords,
                'Sector': instrs,
                'Subsector': subinstrs}
        df = pd.DataFrame(data)
        print(df)

        with pd.ExcelWriter("{}.xlsx".format(d), engine='xlsxwriter',
                            engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
            df.to_excel(writer)
