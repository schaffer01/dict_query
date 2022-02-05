import pymysql


class Database:
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', port=8848,
                                  password='123456', user='root',
                                  database='dict', charset='utf8')

    def generate_cur(self):
        self.cur = self.db.cursor()

    def check_name(self, name):
        sql = 'select * from user where name=s%'
        self.cur.execute(sql, name)
        if self.cur.fetchone():
            return False
        else:
            return True

    def register(self, name, passwd):
        try:
            sql = 'insert into user(name,passwd) values(s%,s%)'
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
        except Exception as e:
            print("写入出错:", e)
            self.db.rollback()
            return False
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

    def do_query(self, word):
        sql = "select mean from words where word=s%"
        self.cur.execute(sql, word)
        mean = self.cur.fetchall()[0]
        if mean:
            return mean
        else:
            return '无此单词'

    def do_insert_hist(self, name, word):
        try:
            sql = "insert into hist(name,word) values(%s,%s)"
            self.cur.execute(sql, [name, word])
            self.db.commit()
            return 'ok'
        except Exception as e:
            print(e)
            self.db.rollback()
            return e

    def do_hist(self, name):
        sql = "select word,query_time from hist where name=%s order by query_time desc limit 10"
        self.cur.execute(sql, [name])
        data=self.cur.fetchall()
        if not data:
            return '无历史记录'
        return data