# 漫画爬虫文件

import requests
import time
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 引入显式等待相关包
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# 启动一个新的driver
def new_chrome(headless=False, timeout=15):
    chrome_options = Options()
    # chrome无界面形态配置，用不打开浏览器GUI的形式，但是要注意关闭进程
    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_page_load_timeout(timeout)  # 设置页面加载超时时间
    return driver


# 获取当前漫画页面的数据，并得到所有漫画图片路径
def page_spider(url, headless=False, timeout=20):
    # 创建driver
    driver = new_chrome(headless, timeout)
    comic_info = {'title': '', 'chapter': '', 'paths': []}

    try:
        driver.get(url)

        # 定时查询是否存加载完指定元素，设定10秒内不停查询，貌似默认是500ms频率查询一次
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='center_box']/img"))
        )

        # 返回漫画标题，话数，所有图片路径
        comic_info['title'] = driver.execute_script("return g_comic_name")
        comic_info['chapter'] = driver.execute_script("return g_chapter_name")
        comic_info['paths'] = add_host(driver.execute_script("return arr_pages"))

        return comic_info  # 通过返回js变量获取漫画信息
    except TimeoutException:
        print('当页面加载时间超过设定时间')
        return comic_info
    finally:
        driver.quit()  # 关闭driver释放内存


# 为图片路径添加完整路径
def add_host(urls):
    if len(urls):
        images = []
        for url in urls:
            images.append('http://images.dmzj.com/{}'.format(url))
        return images
    else:
        return []


# 获取文件名
def get_filename(path=''):
    return os.path.basename(path)


# 通过图片路径下载图片
def save(path, title, chapter, filename=None):
    # 设置请求头，模拟浏览器请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Referer': 'http://www.dmzj.com/category'
    }
    res = requests.get(path, stream=True, headers=headers)
    if filename is None or filename == '':
        filename = get_filename(path)  # 获取文件名保存
    if not os.path.exists(title):
        os.mkdir(title)
    if not os.path.exists('{}/{}'.format(title, chapter)):
        os.mkdir('{}/{}'.format(title, chapter))
    # 文件路径名
    _dir_path = '{}/{}/{}'.format(title, chapter, filename)
    with open(_dir_path, 'wb') as file:
        for line in res.iter_content():
            file.write(line)
    print('图片{}保存成功'.format(filename))


# 批量下载图片,comic.paths为路劲集合，sleep为间隔时间，避免频繁读取
def save_all(comic, sleep=1):
    if comic['paths'] and len(comic['paths']):
        print('【{}】{}开始下载...'.format(comic['title'], comic['chapter']))
        for path in comic['paths']:
            save(path, comic['title'], comic['chapter'])
            time.sleep(sleep)  # 延迟执行
        print('【{}】{}下载完毕'.format(comic['title'], comic['chapter']))


# 主函数，通过漫画某一话地址，事实上是第一页图片所在地址开始下载本话所有图片
def comic_main(url):
    # 1.获取当前漫画页面的数据，并得到所有漫画信息，包含标题，话数，
    comic = page_spider(url)

    # 2.下载该一话所有内容并保存
    save_all(comic)


# comic_main('http://manhua.dmzj.com/yiquanchaoren/31216.shtml#@page=1')
