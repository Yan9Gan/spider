from selenium import webdriver


# PhantomJS打开网站
browser = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe',
                              service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
# browser = webdriver.Chrome()
browser.get('https://www.zhenguo.com/housing/1772835/')
# 点击页面弹出遮挡广告，可改用以上chrome打开确认是否存在广告，若没有则可注释不用
browser.find_element_by_class_name('xcxh-dont-remind__times').click()
# 点击入住日期按钮
browser.find_element_by_xpath('//*[@id="bookingMain"]/div/div[1]/div[1]/div[1]/div/div[2]/button').click()
# 选中日历左侧，右侧方法类似
left_table = browser.find_element_by_xpath('//*[@id="bookingMain"]/div/div[1]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/table/tbody')
month_year_left = browser.find_elements_by_id('CalendarMonth__caption')[1].get_attribute('textContent')
# 遍历日历左侧每个日期的class=CalendarDay--blocked-calendar
for item in left_table.find_elements_by_class_name('CalendarDay--blocked-calendar'):
    # 取出日期和价格
    date = item.find_element_by_xpath('./button/div/div[1]/span').get_attribute('textContent')
    price = item.find_element_by_xpath('./button/div/div[2]/span').get_attribute('textContent')
    print(month_year_left, date, price)


