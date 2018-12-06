from selenium import webdriver


browser = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
browser.get('https://www.baidu.com')
print(browser.current_url)



