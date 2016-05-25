#!/usr/bin/env python

import argparse
import socket
import sys


parser = argparse.ArgumentParser()

parser.add_argument('host', metavar='HOST', type=str,
                    help='Hostname to knock at')
parser.add_argument('ports', metavar='PORT', type=int, nargs='+',
                    help='Port(s) to use, in order specified')
parser.add_argument('-t', '--timeout', type=int,
                    help='Timeout for connection attempt (seconds), default 10')
parser.add_argument('-v', '--verbose', action="store_true",
                    help='Show detailed information')

parser.set_defaults(timeout=10)

args = parser.parse_args()


TCP_IP = args.host
TIMEOUT = args.timeout
VERBOSE = args.verbose

ports_failed = []

for TCP_PORT in args.ports:

    if VERBOSE:
        sys.stdout.write("Knocking on port ")
        sys.stdout.write('{0: <10}'.format(str(TCP_PORT) + '...'))
        sys.stdout.flush()

    sock_msg, sock_ok = None, True

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        s.connect((TCP_IP, TCP_PORT))
        sock_msg = "open"
        s.close()

    # timeouts are knocks, too
    except socket.timeout, e:
        sock_msg = "no answer"

    except socket.error, e:
        ports_failed.append(TCP_PORT)
        sock_msg = "%s" % e
        sock_ok = False

    if VERBOSE:
        if sock_ok:
            sys.stdout.write("OK")
        else:
            sys.stdout.write("FAILED")
        if sock_msg:
            sys.stdout.write(" (%s)" % sock_msg)
        sys.stdout.write("\n")
        sys.stdout.flush()


if len(ports_failed):
    s_ports = ", ".join([str(p) for p in ports_failed])
    print "\nFailed ports: %s" % s_ports
    sys.exit(1)
else:
    sys.exit(0)