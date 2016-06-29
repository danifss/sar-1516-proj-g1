from sshtunnel import SSHTunnelForwarder
from time import sleep

with SSHTunnelForwarder(
    ('localhost', 2222),
    ssh_username="vagrant",
    ssh_password="vagrant",
    remote_bind_address=('127.0.0.1', 3306)
) as server:

    print(server.local_bind_port)
    while True:
        # press Ctrl-C for stopping
        sleep(1)

print('FINISH!')

