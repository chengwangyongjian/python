import OpenSSL
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer
class securehttp(HTTPServer):
    def __init__(self,server_address,HandlerClass):
        BaseServer.__init__(self,server_address,HandlerClass)
        ctx=SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file(r'E:\pythonproject\webserver\.idea\app.key')
        ctx.use_certificate_file('E:\pythonproject\webserver\.idea\server.crt')
        self.socket=SSL.Connection(ctx,socket.socket(self.address_family,self.socket_type))
        self.server_bind()
        self.server_activate()