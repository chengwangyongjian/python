import os,StringIO,cgi,gzipfile

def list_dir(self,path):
    list=os.listdir(path)
    f=StringIO.StringIO()
    f.write("<h2>directory listing for %s </h2>\n"%self.path)
    f.write("<hr>\n<ul>\n")
    f.write('<li><a href="%s">parent_dir</a>\n'%(os.path.dirname(self.path)))
    for name in list:
        fullname=os.path.join(path,name)
        displayname=cgi.escape(name)
        if os.path.isdir(fullname):
            displayname=name+'/'
            name=name+os.sep
        f.write('<li><a href="%s">%s</a>\n'%(name,displayname))
    f.write("</ul>\n<hr>\n")
    f.seek(0)
    return f

def mk_package(self,file,query):
    if query[0].endswith('.gz'):
        package = {'Content-Type': 'application/octet-stream', \
                   'content': open(file).read()}
    else:
        package = {'Content-Type': 'text/html', \
                   'Content-Encoding': 'gzip'}
        if query[0] is '/':
            file_content = list_dir(self,self.root_path).read()
        elif os.path.isdir(file):
            path = file
            file_content = list_dir(self,path).read()
        else:
            file_content = open(file).read()
        package['content'] = gzipfile.compressbuf(file_content, 1)
    return package