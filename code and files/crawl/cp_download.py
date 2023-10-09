from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random
import time

# s = Service(r"./chromedriver.exe")

#  随机请求头设置
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; Avant Browser; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
    'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0'
]

url = 'https://climatepolicydatabase.org/policies/export?page&_format=csv'
headers = {}
headers['User-Agent'] = random.choice(USER_AGENTS)
chrome_options = Options()
headers = random.choice(USER_AGENTS)
chrome_options.add_argument('--user-agent={}'.format(headers))  # 设置请求头的User-Agent
chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
# chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 设置下载路径
prefs = {
    "download.default_directory": r'/home/zhhuang/climate_policy_paper/code/files'}
chrome_options.add_experimental_option("prefs", prefs)

# driver = webdriver.Chrome(service=s, options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get(url)

element = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.ID, "vde-automatic-download"))
)

button = driver.find_element(By.ID, "vde-automatic-download")
driver.execute_script("arguments[0].click();", button)
driver.close()
