
from SimpleXMLRPCServer import SimpleXMLRPCServer




def add_condition_order(stock_code, amount, up_price, down_price, insert_time)
    #insert into db

def is_even(n):
    return n % 2 == 0

server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
#server.register_function(is_even, "is_even")

thread.start_new_thread(process_order, )
server.serve_forever()
