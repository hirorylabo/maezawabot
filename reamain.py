from random_password import random_password
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
from time import sleep
from gimei import Gimei
from lxml.html import fromstring
import os
from tempmail import TempMail

name = Gimei().name
tm = TempMail()
email = tm.get_email_address()
password = random_password()
print(email, password)

# ブラウザのオプションを格納する変数をもらってきます。
options = webdriver.ChromeOptions()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
# options.headless = True
options.add_argument("--incognito")
# http://www.freeproxylists.net/ja/?c=&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0
proxy_server = os.environ.get('https_proxy', os.environ.get('http_proxy'))
if proxy_server:
    options.add_argument('--proxy-server=%s' % proxy_server)
# ブラウザを起動する
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

# ブラウザでアクセスする
driver.get('https://twitter.com/i/flow/signup')

sleep(randint(20, 25))
# print(driver.find_element_by_xpath('//div[text()="かわりにメールアドレスを登録する""]'))
driver.find_element_by_xpath('//div[text()="かわりにメールアドレスを登録する"]').click()

sleep(randint(3, 5))
driver.find_element_by_xpath('//input[@name="name"]').send_keys(name.kanji)
sleep(randint(3, 5))
driver.find_element_by_xpath('//input[@name="email"]').send_keys(email)
sleep(randint(3, 5))
driver.find_element_by_xpath('//input[@name="email"]').click()

sleep(randint(3, 5))
driver.find_element_by_xpath('//span[text()="次へ"]').click()

sleep(randint(3, 5))
driver.find_element_by_xpath('//span[text()="登録する"]').click()

sleep(randint(10, 15))
mailbox = tm.get_mailbox(email)
if not mailbox:
    print('認証コードが受信されませんでした。')
    exit(1)
print(mailbox)
auth_code = fromstring(mailbox[0]['mail_html']).xpath('//td[@class="h1 black"]')[0].text.strip()
print(auth_code)

driver.find_element_by_xpath('//input[@placeholder="認証コード"]').send_keys(auth_code)

sleep(randint(3, 5))
driver.find_element_by_xpath('//span[text()="次へ"]').click()

sleep(randint(10, 15))
driver.find_element_by_xpath('//input[@name="password"]').send_keys(password)

sleep(randint(3, 5))
driver.find_element_by_xpath('//span[text()="次へ"]').click()

# sleep(randint(1, 2))
# driver.find_element_by_xpath('//font[text()="今はしない"]').click()
#
# sleep(randint(1, 2))
# driver.find_element_by_xpath('//font[text()="今のところスキップする"]').click()
#
# sleep(randint(1, 2))
# driver.find_element_by_xpath('//span[text()="Next"]').click()
#
# sleep(randint(1, 2))
# driver.find_element_by_xpath('//span[text()="Skip for now"]').click()

yousuck2020 = 'https://twitter.com/yousuck2020/status/1081544630754103296'

sleep(randint(5, 7))
# ブラウザでアクセスする
driver.get(yousuck2020)
sleep(randint(5, 7))
# ブラウザでアクセスする
driver.get(yousuck2020)

sleep(randint(2, 5))
driver.find_element_by_xpath('//span[text()="Follow"]').click()

sleep(randint(3, 5))
driver.find_element_by_xpath('//button[@class="ProfileTweet-actionButton  js-actionButton js-actionRetweet"]').click()

sleep(randint(3, 5))
driver.find_element_by_xpath('//button[@class="EdgeButton EdgeButton--primary retweet-action"]').click()

sleep(randint(3, 5))
driver.close()

print('Success:', email, password)
with open("success_list.txt", "a") as myfile:
    myfile.write("%s %s" % (email, password))
