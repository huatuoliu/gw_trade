import xmlrpclib
proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
print str(proxy.is_even(12))
proxy.add_condition_order("600036", 1, 1, 100, 17, 2, 3)
