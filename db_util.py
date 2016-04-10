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
    direction = Column(Integer)
    action = Column(Integer)
    amount = Column(Integer)
    compare_price = Column(Integer)
    begin_in_day  = Column(Integer)
    end_in_day =  Column(Integer)
    state = Column(Integer)
    insert_time = Column(TIMESTAMP)
    update_time = Column(TIMESTAMP)
class db_util:
    def __init__(self):
        return

    def get_db_session(self):
        engine = create_engine('mysql+pymysql://root:root123@localhost:3306/orderdb')
        db_session = sessionmaker(bind=engine)
        return db_session

db_util = db_util()
Session = db_util.get_db_session()
session = Session()
new_order = cond_order(order_id=0, stock_code="600036", direction=1, action=1,  amount=1000, compare_price=14900,
                       begin_in_day=0, end_in_day=0, state=0, insert_time=func.now())
print new_order.compare_price
session.add(new_order)
print "fasdfa"
#print new_order.stock_code
session.commit()

order_list = session.query(cond_order).filter(cond_order.stock_code=='600036').all()
print order_list
session.close()

