import Pyro4
from db_util import *

class order_server:
    def __init__(self):
        self.db = db_util()
        self.db.init_db()
        self.daemon = None
        self.init_server()

    def init_server(self):
        self.daemon = Pyro4.Daemon()                # make a Pyro daemon
        ns = Pyro4.locateNS()                  # find the name server
        uri = self.daemon.register(self.db)   # register the greeting maker as a Pyro object
        ns.register("db_util", uri)   # register the object with a name in the name server
        print("Rmi Server Ready.")
    def run(self):
        #thread.start_new_thread(process_order, )
        self.daemon.requestLoop()                   # start the event loop of the server to wait for calls

s = order_server()
s.run()




