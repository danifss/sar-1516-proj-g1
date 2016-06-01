import socks

s = socks.socksocket() # Same API as socket.socket in the standard lib

s.set_proxy(socks.SOCKS5, "localhost") # SOCKS4 and SOCKS5 use port 1080 by default

# Can be treated identical to a regular socket object
s.connect(("www.google.com", 80))
s.sendall("GET / HTTP/1.1 ...")
print s.recv(4096)