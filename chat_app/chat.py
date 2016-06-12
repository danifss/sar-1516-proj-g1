import socket
import threading
from time import sleep
import public_ip
import json
import urllib2
import os
import random


class receiver (threading.Thread):
    def __init__(self, BUFFER_SIZE):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 0))
        self.s.listen(1)
        self.end = False
        

    def run(self):
        print "Listening on port", self.s.getsockname()[1]
        print "Waiting for connection..."
        self.conn, self.addr = self.s.accept()
        print "Running"
        while not self.end:
            data = self.conn.recv(BUFFER_SIZE)
            if not data: break
            if data =='bye':
                break
            else:
                print "> ", data
        self.stop()

    def get_port(self):
        return str(self.s.getsockname()[1])

    def stop(self):
        #self.s.close()
        self.end = True
        delete_service(public_ip.get_lan_ip(), get_port())
        os._exit(0)
        

class sender (threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def run(self):
        print "Send message: "
        while 1:
            msg = raw_input("\n")
            totalsent = 0
            self.s.send(msg)
            if msg =='bye':
                break
        self.stop()

    def get_port(self):
        return str(self.s.getsockname()[1])

    def stop(self):
        self.running = False
        #self.s.close()
        os._exit(0)


def register_service(ip, port):
    data = {
        "ip" : str(ip),
        "name" : "chat_app_" + str(port),
        "description" : "Chat end-to-end app using sockets without encryption",
        "port" : str(port)
    }

    try:
        req = urllib2.Request('http://localhost:8000/api/services/')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
    except:
        print "Error while registering service"
        os._exit(1)  


def delete_service(ip, port):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request('http://localhost:8000/api/services/del/' + ip + "/" + port)
    request.get_method = lambda: 'DELETE'
    url = opener.open(request)


try:
    BUFFER_SIZE = 20
    thread1 = receiver(BUFFER_SIZE)
    thread1.start()
    sleep(0.1)   

    register_service(public_ip.get_lan_ip(), thread1.get_port())

    ip = raw_input("Connect to\nIP: ")
    port = int(raw_input("Port: "))
    thread2 = sender(ip, port)
    thread2.start()
    
except KeyboardInterrupt:
    print "\nStoping"
    delete_service(public_ip.get_lan_ip(), thread1.get_port())
    thread1.stop()
    thread2.stop()
    os._exit(0)

