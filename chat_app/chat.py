import socket
import threading
from time import sleep
import sys, traceback

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

    def stop(self):
        sys.exit()
        self.end = True
        self.s.close()
        sys.exit()
        

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

    def stop(self):
        sys.exit()
        self.running = False
        #socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.hostname, self.port))
        self.s.close()

TCP_IP = '127.0.0.1'
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

try:
    thread1 = receiver(BUFFER_SIZE)
    thread1.start()
    sleep(0.1)   

    ip = raw_input("Connect to\nIP: ")
    port = int(raw_input("Port: "))
    thread2 = sender(ip, port)
    thread2.start()
    
except KeyboardInterrupt:
    print "Stoping"
    thread1.stop()
    thread2.stop()
    sys.exit(0)