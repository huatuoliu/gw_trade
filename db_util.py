#!/usr/bin/python
# coding:utf-8
from sqlalchemy import Column, String, Integer, Float, TIMESTAMP,  create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql
import time

Base = declarative_base()
class cond_order(Base):
    __tablename__ = "cond_order"
    order_id = Column(Integer, primary_key=True)
    stock_code = Column(String(20))
    direction = Column(String)
    action = Column(String)
    amount = Column(Integer)
    deal_price = Column(Integer)
    compare_price = Column(Integer)
    begin_in_day  = Column(Integer)
    end_in_day =  Column(Integer)
    state = Column(Integer)
    insert_time = Column(TIMESTAMP)
    update_time = Column(TIMESTAMP)
class db_util:
    def __init__(self):
        self.session = None

    def get_db_session(self):
        engine = create_engine('mysql+pymysql://root:root123@localhost:3306/orderdb?charset=utf8',echo=False)
        db_session = sessionmaker(bind=engine)
        return db_session

    def init_db(self):
        Session = self.get_db_session()
        self.session = Session()

    def close_db(self):
        self.session.close()

    def get_todo_orders(self, stock_code):
        if stock_code != "":
            order_list = self.session.query(cond_order).filter(cond_order.stock_code == stock_code, cond_order.state == 0).all()
        else:
            order_list = self.session.query(cond_order).filter(cond_order.state == 0).all()
        print order_list
        return order_list

    def get_all_orders(self, stock_code):
        if stock_code != "":
            order_list = self.session.query(cond_order).filter(cond_order.stock_code == stock_code).all()
        else:
            order_list = self.session.query(cond_order).all()
        print order_list
        return order_list

    def get_cond_order_bystock(self, stock_code):
        order_list = self.session.query(cond_order).filter(cond_order.stock_code==stock_code).all()
        return order_list

    def add_condition_order(self, stock_code, direction, compare_price, action, deal_price,  amount,  begin_in_day, end_in_day):
        #insert into db
        print "stock_code=", stock_code, ", direction=", direction, ", action=", action,  ", amount=",  amount, ",deal_price=", deal_price, "compare_price=", compare_price, ", begin_in_day=", begin_in_day, ", end_in_day=", end_in_day
        new_order = cond_order(order_id=0, stock_code=stock_code, direction=direction, action=action,  amount=amount, deal_price=deal_price, compare_price=compare_price,
                               begin_in_day=begin_in_day, end_in_day=end_in_day, state=0, insert_time=func.now())
        self.session.add(new_order)
        #print new_order.stock_code
        ret = self.session.commit()
        return 1

    def update_cond_order(self, order_id, state):
        self.session.query(cond_order).filter(cond_order.order_id == order_id).update({cond_order.state: state})
        ret = self.session.commit()
        return ret

    def cancel_cond_order(self, order_id):
        self.update_cond_order(order_id, 2)


db_util1 = db_util()
db_util1.init_db()
order_list = db_util1.get_cond_order_bystock("600036")
for row in order_list:
    print(row.__dict__)

#db_util1.add_condition_order("600036", 1, 17,  'B', 100,  17, 1430, 1500)
#db_util1.update_cond_order(3, 0)
