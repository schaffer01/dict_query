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

HOST = '127.0.0.1'
PORT = 8848
ADDR = (HOST, PORT)

signal.signal(signal.SIGCHLD, signal.SIG_IGN)


def handle(connfd):
    while True:
        try:
            data = connfd.recv(1024).decode()
        except Exception as e:
            print(e)
            return
        if not data:
            connfd.close()
            os._exit(0)
        print(connfd.getpeername(),':',data)



def main():  # 创建启动函数
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)
    print('listen the port 8848...')

    while True:
        try:
            connfd, addr = s.accept()
            print('connect with',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('谢谢')
        except Exception as e:
            print(e)
            continue

        p = Process(target=handle, args=(connfd,))
        p.daemon = True  # 父进程结束，所有子进程强制结束
        p.start()
if __name__ == '__main__':
    main()