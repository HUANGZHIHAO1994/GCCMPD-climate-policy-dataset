import csv
import time

import requests
from lxml import etree
from fake_useragent import UserAgent


def get_page(url):
    ua = UserAgent()
    usr_ag = ua.random
    headers = {'User-Agent': usr_ag}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    response.encoding = 'utf-8'
    response = response.text
    # print(response)
    return response


e = open("/home/zhhuang/climate_policy_paper/code/files/ECOLEX_Treaty.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(e)
# [Policy,Year,Country_txt,Policy_Content,single_url_2,Subject,Document_Type,Keyword,Entry_into_force,'ECOLEX']
csv_writer.writerow(
    ['Policy', 'Year', 'Country', 'Policy_Content', 'URL', 'Subject', 'Document_Type', 'Keyword', 'Entry into force',
     'Source'])
e.close()

res = get_page(
    'https://www.ecolex.org/result/?type=treaty&xsubjects=Air+%26+atmosphere&xsubjects=Environment+gen.&xsubjects=Land+%26+soil&xsubjects=Mineral+resources&xsubjects=Agricultural+%26+rural+development&xsubjects=Energy&xsubjects=Forestry&xsubjects=General&xdate_max=2021&xdate_min=1900')
data = etree.HTML(res)
page_number = data.xpath("//a[contains(@class, 'btn btn-sm btn-default')][last()-1]/text()")[0]
print(page_number)

for i_1 in range(1, int(page_number) + 1):
    try:
        print('=========爬取至{}页==========='.format(i_1))
        if i_1 == 1:
            url_1 = 'https://www.ecolex.org/result/?type=treaty&xsubjects=Air+%26+atmosphere&xsubjects=Environment+gen.&xsubjects=Land+%26+soil&xsubjects=Mineral+resources&xsubjects=Agricultural+%26+rural+development&xsubjects=Energy&xsubjects=Forestry&xsubjects=General&xdate_max=2021&xdate_min=1900'
        else:
            url_1 = 'https://www.ecolex.org/result/?type=treaty&xsubjects=Air+%26+atmosphere&xsubjects=Environment+gen.&xsubjects=Land+%26+soil&xsubjects=Mineral+resources&xsubjects=Agricultural+%26+rural+development&xsubjects=Energy&xsubjects=Forestry&xsubjects=General&xdate_max=2021&xdate_min=1900&page={}'.format(
                i_1)
        res_1 = get_page(url_1)
        data_1 = etree.HTML(res_1)
        url2_list = data_1.xpath('//h3[@class="search-result-title"]/a/@href')
        for single_url2_ache in url2_list:
            try:
                print('***********爬取至{}条************'.format(url2_list.index(single_url2_ache)))
                single_url_2 = 'https://www.ecolex.org{}'.format(single_url2_ache)
                print(single_url_2)
                res_2 = get_page(single_url_2)
                # print(res_2)
                data_2 = etree.HTML(res_2)
                # ********['Policy','Year','Country','Abstract','URL','Subject','Document_Type','Keyword','Geographical_area','Entry into force notes','Source']******
                # Policy
                try:
                    Policy = data_2.xpath('//h1/text()')[0]
                except:
                    Policy = ''
                print(Policy)
                # 第一部分
                Year = ''
                Document_Type = ''
                Country = ''
                try:
                    other_data_list = data_2.xpath('//header/dl')[0]
                    dt_list = other_data_list.xpath('./dt/text()')
                    print(dt_list)
                    dd_list = other_data_list.xpath('./dd')
                    print(dd_list)
                    # time.sleep(111)
                    for s_1 in range(len(dt_list)):
                        try:
                            print(dt_list[s_1])
                            if 'Document type' in dt_list[s_1]:
                                Document_Type = dd_list[s_1].xpath('./text()')[0]
                            elif 'Date' in dt_list[s_1]:
                                Year = str(dd_list[s_1].xpath('./text()')[0]).split(', ')[-1]
                        except:
                            continue
                except:
                    pass
                print(Year, Document_Type, Country)
                # time.sleep(1111)

                # 第二部分
                Subject = ''
                Keyword = ''
                Entry_into_force = ''
                try:
                    other_data_list_2 = data_2.xpath('//section[@id="details"]/dl')[0]
                    dt_list_2 = other_data_list_2.xpath('./dt/text()')
                    dd_list_2 = other_data_list_2.xpath('./dd')
                    for s_2 in range(len(dt_list_2)):
                        try:
                            if 'Subject' in dt_list_2[s_2]:
                                Subject = dd_list_2[s_2].xpath('./text()')[0]
                            elif 'Keyword' in dt_list_2[s_2]:
                                Keyword_ls = dd_list_2[s_2].xpath('./span/text()')
                                for single_Keyword in Keyword_ls:
                                    if single_Keyword != Keyword_ls[-1]:
                                        Keyword += single_Keyword + ','
                                    else:
                                        Keyword += single_Keyword
                            elif 'Entry into force' in dt_list_2[s_2]:
                                Entry_into_force = dd_list_2[s_2].xpath('./text()')[0]
                        except:
                            continue
                except:
                    pass
                print(Subject, Keyword, Entry_into_force)

                Policy_Content = ''
                try:
                    Policy_Content = data_2.xpath('//p[@class="abstract"]/text()')[0]
                except:
                    pass
                try:
                    Policy_Content = data_2.xpath('//p[@class="comment"]/text()')[0]
                except:
                    pass
                print(Policy_Content)

                Country_txt = ''
                try:
                    Country_ls = data_2.xpath('//tbody[@class="body"]/tr/th/text()')

                    for single_Country in Country_ls:
                        if single_Country != Country_ls[-1]:
                            Country_txt += single_Country + ','
                        else:
                            Country_txt += single_Country
                except:
                    pass

                if Policy != '':
                    e = open("/home/zhhuang/climate_policy_paper/code/files/ECOLEX_Treaty.csv", 'a+',
                             encoding='utf-8-sig', newline='')
                    csv_writer = csv.writer(e)
                    csv_writer.writerow(
                        [Policy, Year, Country_txt, Policy_Content, single_url_2, Subject, Document_Type, Keyword,
                         Entry_into_force, 'ECOLEX_Treaty'])
                    e.close()
                    print(single_url_2)
            except:
                continue
    except:
        continue
