from socket import socket
import sys, os

ADDR = ('127.0.0.1', 8848)


def main():
    s = socket()
    s.connect(ADDR)
    while True:
        print("""
        =======QUERY========
        1.注册  2.登录  3.退出
        """)
        cmd=input('请输入编号>>')
        if cmd=='1':
            s.send(cmd.encode())

if __name__ == '__main__':
    main()
