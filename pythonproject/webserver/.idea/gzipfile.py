import gzip,StringIO
def compressbuf(buf,level):
    s=StringIO.StringIO()
    zfile=gzip.GzipFile(mode='wb',compresslevel=level,fileobj=s)
    zfile.write(buf)
    zfile.close()
    return s.getvalue()

