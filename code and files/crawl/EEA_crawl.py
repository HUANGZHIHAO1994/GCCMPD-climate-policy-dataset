import requests


def download_source(url, output_path, chunk_size=512):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    response = requests.get(url=url, stream=True, headers=headers)
    with open(output_path, mode='wb') as f:
        for chunk in response.iter_content(chunk_size):
            f.write(chunk)


# download_query: http://pam.apps.eea.europa.eu/?source={"track_total_hits":true,"query":{"match_all":{}},"display_type":"tabular","sort":[{"Country":{"order":"asc"}},{"ID_of_policy_or_measure":{"order":"asc"}}],"highlight":{"fields":{"*":{}}}}download_format: csv
url = 'http://pam.apps.eea.europa.eu/tools/download?download_query=http%3A%2F%2Fpam.apps.eea.europa.eu%2F%3Fsource%3D%7B%22track_total_hits%22%3Atrue%2C%22query%22%3A%7B%22match_all%22%3A%7B%7D%7D%2C%22display_type%22%3A%22tabular%22%2C%22sort%22%3A%5B%7B%22Country%22%3A%7B%22order%22%3A%22asc%22%7D%7D%2C%7B%22ID_of_policy_or_measure%22%3A%7B%22order%22%3A%22asc%22%7D%7D%5D%2C%22highlight%22%3A%7B%22fields%22%3A%7B%22*%22%3A%7B%7D%7D%7D%7D&download_format=csv'

download_source(url, '/home/zhhuang/climate_policy_paper/code/files/EEA.csv')
