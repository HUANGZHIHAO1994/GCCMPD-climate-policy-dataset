import json
import pandas as pd
import numpy as np
import os


def get_dict(database):
    with open("{}.json".format(database), "r") as f:
        json_dict = json.load(f)
    return json_dict


if __name__ == '__main__':
    for d in ["iea_instrument_dict", "cp_instrument_dict", "lse_instrument_dict"]:
        keywords = []
        instrs = []
        secinstrs = []

        map_dict = get_dict(d)
        for i in map_dict:
            keywords.append(i)
            if map_dict[i][0] in ["", "No"]:

                instrs.append('; '.join(map_dict[i][1].split(";")))
                subsec_temp = []
                for j in map_dict[i][2].split(";"):
                    if j:
                        subsec_temp.append(j.split(":")[1])
                    # else:
                    #     subsec_temp.append('')
                secinstrs.append('; '.join(subsec_temp))
            elif map_dict[i][0] == "Sector":
                instrs.append('; '.join(map_dict[i][1].split(";")))
                secitr = ';'.join(
                    [map_dict[i][2]["Multi-sector"], map_dict[i][2]["Energy systems"], map_dict[i][2]["Transport"],
                     map_dict[i][2]["Buildings"], map_dict[i][2]["Industry"], map_dict[i][2]["AFOLU"]])
                subsec_temp = []
                for j in secitr.split(";"):
                    if j:
                        subsec_temp.append(j.split(":")[1])
                    # else:
                    #     subsec_temp.append('')
                secinstrs.append('; '.join(subsec_temp))

        data = {'Keywords': keywords,
                'Instrument': instrs,
                'Sector-Instrument': secinstrs}
        df = pd.DataFrame(data)
        print(df)

        with pd.ExcelWriter("{}.xlsx".format(d), engine='xlsxwriter',
                            engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
            df.to_excel(writer)
