import requests
from io import BytesIO
from PIL import Image
import time
import pandas as pd
import matplotlib.pyplot as plt
#
#
url = "https://photos.app.goo.gl/XsgAdsYZhTKwz25E6"
# res = requests.get(url)
# # request.get 요청
#
# links = []
# for j, line in enumerate(res.content.decode().split(',')):
#     if line.find('https://lh3.google')!=-1:
#         links.append(line)
# print(links)
# print(len(links))
# print(res.content[:100])
# res2 = requests.get(links[299][2:-1])
# print(res2.content)
#
# img = Image.open(BytesIO(res2.content))
# plt.imshow(img)
#


# "https://beomi.github.io/2017/02/27/HowToMakeWebCrawler-With-Selenium/"

path_chromedriver = "/Users/jiyoung/Documents/chromedriver"
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
# options = webdriver.ChromeOptions()
# options.add_argument("headless")
# driver = webdriver.Chrome(path_chromedriver, options)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
# def set_chrome_driver():
#     chrome_options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver


url2 = 'https://www.geeksforgeeks.org/how-to-scroll-down-to-bottom-of-page-in-selenium-using-javascriptexecutor/'
driver = webdriver.Chrome(path_chromedriver)
# driver = set_chrome_driver()

driver.implicitly_wait(3)
driver.get(url)
time.sleep(10)

# input_field = driver.find_element(By.XPATH,
input_field = driver.find_elements(By.CLASS_NAME, "RY3tic")
input_field[0].click()
input_field[0].send_keys(Keys.BACK_SPACE)

print(len(input_field))
action = ActionChains(driver)
action.move_to_element(input_field[len(input_field)-1]).perform()

driver.execute_script("window.scrollTo(0, document.body.scollHeight);")
input_field[0].send_keys(Keys.PAGE_DOWN)
# input_field[0].
# input_field.send_keys(Keys.)


# driver.execute_script("alert('이 브라우저 포커스')")


# ast_review = driver.find_element_by_css_selector('div.gws-localreviews__google-review:last-of-type')


print('a')