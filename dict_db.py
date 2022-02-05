import pymysql


class Database:
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', port=8848,
                                  password='123456', user='root',
                                  database='dict', charset='utf8')

    def generate_cur(self):
        self.cur = self.db.cursor()

    def register(self, name, passwd):
        sql = 'select * from user where name=s%'
        self.cur.execute(sql, name)
        if self.cur.fetchone():
            return False
        else:
            try:
                sql = 'insert into user(name,passwd) values(s%,s%)'
                self.cur.execute(sql, [name, passwd])
                self.db.commit()
            except Exception as e:
                print("写入出错:", e)
                self.db.rollback()
                return
            return True

    def log_in(self, name, passwd):
        sql = "select * from user where name=s% and passwd=s%"
        self.cur.execute(sql, [name, passwd])
        if self.cur.fetchone():
            print('登录成功')
            return True
        else:
            print("输入有误")
            return False

    def close_cur(self):
        self.cur.close()

