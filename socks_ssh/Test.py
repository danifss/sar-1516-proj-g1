import socket
import socks
import urllib2

socks.set_default_proxy(socks.SOCKS5, "localhost")
socket.socket = socks.socksocket

print urllib2.urlopen('http://www.google.com').read()