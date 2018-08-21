from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
from CGIHTTPServer import CGIHTTPRequestHandler
import urllib,datetime,gzipfile,list,re,os,copy
#import ssl

class ServerHTTP(CGIHTTPRequestHandler):
    root_path='E:\pythonproject\webserver\.idea\\'
    cgi_path=root_path+'cgi-bin\\'
    def do_GET(self):
        path=self.path
        query = urllib.splitquery(path)
        print query
        if query[0] == '/':
            file=self.root_path+'index.html'
        else:
            file=self.root_path+query[0][1:].replace('/','\\')
        package = {'Content-Type': 'text/html',\
                  'content': open(file).read()}
        #package = list.mk_package(self, file, query)
        self.send_response(200)
        for item in package:
            if item != 'content':
                self.send_header(item, package[item])
        self.end_headers()
        self.wfile.write(package['content'])

    def do_POST(self):
        path = self.path
        print path
        datas = self.rfile.read(int(self.headers['content-length']))
        print datas
        print urllib.unquote(datas)
        datas = urllib.unquote(datas).decode('utf-8', 'ignore')
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("test", 'this is test')
        self.end_headers()
        buf = '''<!DOCTYPE HTML>
		<html>
		     <head><title>POST page</title></head>
		     <body>post data:%s   <br />path:%s</body>
		</html>''' % (datas, self.path)
        self.wfile.write(buf)

def start_server(port):
    http_server = HTTPServer(('', int(port)), ServerHTTP)
   # http_server=ssl.securehttp(('', int(port)), ServerHTTP)
    http_server.serve_forever()

start_server(8001)
