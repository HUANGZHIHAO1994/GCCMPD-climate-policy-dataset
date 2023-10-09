import time
import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import json

e = open("/home/zhhuang/climate_policy_paper/code/files/GOV_PRC.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(e)
csv_writer.writerow(['Policy', 'Year', 'Country', 'Policy_Content', 'URL', 'Scope', 'Source'])
e.close()


def get_page(url):
    ua = UserAgent()
    usr_ag = ua.random
    headers = {'User-Agent': usr_ag}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    response.encoding = 'utf-8'
    response = response.text
    return response


num_list = ['国土资源、能源%5C矿产', '国土资源、能源%5C煤炭', '国土资源、能源%5C石油与天然气', '国土资源、能源%5C电力']
for num_d in num_list:
    n_k = 1
    while True:
        print('爬取序号{}--------爬取页数{}'.format(num_d, n_k))
        url = 'http://xxgk.www.gov.cn/search-zhengce/?callback=jQuery1124017801747997612605_1678622720550&mode=smart&sort=relevant&page_index={}&page_size=10&title=&theme={}&_=1678622720562'.format(
            n_k, num_d)
        for n_p in range(3):
            try:
                res_1 = str(get_page(url)).split('jQuery1124017801747997612605_1678622720550(')[-1][0:-2]
                break
            except:
                continue
        print(res_1)
        # data_1 = etree.HTML(res_1)
        js_data = json.loads(res_1)
        target_list = js_data['data']
        print(target_list)
        n_k += 1
        if len(target_list) < 1:
            break
        for single_target in target_list:
            try:
                try:
                    Policy = single_target['title']
                except:
                    Policy = ''
                try:
                    Year = str(single_target['writetime']).split('年')[0].replace('\'', '')
                except:
                    Year = ''

                url_2 = single_target['url']
                res_2 = get_page(url_2)
                data_2 = etree.HTML(res_2)
                try:
                    Policy_Content_ls_ache = data_2.xpath('//td[@class="b12c"]//text()')[0]
                    Policy_Content_ls = data_2.xpath('//td[@class="b12c"]//text()')
                    Policy_Content = ''
                    for single_Policy_Content in Policy_Content_ls:
                        if single_Policy_Content != '\n':
                            Policy_Content += single_Policy_Content.replace("\n", ' ').strip()
                except:
                    Policy_Content = ''
                if Policy != '':
                    e = open("/home/zhhuang/climate_policy_paper/code/files/GOV_PRC.csv", 'a+', encoding='utf-8-sig',
                             newline='')
                    csv_writer = csv.writer(e)
                    csv_writer.writerow([Policy, Year, 'China', Policy_Content, url_2, 'National', 'GOV_CHN'])
                    e.close()
                    print([Policy, Year, 'China', Policy_Content, url_2, 'National', 'GOV_CHN'])
                time.sleep(2)
            except:
                time.sleep(2)
                continue
