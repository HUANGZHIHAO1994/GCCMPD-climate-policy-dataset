import time

from lxml import etree
import requests
from fake_useragent import UserAgent
import json
import csv


def get_page(url):
    ua = UserAgent()
    usr_ag = ua.random
    headers = {'User-Agent': usr_ag}
    # 'Cookie': 'qgqp_b_id=1cfcb377c049ff6efe08918be2359014; st_si=56864813917721; st_asi=delete; cdcfh=6793013397600842%2C3118213442497792; st_pvi=81312807735168; st_sp=2022-12-12%2023%3A25%3A14; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=5; st_psi=20221213123300162-119101302791-8364966167'}
    response = requests.get(url, headers=headers, timeout=1.5)
    print(response.status_code)
    response.encoding = 'utf-8'
    response = response.text
    return response


url_1 = 'https://icapcarbonaction.com/en/json/maplist'
res_1 = get_page(url_1)
js_data = json.loads(res_1)
print(js_data)
id_ls = []
for j_1 in js_data:
    id_ls.append(j_1['id'])
print(id_ls)

e = open("/home/zhhuang/climate_policy_paper/code/files/ICAP_ETS.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(e)
csv_writer.writerow(
    ['Policy', 'Year', 'Country', 'Policy_Content', 'URL', 'Scope', 'Allocation', 'Sectoral coverage', 'GHGs covered',
     'Offsets credits', 'Cap', 'Source'])
e.close()
print(len(id_ls))
for single_id in id_ls:
    try:
        url_2 = r'https://icapcarbonaction.com/en/ets_system/{}'.format(single_id)
        res_2 = get_page(url_2)
        # print(res_2)
        # time.sleep(1111)
        data_2 = etree.HTML(res_2)
        # Policy
        try:
            Policy = data_2.xpath('//h1[@class="ets-caption"]/text()')[0]
        except:
            Policy = ''
        # Year
        try:
            Year = data_2.xpath(
                '//div[@class="field field--label-above field--type-integer field-start-operation-year"]/div[2]/text()')[
                0].replace("\n", ' ').strip()
        except:
            Year = ''
        # Country
        try:
            Country = data_2.xpath(
                '//div[@class="field field--label-above field--type-entity_reference field-regions"]/div[2]/div[@class="field__content"]/text()')[
                0].replace("\n", ' ').strip()
        except:
            Country = ''
        # Policy_Content
        try:
            Policy_Content_ls = data_2.xpath(
                '//div[@class="field field--label-above field--type-text_long field-summary-short dropdown-menu hide-frame"]/div[@class="dropdown-menu__frame"]//text()')
            Policy_Content = ''
            for single_Policy in Policy_Content_ls:
                print(single_Policy)
                if single_Policy != '':
                    Policy_Content += single_Policy
            Policy_Content = Policy_Content.replace("\n", ' ').strip()
        except:
            Policy_Content = ''
        # url
        URL = url_2
        # Scope
        if '-' in Policy:
            Scope = 'SubNational'
            Country = Policy.split('-')[0].strip()
        else:
            Scope = 'National'
        # Allocation
        try:
            Allocation = data_2.xpath(
                '//div[@class="field field--label-above field--type-string field-allowance-alloc-summary"]/div[2]/text()')[
                0]
            Allocation = Allocation.replace("\n", ' ').strip()
        except:
            Allocation = ''
        # Sectoral coverage
        try:
            Sectoral_coverage_ls = data_2.xpath(
                '//div[@class="field field--label-above field--type-entity_reference field-sectoral-coverage"]/div[2]//div[@class="field field--label-hidden field--type-string field-name"]/div/text()')
            # Sectoral_coverage_txt = ''
            # print(Sectoral_coverage_ls)
            Sectoral_coverage_txt = ','.join(Sectoral_coverage_ls).replace('\n', '').replace(' ', '')
            # print(Sectoral_coverage_txt)
            # for single_Sectoral in Sectoral_coverage_ls:
            #     print(single_Sectoral)
            #     single_Sectoral = str(single_Sectoral).replace('\n', '').replace(' ', '')
            #     if single_Sectoral != Sectoral_coverage_ls[-1]:
            #         Sectoral_coverage_txt += single_Sectoral + ','
            #     else:
            #         Sectoral_coverage_txt += single_Sectoral
        except:
            Sectoral_coverage_txt = ''
        # GHGs covered
        try:
            GHGs_covered = data_2.xpath(
                '//div[@class="field field--label-above field--type-string_long field-ghgs-covered"]/div[2]/text()')[0]
            GHGs_covered = GHGs_covered.replace("\n", ' ').strip()
        except:
            GHGs_covered = ''
        # Offsets and credits
        try:
            Offsets_credits = data_2.xpath(
                '//div[@class="field field--label-above field--type-string field-offsets-credits-summary"]/div[2]/text()')[
                0]
            Offsets_credits = Offsets_credits.replace("\n", ' ').strip()
        except:
            Offsets_credits = ''
        # Cap
        try:
            Cap = \
                data_2.xpath(
                    '//div[@class="field field--label-above field--type-string field-cap-summary"]/div[2]/text()')[
                    0]
            Cap = Cap.replace("\n", ' ').strip()
        except:
            Cap = ''
        if Policy != '':
            e = open("/home/zhhuang/climate_policy_paper/code/files/ICAP_ETS.csv", 'a+', encoding='utf-8-sig',
                     newline='')
            csv_writer = csv.writer(e)
            csv_writer.writerow(
                [Policy, Year, Country, Policy_Content, URL, Scope, Allocation, Sectoral_coverage_txt, GHGs_covered,
                 Offsets_credits, Cap, 'ICAP'])
            e.close()
            print(URL)
    except:
        continue
