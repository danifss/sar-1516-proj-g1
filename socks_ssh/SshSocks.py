from paramiko import SSHClient


class SshSocks(SSHClient):
    def connect(
        self,
        hostname,
        port=SSH_PORT,
        username=None,
        password=None,
        pkey=None,
        key_filename=None,
        timeout=None,
        allow_agent=True,
        look_for_keys=True,
        compress=False,
        sock=None,
        gss_auth=False,
        gss_kex=False,
        gss_deleg_creds=True,
        gss_host=None,
        banner_timeout=None
    ):
        super(SshSocks, self).connect(self,
                                      hostname,
                                      port,
                                      username,
                                      password,
                                      pkey,
                                      key_filename,
                                      timeout,
                                      allow_agent,
                                      look_for_keys,
                                      compress,
                                      sock,
                                      gss_auth,
                                      gss_kex,
                                      gss_deleg_creds,
                                      gss_host,
                                      banner_timeout
                                      )