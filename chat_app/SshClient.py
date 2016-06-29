import paramiko
import sys
import socket
import paramiko
import socks
from ForwardServer import ForwardServer, Handler
import time

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

# SSH_SERVER_HOST = '192.168.35.151'
SSH_SERVER_HOST = '10.0.0.1'
SSH_SERVER_PORT = 22
USERNAME = 'silva'
PASSWORD = 'a'
SOCKS_HOST = 'localhost'
SOCKS_PORT = 1080


def verbose(s):
    print(s)


def forward_tunnel(local_port, remote_host, remote_port, transport):
    # this is a little convoluted, but lets me configure things for the Handler
    # object.  (SocketServer doesn't give Handlers any way to access the outer
    # server normally.)
    class SubHander(Handler):
        chain_host = remote_host
        chain_port = remote_port
        ssh_transport = transport

    ForwardServer(('localhost', local_port), SubHander).serve_forever()


def tunnel(port_src, port_dst):
    # sock = socks.socksocket()
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, SOCKS_HOST, SOCKS_PORT, False)
    # sock.connect((SSH_SERVER_HOST, 22))
    paramiko.client.socket.socket = socks.socksocket
    client = paramiko.SSHClient()
    # client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    # client.connect(hostname=SSH_SERVER_HOST, port=SSH_SERVER_PORT, username=USERNAME, password=PASSWORD)

    # t = paramiko.Transport(sock)

    verbose('Connecting to ssh host %s:%d ...' % (SSH_SERVER_HOST, SSH_SERVER_PORT))
    try:
        # t.connect(None, username='nuno', password='nuno')
        client.connect(hostname=SSH_SERVER_HOST, port=SSH_SERVER_PORT, username=USERNAME, password=PASSWORD)
        transport = client.get_transport()
        forward_tunnel(port_src, SSH_SERVER_HOST, port_dst, transport)
    except Exception as e:
        print('*** Failed to connect to %s:%d: %r' % (SSH_SERVER_HOST, SSH_SERVER_PORT, e))
        sys.exit(1)

    verbose('Now forwarding port %d to %s:%d ...' % (port_src, SSH_SERVER_HOST, port_dst))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('C-c: Port forwarding stopped.')
        sys.exit(0)


if __name__ == '__main__':
    main()
