from twisted.internet import ssl
from oonib.config import config

class SSLContext(ssl.DefaultOpenSSLContextFactory):
    def __init__(self, *args, **kw):
        ssl.DefaultOpenSSLContextFactory.__init__(self,
                config.helpers.ssl.private_key,
                config.helpers.ssl.certificate)

