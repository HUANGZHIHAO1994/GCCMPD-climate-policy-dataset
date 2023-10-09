import time
import requests
from fake_useragent import UserAgent
from lxml import etree
import csv

e = open("/home/zhhuang/climate_policy_paper/code/files/MEE_PRC.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(e)
csv_writer.writerow(['Policy', 'Year', 'Country', 'Policy_Content', 'URL', 'Scope', 'Source'])
e.close()


def get_page(url):
    ua = UserAgent()
    usr_ag = ua.random
    headers = {'User-Agent': usr_ag}
    response = requests.get(url, headers=headers, timeout=1.5)
    print(response.status_code)
    response.encoding = 'utf-8'
    response = response.text
    return response


num_list = [168, 169, 170, 174, 177, 178, 180, 182, 183, 184, 185, 186, 187, 188, 189]
for num_d in num_list:
    n_k = 0
    while True:
        print('爬取序号{}--------爬取页数{}'.format(num_d, n_k + 1))
        if n_k == 0:
            url = 'https://www.mee.gov.cn/xxgk2018/160/167/{}/index_6700.html'.format(num_d)
        else:
            url = 'https://www.mee.gov.cn/xxgk2018/160/167/{}/index_6700_{}.html'.format(num_d, n_k)
        res_1 = get_page(url)
        data_1 = etree.HTML(res_1)
        url_2_list = data_1.xpath('//div[@class="iframe-list"]/table//tr')
        print(url_2_list)
        n_k += 1
        if len(url_2_list) < 1:
            break
        for single_target in url_2_list:
            try:
                single_url2 = 'https://www.mee.gov.cn/xxgk2018' + str(
                    single_target.xpath('./td[2]/a/@href')[0]).replace('../../..', '')
                print(single_url2)
                res_2 = get_page(single_url2)
                data_2 = etree.HTML(res_2)
                try:
                    Policy = data_2.xpath('//li[@class="first"]/div/p/text()')[0]
                except:
                    try:
                        Policy = data_2.xpath('//h2[@class="neiright_Title"]/text()')[0]
                    except:
                        Policy = ''
                try:
                    Year = str(single_target.xpath('./td[1]/span/text()')[0]).split('-')[0]
                except:
                    Year = ''
                try:
                    Policy_Content_ls_ache = data_2.xpath('//div[@id="print_html"]//text()')[0]
                    Policy_Content_ls = data_2.xpath('//div[@id="print_html"]//text()')
                    Policy_Content = ''
                    for single_Policy_Content in Policy_Content_ls:
                        if single_Policy_Content != '\n':
                            Policy_Content += single_Policy_Content.replace("\n", ' ').strip()
                except:
                    try:
                        Policy_Content_ls_ache = data_2.xpath('//div[@class="neiright_JPZ_GK_CP"]//text()')[0]
                        Policy_Content_ls = data_2.xpath('//div[@class="neiright_JPZ_GK_CP"]//text()')
                        Policy_Content = ''
                        for single_Policy_Content in Policy_Content_ls:
                            if single_Policy_Content != '\n':
                                Policy_Content += single_Policy_Content.replace("\n", ' ').strip()
                    except:
                        Policy_Content = ''
                if Policy != '':
                    e = open("/home/zhhuang/climate_policy_paper/code/files/MEE_PRC.csv", 'a+', encoding='utf-8-sig',
                             newline='')
                    csv_writer = csv.writer(e)
                    csv_writer.writerow([Policy, Year, 'China', Policy_Content, single_url2, 'National', 'MEE_PRC'])
                    e.close()
                    print([Policy, Year, 'China', Policy_Content, single_url2, 'National', 'MEE_PRC'])
                time.sleep(2)
            except:
                time.sleep(2)
                continue
