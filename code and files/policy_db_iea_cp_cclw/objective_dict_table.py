import json
import pandas as pd
import numpy as np
import os


def get_dict(database):
    with open("{}.json".format(database), "r") as f:
        json_dict = json.load(f)
    return json_dict


if __name__ == '__main__':
    for d in ["iea_objective_dict", "cp_objective_dict", "lse_objective_dict"]:
        keywords = []
        objs = []
        subobjs = []

        map_dict = get_dict(d)
        for i in map_dict:
            # print(i)
            keywords.append(i)
            # print(map_dict[i])
            objs.append('; '.join(map_dict[i][0].split(";")))
            subobj_temp = []
            for j in map_dict[i][1].split(";"):
                if j:
                    subobj_temp.append(j.split(":")[1])
                # else:
                #     subobj_temp.append('')
            subobjs.append('; '.join(subobj_temp))

        data = {'Keywords': keywords,
                'Objective': objs,
                'Subobjective': subobjs}
        df = pd.DataFrame(data)
        print(df)

        with pd.ExcelWriter("{}.xlsx".format(d), engine='xlsxwriter',
                            engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
            df.to_excel(writer)
