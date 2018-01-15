import requests
import pickle
import os


# 模拟登陆动漫之家，name：用户名，pas：密码
def login(name, pas):
    session = requests.Session()
    login_data = {'nickname': name, 'password': pas}
    session.post('http://i.dmzj.com/doLogin', data=login_data)
    return session


# 保存cookie
def save_cookie(filename, session):
    with open(filename, 'wb') as f:
        f.truncate()
        pickle.dump(session.cookies, f)


# 读取cookie
def load_cookie(filename):
    if os.path.exists('cookie.txt'):
        with open(filename, 'rb') as f:
            cookies = pickle.load(f)
            return cookies
    else:
        print('不存在cookie')
        return False


if __name__ == '__main__':
    # 登录，填写自己的用户名和密码
    # session = login('', '')

    # 读取本地cookie
    cookies = load_cookie('cookie.txt')
    page_data = {
        'page': 1,
        'type_id': 1,
        'letter_id': 0,
        'read_id': 1
    }
    r = requests.post('https://i.dmzj.com/ajax/my/subscribe', data=page_data, cookies=cookies)
    print(r.text)
