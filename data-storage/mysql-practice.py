import pymysql


"""创建数据库"""
# db = pymysql.connect(host='localhost', user='root', password='mysql', port=3306)
# cursor = db.cursor()
# cursor.execute('SELECT VERSION()')
# data = cursor.fetchone()
# print('Database version:', data)
# cursor.execute('CREATE DATABASE spider DEFAULT CHARACTER SET utf8')
# db.close()

db = pymysql.connect(host='localhost', user='root', password='mysql', port=3306, db='spider')
cursor = db.cursor()

"""创建表"""
# sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL,' \
#       ' age INT NOT NULL, PRIMARY KEY (id))'
# cursor.execute(sql)
# db.close()


"""插入数据"""
# id = '20120001'
# user = 'Bob'
# age = 20
#
# sql = 'INSERT INTO students(id, name, age) values (%s, %s, %s)'
# try:
#     cursor.execute(sql, (id, user, age))
#     db.commit()  # 执行了这句增删改等操作才生效
# except:
#     db.rollback()  # 报错就数据回滚
# db.close()

# data = {
#     'id': '20120004',
#     'name': 'Alice',
#     'age': 24
# }
# table = 'students'
# keys = ','.join(data.keys())
# values = ','.join(['%s'] * len(data))
# sql = 'INSERT INTO {table} ({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
# try:
#     if cursor.execute(sql, tuple(data.values())):
#         print('Successful')
#         db.commit()
# except:
#     print('Failed')
#     db.rollback()
# db.close()


"""更新数据"""
# sql = 'UPDATE students SET age=%s WHERE name=%s'
# try:
#     cursor.execute(sql, (25, 'Bob'))
#     db.commit()
# except:
#     db.rollback()
# db.close()


# data = {
#     'id': '20120002',
#     'name': 'John',
#     'age': 18
# }
#
# table = 'students'
# keys = ','.join(data.keys())
# values = ','.join(['%s'] * len(data))
#
# sql = 'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '.\
#     format(table=table, keys=keys, values=values)
# update = ','.join(["{key}=%s".format(key=key) for key in data])
# sql += update
# try:
#     if cursor.execute(sql, tuple(data.values())*2):
#         print('Successful')
#         db.commit()
# except:
#     print('Failed')
#     db.rollback()
# db.close()


"""删除数据"""
# table = 'students'
# condition = 'age > 20'
#
# sql = 'DELETE FROM  {table} WHERE {condition}'.format(table=table, condition=condition)
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()
# db.close()


"""查询数据"""
sql = 'SELECT * FROM students WHERE age>=20'
try:
    cursor.execute(sql)
    print('Count:', cursor.rowcount)
    # one = cursor.fetchone()
    # print('One:', one)
    results = cursor.fetchall()
    # print('Results:', results)
    # print('Results Type:', type(results))
    for row in results:
        print(row)
except:
    print('Error')









