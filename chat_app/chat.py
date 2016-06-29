import socket
import threading
import sys
from time import sleep
import public_ip
import os
import requests
import SshClient

BROKER_HOST = "http://192.168.1.1:8000"


class sender (threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.toRun = True

    def run(self):
        print "Send message: "
        while self.toRun:
            msg = raw_input("\n")
            totalsent = 0
            self.s.send(msg)
            if msg == 'bye':
                break
        self.stop()

    def get_port(self):
        return str(self.s.getsockname()[1])

    def stop(self):
        URL_delete = BROKER_HOST + '/api/services/del/' + str(public_ip.get_lan_ip()) + "/" + str(self.s.getsockname()[1]) + '/'
        r = requests.delete(URL_delete)
        self.toRun = False
        os._exit(0)



class receiver (threading.Thread):
    def __init__(self, BUFFER_SIZE):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 0))
        self.s.listen(1)
        self.toRun = True

    def run(self):
        print "Listening on port", self.s.getsockname()[1]
        print "Waiting for connection..."
        self.conn, self.addr = self.s.accept()
        print "Running"
        while self.toRun:
            data = self.conn.recv(BUFFER_SIZE)
            if not data:
                break
            if data == 'bye':
                break
            else:
                print "> ", data
        self.stop()

    def get_port(self):
        return str(self.s.getsockname()[1])

    def stop(self):
        URL_delete = BROKER_HOST + '/api/services/del/' + str(public_ip.get_lan_ip()) + '/' + str(self.s.getsockname()[1]) + '/'
        r = requests.delete(URL_delete)
        self.toRun = False
        os._exit(0)


def register_service(nickname, ip, port):
    data = {
        "nickname": nickname,
        "ip": str(ip),
        "name": "chat_app_" + str(port),
        "description": "Chat end-to-end app using sockets without encryption",
        "port": str(port)
    }

    try:
        r = requests.post(BROKER_HOST + '/api/services/', data=data)
    except:
        print "Error while registering service"
        sys.exit(1)


def delete_service(ip, port):
    URL_delete = BROKER_HOST + '/api/services/del/' + str(ip) + '/' + str(port) + '/'
    r = requests.delete(URL_delete)

def get_service(ip, port):
    URL_get = BROKER_HOST + '/api/services/' #TODO: Link of get
    r = requests.get(URL_get)
    json=r.json()
    return json["ip"], json["port"]


try:
    BUFFER_SIZE = 20
    thread_receiver = receiver(BUFFER_SIZE)
    thread_receiver.start()
    sleep(0.1)   

    nickname=raw_input("Insert your nickname: ")
    register_service(nickname, public_ip.get_lan_ip(), thread_receiver.get_port())

    nickname=raw_input("Insert nickname to chat with: ")
    (ip, port)=get_service(nickname)
    #ip = raw_input("Connect to\nIP: ")
    #port = int(raw_input("Port: "))
    thread_sender = sender(nickname)
    thread_sender.start()
    SshClient.tunnel(thread_receiver.get_port(), port)
    
    while True: sleep(100)
except KeyboardInterrupt:
    print "\nStoping"
    delete_service(public_ip.get_lan_ip(), thread_receiver.get_port())
    thread_receiver.stop()
    thread_sender.stop()
    os._exit(0)
