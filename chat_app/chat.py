import socket
import threading
import os
from time import sleep
import public_ip
import os
import requests

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
        URL_delete ='http://localhost:8000/api/services/del/' + str(public_ip.get_lan_ip()) + "/" + str(port)
        r = requests.delete(URL_delete)
        os._exit(0)



class receiver (threading.Thread):
    def __init__(self, BUFFER_SIZE):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 0))
        self.s.listen(1)

    def run(self):
        print "Listening on port", self.s.getsockname()[1]
        print "Waiting for connection..."
        self.conn, self.addr = self.s.accept()
        print "Running"
        while 1:
            data = self.conn.recv(BUFFER_SIZE)
            if not data:
                break
            if data =='bye':
                break
            else:
                print "> ", data
        self.stop()

    def get_port(self):
        return str(self.s.getsockname()[1])

    def stop(self):
        URL_delete ='http://localhost:8000/api/services/del/' + str(public_ip.get_lan_ip()) + "/" + str(port)
        r = requests.delete(URL_delete)
        os._exit(0)


def register_service(ip, port):
    data = {
        "ip" : str(ip),
        "name" : "chat_app_" + str(port),
        "description" : "Chat end-to-end app using sockets without encryption",
        "port" : str(port)
    }

    try:
        r = requests.post('http://localhost:8000/api/services/', data=data)
    except:
        print "Error while registering service"
        os._exit(1)  


def delete_service(ip, port):
    URL_delete ='http://localhost:8000/api/services/del/' + str(ip) + "/" + str(port)
    r = requests.delete(URL_delete)


try:
    BUFFER_SIZE = 20
    thread_receiver = receiver(BUFFER_SIZE)
    thread_receiver.start()
    sleep(0.1)   

    register_service(public_ip.get_lan_ip(), thread_receiver.get_port())

    ip = raw_input("Connect to\nIP: ")
    port = int(raw_input("Port: "))
    thread_sender = sender(ip, port)
    thread_sender.start()
    
except KeyboardInterrupt:
    print "\nStoping"
    delete_service(public_ip.get_lan_ip(), thread_receiver.get_port())
    thread_receiver.stop()
    thread_sender.stop()
    os._exit(0)
