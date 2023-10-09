import csv
from lxml import etree
import requests
from fake_useragent import UserAgent
import re
import json

e = open("/home/zhhuang/climate_policy_paper/code/files/CRT.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(e)
csv_writer.writerow(['Policy', 'Year', 'Country', 'Policy_Content', 'URL', 'Scope', 'Explanation', 'Agency', 'Source'])
e.close()


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


# 请求网址，所有数据都在一个网址
url = 'https://climate.law.columbia.edu/content/climate-reregulation-tracker'
res_1 = get_page(url)
# print(res_1)

# 获取Explanation库，对Explanation参数进行解析    #services_dept_data
Explanation_key_list = eval(
    re.findall('var services_dept_data = .*?;var services_aud_data', res_1)[0].replace(
        'var services_dept_data = ', '').replace(';var services_aud_data', ''))

# 建立Explanation映射，数字对应相应值
dict_Explanation = {}
# print(Explanation_key_list)
for e_1 in Explanation_key_list:
    dict_Explanation[e_1['id']] = e_1['label']
# print(dict_Explanation)

# 获取Agency库，对Agency参数进行解析   #services_aud_data
Agency_key_list = eval(re.search('var services_aud_data = .*?;var services_cat_data', res_1, re.S).group(0).replace(
    'var services_aud_data = ', '').replace(';var services_cat_data', ''))

# 建立Agency映射，数字对应相应值
dict_Agency = {}
for e_2 in Agency_key_list:
    dict_Agency[e_2['id']] = e_2['label']
# print(dict_Agency)

# 总数据
data_1 = re.search('var services_data = .*?;var services_dept_data', res_1, re.S).group(0).replace(
    'var services_data = ', '').replace(';var services_dept_data', '')
js_data = json.loads(data_1)
for single_data in js_data:
    # 三个固定数据
    Country = 'USA'
    Scope = 'National'
    Source = 'Climate-Reregulation-Tracker'
    Policy = single_data['title']
    print(Policy)

    Year = str(single_data['date']).split('-')[0].replace('\"', '')
    print(Year)

    Summary = single_data['summary']
    print(Summary)

    # 解析Explanation参数，依次用数值解析处真正的值
    Explanation_num_list = list(single_data['departments_id'])
    Explanation_txt = ''
    for single_Explanation_num in Explanation_num_list:
        if single_Explanation_num != Explanation_num_list[-1]:
            Explanation_txt += dict_Explanation[single_Explanation_num] + ','
        else:
            Explanation_txt += dict_Explanation[single_Explanation_num]
    print(Explanation_txt)
    # 解析Agency参数，依次用数值解析处真正的值
    Agency_num_list = list(single_data['groups_id'])
    Agency_txt = ''
    for single_Agency_num in Agency_num_list:
        if single_Agency_num != Agency_num_list[-1]:
            Agency_txt += dict_Agency[single_Agency_num] + ','
        else:
            Agency_txt += dict_Agency[single_Agency_num]
    print(Agency_txt)
    # 构建每条文章的网址，获取内容
    url_t = 'https://climate.law.columbia.edu' + single_data['path']
    print(url_t)
    res_2 = get_page(url_t)
    data_2 = etree.HTML(res_2)
    main_txt = ''
    text_list = data_2.xpath(
        '//div[@class="field field--name-field-cu-wysiwyg field--type-text-long field--label-hidden field--item"]//text()')
    for single_text in text_list:
        if single_text != '':
            main_txt += single_text
    Policy_Content = Summary + '\n' + main_txt
    print(Policy)
    # 写入表格
    e = open("/home/zhhuang/climate_policy_paper/code/files/CRT.csv", 'a+', encoding='utf-8-sig', newline='')
    csv_writer = csv.writer(e)
    csv_writer.writerow([Policy, Year, Country, Policy_Content, url_t, Scope, Explanation_txt, Agency_txt, Source])
    e.close()
