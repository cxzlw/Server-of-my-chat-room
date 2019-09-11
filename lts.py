from flask import *

import file_op as file


a = Flask(__name__)

admin_list = []
try:
    port = file.read('port.lwf')
except Exception:
    port = int(input('Set port:'))
    file.save(port, 'port.lwf')
try:
    userinfo = file.read('userinfo.lwf')
except Exception:
    userinfo = {'admin': 'admin'}
    file.save(userinfo, 'userinfo.lwf')
try:
    m = file.read('message.lwf')
except Exception:
    m = []
    file.save(m, 'message.lwf')
try:
    admin_list = file.read('admin_list.lwf')
except Exception:
    admin_list = ['admin']
    file.save(admin_list, 'admin_list.lwf')
try:
    ltsname = file.read('ltsname.lwf')
except Exception:
    ltsname = '未命名'
    file.save(ltsname, 'ltsname.lwf')


def list_to_html(list_a):
    st = ''
    for x in list_a:
        st += f'''
<p>
    <a>{x}</a>
</p>
'''
    return st


@a.route('/<thing>')
def send(thing):
    if 'username' in session:
        nowuser = session['username']
    else:
        nowuser = '匿名用户'
    m.append(f'{nowuser}:{thing}')
    file.save(m, 'message.lwf')
    print(f'{nowuser}:{thing}')
    return redirect('/')


@a.route('/favicon.ico')
def favicon():
    return ''


@a.route('/')
def get_message():
    return f'''
<p>
        <a>{ltsname}</a>
</p>
<p>
        <a>消息列表</a>
</p>
''' + list_to_html(m) + f'''
<p>
        <a>在网址后面加 /(消息) 发送消息</a>
</p>
<p>
        <a>在网址后面加 /r/(用户名)/(密码) 注册用户</a>
</p>
<p>
        <a>在网址后面加 /l/(用户名)/(密码) 登录用户</a>
</p>
<p>
	<a href="/">点击刷新</a> 
</p>
'''


@a.route('/l/<username>/<password>')
def login(username, password):
    if username not in userinfo:
        return f'''
<p>
    <a>用户{username}不存在</a>
</p>
<p>
	<a href="/">点击刷新</a> 
</p>
'''
    elif userinfo[username] == password:
        session['username'] = username
        m.append(f'欢迎:\'{username}\'来到{ltsname}')
        file.save(m, 'message.lwf')
        return redirect('/')
    else:
        return f'''
<p>
    <a>密码错误:{username}</a>
</p>
<p>
    <a href="/" target="_blank">点击返回</a>
</p>
'''


@a.route('/r/<username>/<password>')
def register(username, password):
    if username in userinfo:
        return f'''
<p>
    <a>用户{username}已存在</a>
</p>
<p>
	<a href="/">点击刷新</a> 
</p>
'''
    else:
        userinfo[username] = password
        file.save(userinfo, 'userinfo.lwf')
        m.append(f'欢迎:\'{username}\'注册{ltsname}账号')
        file.save(m, 'message.lwf')
        return redirect('/')


# # 管理员设置变量
# @a.route('/admin/set/<var>/<thing>')
# def admin_set(var, thing):
#     if 'username' in session:
#         nowuser = session['username']
#     else:
#         nowuser = '匿名用户'
#     if nowuser in admin_list:
#         exec(f'global {var}')
#         exec(f'{var} = {thing}')
#         return str(eval(var))
#     else:
#         return f'''
# <p>
#     <a>用户{nowuser}无权限</a>
# </p>
# <p>
# 	<a href="/">点击刷新</a>
# </p>
# '''


a.secret_key = 'kslwnbeqbsybnbbjwhnb'
a.run(host='0.0.0.0', port=port)
