# 模拟登陆动漫之家
def login(session, name, pas):
    login_data = {'nickname': name, 'password': pas}
    session.post('http://i.dmzj.com/doLogin', data=login_data)
    return session
