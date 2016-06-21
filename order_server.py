from db_util import *
from SimpleXMLRPCServer import SimpleXMLRPCServer

def is_even(n):
    return n % 2 == 0

class order_server:
    def __init__(self):
        self.db = db_util()
        self.db.init_db()
        self.init_server()
    def is_even(self, n):
        return n % 2 == 0

    def init_server(self):
        self.server = SimpleXMLRPCServer(("localhost", 8000))
        self.server.register_function(self.is_even, "is_even")
        self.server.register_function(self.db.add_condition_order, "add_condition_order")

    def run(self):
        #thread.start_new_thread(process_order, )
        self.server.serve_forever()

s = order_server()
s.run()

