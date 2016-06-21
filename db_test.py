#coding=utf-8

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__ = 'user2'

	id = Column(String(20),primary_key=True)
	name = Column(String(20))


class School(Base):
	__tablename__ = 'school'
	id = Column(String(20), primary_key=True)
	name = Column(String(20))


#创建从Base派生的所有表
def createAll(eng):
	Base.metadata.create_all(eng)

#删除DB中所有的表
def dropAll(eng):
	Base.metadata.drop_all(eng)

#删除数据库中从Base派生的所有表

#创建session对象
if __name__ == '__main__':
	#创建数据库引擎
	eng = create_engine('mysql://root:root123@localhost:3306/orderdb?charset=utf8',echo=True)

	#设置回显
	#eng.echo = True

	#创建DBSession类型
	DBSession = sessionmaker(bind=eng)

	#创建session对象
	session = DBSession()

try:
	#创建表
	createAll(eng)

	#创建新User对象
	new_user = User(id='13', name='sdfdf')

	print(u'你好吗')

	#添加到session
	session.add(new_user)

	#提交保存到数据库
	session.commit()

except BaseException,e:
	print('e.message=%s' % str(e.message))

finally:
	session.close()
	#eng.close()
