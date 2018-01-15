import bs4
from subprocess import call
import manga  # 引入下载模块

import login as login_dmzj


# 读取我的订阅漫画
def check_rss(session, page=1, type_id=1, letter_id=0, read_id=2):
    page_data = {
        'page': page,
        'type_id': type_id,
        'letter_id': letter_id,
        'read_id': read_id
    }
    return session.post('https://i.dmzj.com/ajax/my/subscribe', data=page_data)


# 过滤页面内容
def filter_html_content(response):
    html = response.text  # 获得页面内容
    soup = bs4.BeautifulSoup(html, "html.parser")
    content_li = soup.find_all(class_='dy_content_li')  # 获取所有漫画条目
    item_list = []
    for item in content_li:
        title = item.h3.a.text  # 获取漫画标题
        url = item.p.em.a['href']  # 获取漫画链接
        item_list.append({'title': title, 'url': url})
    return item_list


# 提醒有更新，调用系统提示api
def notice(item_list=None):
    if item_list is None:
        item_list = []
    if len(item_list):
        # 读取所有更新漫画标题
        title_str = []
        for item in item_list:
            print(item)
            title_str.append('【' + item['title'] + '】')
        content = '|'.join(title_str)

        # 调取系统提示框
        cmd = 'display notification \"' + \
              content + '\" with title \"动漫之家订阅漫画更新\"'
        call(["osascript", "-e", cmd])


# 主函数
def main():
    # 登录，填写自己的用户名和密码
    session = login_dmzj.login('', '')

    # 读取我的订阅漫画
    r = check_rss(session)

    comic_list = filter_html_content(r)
    # 过滤内容并提醒
    notice(comic_list)

    # 开始下载漫画
    for comic in comic_list:
        manga.comic_main(comic['url'])


if __name__ == '__main__':
    main()
