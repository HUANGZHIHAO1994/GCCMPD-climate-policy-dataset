import time

import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import re

e = open("/home/zhhuang/climate_policy_paper/code/files/CDR_CCUS.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(e)
csv_writer.writerow(['Policy', 'Year', 'Keyword', 'Policy_Content', 'URL', 'Type', 'Source'])
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


res_1 = str(get_page(
    'https://cdrlaw.org/technical-pathway/carbon-capture-utilization-and-storage/?_cdr_res_type=eleg%2Creg%2Cpleg%2Chear%2Cdec%2Cpol%2Cnew')).replace(
    '\\', '')
# print(res_1)
max_page = int(
    re.search('<a class=\"facetwp-page last\" data-page=\".*?\"', res_1, re.S).group(0).split('data-page="')[-1].split(
        '\"')[0])
print('---------最大页数{}----------'.format(max_page))
# time.sleep(11111)

for i in range(1, max_page + 1):
    if i == 1:
        url_2 = 'https://cdrlaw.org/technical-pathway/carbon-capture-utilization-and-storage/?_cdr_res_type=eleg%2Creg%2Cpleg%2Chear%2Cdec%2Cpol%2Cnew'
    else:
        url_2 = 'https://cdrlaw.org/technical-pathway/carbon-capture-utilization-and-storage/?_cdr_res_type=eleg%2Creg%2Cpleg%2Chear%2Cdec%2Cpol%2Cnew&_paged={}'.format(
            i)
    for r_t in range(3):
        try:
            res_2 = get_page(url_2)
            break
        except:
            continue
    data_2 = etree.HTML(res_2)
    url_list = data_2.xpath('//article/h2/a/@href')
    for url_3 in url_list:
        try:
            res_3 = get_page(url_3)
            data_3 = etree.HTML(res_3)
            try:
                Policy = data_3.xpath('//h1/text()')[0]
            except:
                Policy = ''
            try:
                Year = data_3.xpath('//div[@class="resource-year"]/text()')[0]
            except:
                Year = ''
            try:
                Keyword = ','.join(data_3.xpath('//div[@class="cdr_resource_keyword"]/a/text()'))
            except:
                Keyword = ''
            try:
                Policy_Content_ls = data_3.xpath('//div[@class="entry-content"]/p//text()')
                Policy_Content_txt = ''
                for single_Policy_Content in Policy_Content_ls:
                    Policy_Content_txt += single_Policy_Content
            except:
                Policy_Content_txt = ''
            try:
                Type = data_3.xpath('//div[@class="resource-type"]/text()')[0].replace("\n", ' ').strip()
            except:
                Type = ''
            Source = 'CDR_CCUS'
            e = open("/home/zhhuang/climate_policy_paper/code/files/CDR_CCUS.csv", 'a+', encoding='utf-8-sig',
                     newline='')
            if Policy != '':
                csv_writer = csv.writer(e)
                csv_writer.writerow([Policy, Year, Keyword, Policy_Content_txt, url_3, Type, Source])
                e.close()
                print([Policy, Year, Keyword, Policy_Content_txt, url_3, Type, Source])
        except:
            continue
