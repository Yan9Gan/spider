from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql

db = pymysql.connect(host='localhost', user='root', password='mysql', port=3306, db='JDipad')
cursor = db.cursor()

sql = 'CREATE TABLE IF NOT EXISTS ipad (name VARCHAR(255) NOT NULL, price INT NOT NULL,' \
      ' link VARCHAR(255) NOT NULL)'
cursor.execute(sql)

browser = webdriver.PhantomJS()
browser.get('https://www.jd.com/')

browser.find_element_by_id('key').send_keys('ipad')
browser.find_element_by_id('key').send_keys(Keys.ENTER)
browser.find_element_by_css_selector('#search > div > div.form > button').click()

ul = browser.find_element_by_class_name('gl-warp')
for item in ul.find_elements_by_class_name('gl-item'):
    href = item.find_elements_by_xpath('./div/div[1]/a')[0].get_attribute('href')
    price = item.find_element_by_xpath('./div/div[2]/strong/i').text
    name = item.find_element_by_xpath('./div/div[3]/a/em').text
    name = ' '.join(name.split(' ')[2:])
    print(href)
    print(price, '-', name)
    sql = 'INSERT INTO ipad(name, price, link) values (%s, %s, %s)'
    try:
        cursor.execute(sql, (name, price, href))
        db.commit()  # 执行了这句增删改等操作才生效
    except:
        db.rollback()  # 报错就数据回滚
db.close()


