import re, pymysql

db = pymysql.connect(host='127.0.0.1', port=3306,
                     user='root', password='123456',
                     database='dict', charset='utf8')
cur = db.cursor()
f = open('dict.txt', 'r')
args_list = []
for line in f:
    tup = re.findall(r'(\w+)\s+(.*)', line)[0]
    args_list.append(tup)
f.close()
sql = "insert into words(word,mean)values(%s,%s);"
try:
    cur.executemany(sql,args_list)
    db.commit()
except Exception as e:
    print(e)
    db.rollback()
cur.close()
db.close()
