"""
字典服务器的逻辑处理单元
dict_server
技术分析：
    socket套接字 tcp
    process并发
"""
from socket import *
from multiprocessing import Process
import sys, os, signal
from dict_db import Database
from time import sleep

HOST = '127.0.0.1'
PORT = 8848
ADDR = (HOST, PORT)

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

db = Database()


def do_register_server(connfd, name, passwd):
    if db.register(name, passwd):
        connfd.send(b'ok')
    else:
        connfd.send("服务器出现bug".encode())


def do_checkname_server(connfd, name):
    if db.check_name(name):
        connfd.send(b'ok')
    else:
        connfd.send('用户名已存在'.encode())


def do_query_server(connfd, name, word):
    data = db.do_query(word)
    connfd.send(data.encode())
    if data != '无此单词':
        db.do_insert_hist(name, word)


def do_login_server(connfd, name, passwd):
    if db.log_in(name, passwd):
        connfd.send(b'ok')
    else:
        connfd.send('用户名/密码输入有误'.encode())


def do_hist_server(connfd, name):
    data=db.do_hist(name)
    if data=='无历史记录':
        connfd.send(data.encode())
        sleep(0.1)
        connfd.send(b'##')
        return
    for item in data:
        connfd.send(("%-15s %s"%item).encode())
        sleep(0.1)
    connfd.send(b'##')




def handle(connfd, addr):
    db.generate_cur()
    while True:
        try:
            data = connfd.recv(1024).decode()
        except Exception as e:
            print(e)
            break
        if not data or data == 'Exit':
            print(connfd.getpeername(), ':', '请求退出')
            break
        elif data.split(' ')[0] == 'R1':
            do_checkname_server(connfd, data.split(' ')[1])
        elif data.split(' ')[0] == 'R2':
            do_register_server(connfd, data.split(' ')[1], data.split(' ')[2])
        elif data.split(' ')[0] == 'L':
            do_login_server(connfd, data.split(' ')[1], data.split(' ')[2])
        elif data.split(' ')[0] == 'Q':
            do_query_server(connfd, data.split(' ')[1], data.split(' ')[2])
        elif data.split(' ')[0] == 'H':
            do_hist_server(connfd, data.split(' ')[1])
    db.cur.close()
    connfd.close()
    sys.exit('客户端退出')


def main():  # 创建启动函数
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)
    print('listen the port 8848...')

    while True:
        try:
            connfd, addr = s.accept()
            print('connect with', addr)
        except KeyboardInterrupt:
            s.close()
            db.db.close()
            sys.exit('谢谢')
        except Exception as e:
            print(e)
            continue

        p = Process(target=handle, args=(connfd, addr))
        p.daemon = True  # 父进程结束，所有子进程强制结束
        p.start()


if __name__ == '__main__':
    main()
