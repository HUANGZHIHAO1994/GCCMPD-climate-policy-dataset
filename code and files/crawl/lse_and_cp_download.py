import requests
import shutil


def download_source(url, output_path, chunk_size=512):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    response = requests.get(url=url, stream=True, headers=headers)
    with open(output_path, mode='wb') as f:
        for chunk in response.iter_content(chunk_size):
            f.write(chunk)


url_list = ['https://climate-laws.org/legislation_and_policies.csv']
for index, single_url in enumerate(url_list):
    try:
        if index == 0:
            download_source(single_url, 'lse.csv')
        elif index == 1:
            download_source(single_url, 'cp.csv')
    except:
        continue

for file in ['lse.csv']:
    shutil.move(file, '/home/zhhuang/climate_policy_paper/code/policy_db_iea_cp_cclw_update/{}'.format(file))
