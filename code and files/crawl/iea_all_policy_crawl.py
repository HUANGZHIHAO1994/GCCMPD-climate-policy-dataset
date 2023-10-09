import requests
from lxml import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from pymongo import MongoClient
import hashlib
import pandas as pd
from config import iea, policy, all_policy
from pymongo.errors import DuplicateKeyError
import openpyxl
from openpyxl import Workbook
import re
import os
import time
import shutil
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


# files_path = os.path.join(os.getcwd(), "files")
# if not os.path.exists(files_path):
#     os.makedirs(files_path)


class PoliciesSpider(object):
    def __init__(self):
        self.start_url = "https://www.iea.org/policies"
        self.headers = {
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        self.client = MongoClient()
        self.collection = self.client['IEA']['all_policy']

    def md5Encode(self, str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def get_url_list(self, url, page):
        new_url_list = [url + "?page=%d" % i for i in range(1, page + 1)]
        return new_url_list

    def parse(self, url):
        rest = requests.get(url, headers=self.headers)
        return rest.text

    def get_content_list(self, rest):
        html_rest = html.etree.HTML(rest)
        # 获取总条数
        total = html_rest.xpath('//span[contains(@class,"m-filter-bar__count")]/text()')[0]
        total = int(total)
        page = total // 30 + 1 if total % 30 > 0 else total // 30
        url_list = self.get_url_list(self.start_url, page)
        item_list = []
        list_url = []
        for i in url_list:
            rest_list = self.parse(i)
            rest_list_html = html.etree.HTML(rest_list)
            li_list = rest_list_html.xpath('//ul[@class="m-policy-listing-items"]/li')
            for li in li_list:
                new_item = dict()
                new_item['Policy'] = li.xpath('.//a[@class="m-policy-listing-item__link"]/text()')[0].replace('\n',
                                                                                                              "").strip()
                new_item['Country'] = li.xpath('./div[@class="m-policy-listing-item-row__content"]/span[1]/text()')[
                    0].replace('\n', "").strip()
                new_item['Year'] = li.xpath('./div[@class="m-policy-listing-item-row__content"]/span[2]/text()')[
                    0].replace('\n', "").strip()
                new_item['Status'] = li.xpath('./div[@class="m-policy-listing-item-row__content"]/span[3]/text()')[
                    0].replace('\n', "").strip()
                new_item['Jurisdiction'] = \
                    li.xpath('./div[@class="m-policy-listing-item-row__content"]/span[4]/text()')[0].replace('\n',
                                                                                                             "").strip()
                new_item['policy_url'] = "https://www.iea.org" + \
                                         li.xpath('.//a[@class="m-policy-listing-item__link"]/@href')[0]
                print(new_item)
                item_list.append(new_item)
                list_url.append(new_item['policy_url'])

        wb = Workbook()
        dt = wb.create_sheet('All_Policies', index=0)
        dt.append(['Policy', 'Country', 'Year', 'Status', 'Jurisdiction', 'policy_url', 'Topics', 'Type', 'Sectors',
                   'Technologies', 'LearnMore', 'Policy_Content', '_id'])

        #         data = []
        with ThreadPoolExecutor(max_workers=5) as pool:
            results = pool.map(self.parse_detail, list_url, item_list)
            all_policy.drop()
            for i in results:
                print(i)
                dt.append([ILLEGAL_CHARACTERS_RE.sub(r' ', i['Policy']), ILLEGAL_CHARACTERS_RE.sub(r' ', i['Country']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['Year']), ILLEGAL_CHARACTERS_RE.sub(r' ', i['Status']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['Jurisdiction']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['policy_url']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['Topics']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['Policy type']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['Sectors']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['Technologies']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['LearnMore']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['Policy_Content']),
                           ILLEGAL_CHARACTERS_RE.sub(r' ', i['_id'])])
                #                 data.append(i)

                self.save(i)

        wb.save(r'iea.xlsx')
        shutil.move("iea.xlsx", '/home/zhhuang/climate_policy_paper/code/policy_db_iea_cp_cclw_update/iea.xlsx')

    #         df = pd.DataFrame(data)
    #         print(df)
    #         # 指定生成的Excel表格名称
    #         file_path = pd.ExcelWriter('All_Policies.xlsx')
    #         # 替换空单元格
    #         df.fillna(' ', inplace=True)
    #         # 输出
    #         df.to_excel(file_path, encoding='utf-8', index=False, engine='xlsxwriter')
    #         # 保存表格
    #         file_path.save()

    def parse_detail(self, url, item):
        rest = self.parse(url)
        html_rest = html.etree.HTML(rest)
        topics_list = html_rest.xpath('//span[contains(text(),"Topics")]/following-sibling::ul/li/a/span[1]/text()')
        topics_list = [i.strip().replace('\n', '').replace('\xa0', '') for i in topics_list]
        # item['Topics'] = ';'.join(topics_list)
        topics_list_temp = set(";".join(set(topics_list)).split(';'))
        topics_list_temp.discard("")
        item['Topics'] = ";".join(topics_list_temp)

        policy_type_list = html_rest.xpath(
            '//span[contains(text(),"Policy types")]/following-sibling::ul/li/a/span[1]/text()')
        policy_type_list = [i.strip().replace('\n', '').replace('\xa0', '') for i in policy_type_list]
        # item['Policy type'] = ';'.join(policy_type_list)
        policy_type_list_temp = set(";".join(set(policy_type_list)).split(';'))
        policy_type_list_temp.discard("")
        item['Policy type'] = ";".join(policy_type_list_temp)

        sectors_list = html_rest.xpath('//span[contains(text(),"Sectors")]/following-sibling::ul/li/a/span[1]/text()')
        sectors_list = [i.strip().replace('\n', '').replace('\xa0', '') for i in sectors_list]
        # item['Sectors'] = ';'.join(sectors_list)
        sectors_list_temp = set(";".join(set(sectors_list)).split(';'))
        sectors_list_temp.discard("")
        item['Sectors'] = ";".join(sectors_list_temp)

        technologies_list = html_rest.xpath(
            '//span[contains(text(),"Technologies")]/following-sibling::ul/li/a/span[1]/text()')
        technologies_list = [i.strip().replace('\n', '').replace('\xa0', '') for i in technologies_list]
        # item['Technologies'] = ';'.join(technologies_list)
        technologies_list_temp = set(";".join(set(technologies_list)).split(';'))
        technologies_list_temp.discard("")
        item['Technologies'] = ";".join(technologies_list_temp)

        learn_more = html_rest.xpath('//span[contains(text(),"Learn more")]/../@href')
        item['LearnMore'] = learn_more[0] if len(learn_more) else ''

        content = html_rest.xpath('//div[contains(@class,"m-block__content")]/p[not(position()=last())]/text()')
        if len(content) > 0 and not content[0] == "":
            item['Policy_Content'] = '\n'.join(content).replace('\n', '').replace('\xa0', '').strip()
        else:
            content = html_rest.xpath('//div[contains(@class,"m-block__content")]/text()')
            if len(content) > 0 and not content[0] == "":
                item['Policy_Content'] = '\n'.join(content).replace('\n', '').replace('\xa0', '').strip()
            else:
                content = html_rest.xpath('//div[contains(@class,"m-block__content")]//font/text()')
                item['Policy_Content'] = '\n'.join(content).replace('\n', '').replace('\xa0', '').strip() if len(
                    content) > 0 else "未知"
        item['_id'] = self.md5Encode(
            (item["Policy"] + item["Country"] + item["Year"] + item["Policy_Content"]).encode('utf-8'))
        print(item)
        return item

    def save(self, item):
        try:
            self.collection.insert_one(item)
        except DuplicateKeyError as e:
            pass

    def run(self):
        rest = self.parse(self.start_url)
        self.get_content_list(rest)


if __name__ == '__main__':
    ps = PoliciesSpider()
    ps.run()
