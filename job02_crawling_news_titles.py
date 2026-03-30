from webbrowser import Chrome
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

options = ChromeOptions()
options.add_argument('lang=ko_KR')
# options.add_argument('headless')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
my_section = 0  # 0: Politics, 1: Economic, 2: Social, 3: Culture, 4: World, 5: IT  .....
url = 'https://news.naver.com/section/10{}'.format(my_section)
driver.get(url)

button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
# for i in range(10):
#     time.sleep(0.5)
#     driver.find_element(By.XPATH, button_xpath).click()

while True:
    try:
        button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
        driver.find_element(By.XPATH, button_xpath).click()
    except:
        break

time.sleep(1)
title_tags = driver.find_elements(By.CLASS_NAME, 'sa_text_strong')
# for title in title_tags:
#     print(title.text)

titles = []
for title in title_tags:
    titles.append(title.text)
df_titles = pd.DataFrame(titles, columns=['title'])
df_titles['category'] = category[my_section] # 섹션별로 카테고리 값 변경
print(df_titles.head())
df_titles.info()
df_titles.to_csv('news_titles_{}.csv'.format(category[my_section]))

# for i in range(1, 10):
#     for j in range(1, 6):
#         try:
#             title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
#             title = driver.find_element(By.XPATH, title_xpath).text
#             print(title)
#
#         except:
#             print(i, j)
#             continue


time.sleep(5)