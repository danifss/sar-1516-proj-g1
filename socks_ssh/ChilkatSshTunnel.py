import sys
import chilkat

#  Starting in v9.5.0.49, all Chilkat classes can be unlocked at once at the beginning of a program
#  by calling UnlockBundle.  It requires a Bundle unlock code.
chilkatGlob = chilkat.CkGlobal()
success = chilkatGlob.UnlockBundle("Anything for 30-day trial.")
if (success != True):
    print(chilkatGlob.lastErrorText())
    sys.exit()

#  This example requires Chilkat version 9.5.0.50 or greater.
tunnel = chilkat.CkSshTunnel()

sshHostname = "192.168.56.101"
sshPort = 22

#  Connect to an SSH server and establish the SSH tunnel:
success = tunnel.Connect(sshHostname,sshPort)
if (success != True):
    print(tunnel.lastErrorText())
    sys.exit()

#  Authenticate with the SSH server via a login/password
#  or with a public key.
#  This example demonstrates SSH password authentication.
success = tunnel.AuthenticatePw("nuno","nuno")
if (success != True):
    print(tunnel.lastErrorText())
    sys.exit()

#  Indicate that the background SSH tunnel thread will behave as a SOCKS proxy server
#  with dynamic port forwarding:
tunnel.put_DynamicPortForwarding(True)

#  We may optionally require that connecting clients authenticate with our SOCKS proxy server.
#  To do this, set an inbound username/password.  Any connecting clients would be required to
#  use SOCKS5 with the correct username/password.
#  If no inbound username/password is set, then our SOCKS proxy server will accept both
#  SOCKS4 and SOCKS5 unauthenticated connections.

tunnel.put_InboundSocksUsername("chilkat123")
tunnel.put_InboundSocksPassword("password123")

#  Start the listen/accept thread to begin accepting SOCKS proxy client connections.
#  Listen on port 1080.
success = tunnel.BeginAccepting(1080)
if (success != True):
    print(tunnel.lastErrorText())
    sys.exit()

#  Now that a background thread is running a SOCKS proxy server that forwards connections
#  through an SSH tunnel, it is possible to use any Chilkat implemented protocol that is SOCKS capable,
#  such as HTTP, POP3, SMTP, IMAP, FTP, etc.  The protocol may use SSL/TLS because the SSL/TLS
#  will be passed through the SSH tunnel to the end-destination.  Also, any number of simultaneous
#  connections may be routed through the SSH tunnel.

#  For this example, let's do a simple HTTPS request:
url = "https://www.google.pt/"

http = chilkat.CkHttp()

#  Indicate that the HTTP object is to use our portable SOCKS proxy/SSH tunnel running in our background thread.
http.put_SocksHostname("localhost")
http.put_SocksPort(1080)
http.put_SocksVersion(5)
http.put_SocksUsername("chilkat123")
http.put_SocksPassword("password123")

http.put_SendCookies(True)
http.put_SaveCookies(True)
http.put_CookieDir("memory")

#  Do the HTTPS page fetch (through the SSH tunnel)
html = http.quickGetStr(url)
if (http.get_LastMethodSuccess() != True):
    print(http.lastErrorText())
    sys.exit()

#  Stop the background listen/accept thread:
waitForThreadExit = True
success = tunnel.StopAccepting(waitForThreadExit)
if (success != True):
    print(tunnel.lastErrorText())
    sys.exit()

#  Close the SSH tunnel (would also kick any remaining connected clients).
success = tunnel.CloseTunnel(waitForThreadExit)
if (success != True):
    print(tunnel.lastErrorText())
    sys.exit()