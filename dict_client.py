from socket import socket
import sys, os
from getpass import getpass

ADDR = ('127.0.0.1', 8848)

s = socket()
s.connect(ADDR)


def do_query(name):
    while True:
        word = input('请输入单词>>')
        if ' ' in word:
            print('输入有误')
            continue
        elif word == '##':
            break
        msg = 'Q %s %s' % (name, word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        if data == '无此单词':
            print(data)
        else:
            print('%-10s: %s' % (word, data))


def do_hist(name):
    msg = 'H %s' % name
    s.send(msg.encode())
    while True:
        data = s.recv(1024).decode()
        if data == '##':
            break
        print(data)


def login_success(name, passwd):
    while True:
        print("""
                ==========QUERY==========
                1.查词   2.历史记录   3.退出
                """)
        cmd = input('请输入编号>>')
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_hist(name)
        elif cmd == '3':
            return
        else:
            print('输入有误，重新输入>>')


def do_register():
    while True:
        name = input('name(不能有空格）\n>>')
        if ' ' in name:
            print('名字输入有误')
            continue
        msg = 'R1 %s' % (name)
        s.send(msg.encode())
        if s.recv(48).decode() == 'ok':
            print('用户名有效')
        else:
            print('用户名被占用，请重新输入')
            continue
        while True:
            passwd = getpass('password（不能有空格）\n>>')
            passwd02 = getpass('reinput password>>')
            if passwd != passwd02 or (' ' in passwd):
                print('密码输入有误')
                continue
            break
        break
    msg = "R2 %s %s" % (name, passwd)
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'ok':
        print('注册成功')
        login_success(name, passwd)
    else:
        print(data)


def do_login():
    while True:
        name = input('输入用户名>>')
        passwd = getpass("password>>")
        if (' ' in name) or (' ' in passwd):
            print('用户名/密码输入有误')
            return
        else:
            break
    msg = 'L %s %s' % (name, passwd)
    s.send(msg.encode())
    data = s.recv(48).decode()
    if data == 'ok':
        login_success(name, passwd)
    else:
        print(data)


def do_exit():
    s.send(b'Exit')
    s.close()
    sys.exit('客户端退出')


def main():
    while True:
        print("""
        =======COMMAND========
        1.注册   2.登录   3.退出
        """)
        cmd = input('请输入编号>>')
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            do_exit()
        else:
            print('输入有误，重新输入>>')


if __name__ == '__main__':
    main()
