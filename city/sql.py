# coding:utf-8

import MySQLdb

conn = MySQLdb.connect(host = "127.0.0.1", user = "root", passwd ='123', db = "db_house_price")
cursor = conn.cursor()
cursor.execute('insert into city(name,address,price) values(%s, %s,%s)', (name, address,price))
#print cursor.rowcount
conn.commit()
#cursor.close()
#cursor = conn.cursor()
cursor.execute('select * from city where name = %s', ('nj',))
values = cursor.fetchall()
print values
cursor.close()

conn.close()




# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi			  #导入twisted的包
import MySQLdb
import MySQLdb.cursors

class FirstscrapyPipeline(object):
	def __init__(self):							#初始化连接mysql的数据库相关信息
		self.dbpool = adbapi.ConnectionPool('MySQLdb',
				db = 'db_house_price',
				user = 'root',
				passwd = '123',
				cursorclass = MySQLdb.cursors.DictCursor,
				charset = 'utf8',
				use_unicode = False
		)

	# pipeline dafault function					#这个函数是pipeline默认调用的函数
	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self._conditional_insert, item)
		return item

	# insert the data to databases				 #把数据插入到数据库中
	def _conditional_insert(self, tx, item):
		sql = "insert into book values (%s, %s)"
		tx.execute(sql, (item["title"], item["link"]))


