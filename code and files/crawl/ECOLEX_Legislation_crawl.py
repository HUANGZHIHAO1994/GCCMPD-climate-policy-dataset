import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from lxml import etree
from fake_useragent import UserAgent


def get_page(url):
    ua = UserAgent()
    usr_ag = ua.random
    headers = {'User-Agent': usr_ag}
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    response.encoding = 'utf-8'
    response = response.text
    # print(response)
    return response


def parse_detail(url):
    result = []
    try:
        # print('***********爬取至{}条************'.format(url2_list.index(single_url2_ache)))
        single_url_2 = 'https://www.ecolex.org{}'.format(url)
        # print(single_url_2)
        res_2 = get_page(single_url_2)
        # print(res_2)
        data_2 = etree.HTML(res_2)
        # ********['Policy','Year','Country','Abstract','URL','Subject','Document_Type','Keyword','Geographical_area','Entry into force notes','Source']******
        # Policy
        try:
            Policy = data_2.xpath('//h1/text()')[0]
        except:
            Policy = ''
        # print(Policy)
        # 第一部分
        Year = ''
        Document_Type = ''
        Country = ''
        try:
            other_data_list = data_2.xpath('//header/dl')[0]
            dt_list = other_data_list.xpath('./dt/text()')
            # print(dt_list)
            dd_list = other_data_list.xpath('./dd')
            # print(dd_list)
            # time.sleep(111)
            for s_1 in range(len(dt_list)):
                try:
                    # print(dt_list[s_1])
                    if 'Country/Territory' in dt_list[s_1]:
                        Country = dd_list[s_1].xpath('./text()')[0].replace("\n", ' ').strip()
                    elif 'Document type' in dt_list[s_1]:
                        Document_Type = dd_list[s_1].xpath('./text()')[0].replace("\n", ' ').strip()
                    elif 'Date' in dt_list[s_1]:
                        Year = dd_list[s_1].xpath('./span/text()')[0].replace("\n", ' ').strip()
                except:
                    continue
        except:
            pass
        # print(Year, Document_Type, Country)
        # time.sleep(1111)

        # 第二部分
        Subject = ''
        Keyword = ''
        Geographical_area = ''
        Entry_into_force_notes = ''
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

                    elif 'Geographical area' in dt_list_2[s_2]:
                        Geographical_area = dd_list_2[s_2].xpath('./text()')[0]
                    elif 'Entry into force notes' in dt_list_2[s_2]:
                        Entry_into_force_notes = dd_list_2[s_2].xpath('./text()')[0]
                except:
                    continue
        except:
            pass
        # print(Subject, Keyword, Geographical_area, Entry_into_force_notes)

        Abstract = ''
        try:
            Abstract = data_2.xpath('//p[@class="abstract"]/text()')[0]
        except:
            pass
        try:
            Abstract = data_2.xpath('//p[@class="comment"]/text()')[0]
        except:
            pass
        # print(Abstract)

        if Policy != '':
            result = [Policy, Year, Country, Abstract, single_url_2, Subject, Document_Type, Keyword,
                      Geographical_area, Entry_into_force_notes, 'ECOLEX_Legislation']

    except:
        pass

    return result


e = open("/home/zhhuang/climate_policy_paper/code/files/ECOLEX_Legislation.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(e)
csv_writer.writerow(
    ['Policy', 'Year', 'Country', 'Policy_Content', 'URL', 'Subject', 'Document_Type', 'Keyword', 'Geographical_area',
     'Entry into force notes', 'Source'])
e.close()

res = get_page(
    'https://www.ecolex.org/result/?q=&type=legislation&xsubjects=Agricultural+%26+rural+development&xsubjects=Air+%26+atmosphere&xsubjects=Energy&xsubjects=Environment+gen.&xsubjects=Forestry&xsubjects=General&xsubjects=Land+%26+soil&xsubjects=Mineral+resources&xdate_min=1900&xdate_max=2021')
data = etree.HTML(res)
page_number = data.xpath("//a[contains(@class, 'btn btn-sm btn-default')][last()-1]/text()")[0]
print(page_number)

for i_1 in range(1, int(page_number) + 1):
    try:
        print('=========爬取至{}页==========='.format(i_1))
        if i_1 == 1:
            url_1 = 'https://www.ecolex.org/result/?q=&type=legislation&xsubjects=Agricultural+%26+rural+development&xsubjects=Air+%26+atmosphere&xsubjects=Energy&xsubjects=Environment+gen.&xsubjects=Forestry&xsubjects=General&xsubjects=Land+%26+soil&xsubjects=Mineral+resources&xdate_min=1900&xdate_max=2021'
        else:
            url_1 = 'https://www.ecolex.org/result/?type=legislation&xsubjects=Agricultural+%26+rural+development&xsubjects=Air+%26+atmosphere&xsubjects=Energy&xsubjects=Environment+gen.&xsubjects=Forestry&xsubjects=General&xsubjects=Land+%26+soil&xsubjects=Mineral+resources&page={}'.format(
                i_1)
        res_1 = get_page(url_1)
        data_1 = etree.HTML(res_1)
        url2_list = data_1.xpath('//h3[@class="search-result-title"]/a/@href')
        e = open("/home/zhhuang/climate_policy_paper/code/files/ECOLEX_Legislation.csv", 'a+', encoding='utf-8-sig',
                 newline='')
        csv_writer = csv.writer(e)
        with ThreadPoolExecutor(max_workers=10) as pool:
            results = pool.map(parse_detail, url2_list)
            for i in results:
                print(i)
                if i:
                    csv_writer.writerow(i)
        e.close()

    except:
        continue
