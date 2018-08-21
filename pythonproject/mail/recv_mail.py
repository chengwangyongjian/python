import poplib

'''email='m18992868907@163.com'
password='Qq794277368'
pop3_server='pop.163.com'''''

email='794277368@qq.com'
password='twbdczskrtegbbjd'
pop3_server='pop.qq.com'

server=poplib.POP3_SSL(pop3_server,'995')
print(server.getwelcome())
server.user(email)
server.pass_(password)
print('Messages: %s. Size: %s' % server.stat())
resp, mails, octets = server.list()
print(mails)
index = len(mails)
resp, lines, octets = server.retr(index)
msg_content = '\r\n'.join(lines)
for i in range(1,index+1):
    server.dele(i)
    print 'delete mail-'+str(i)
#print msg_content
server.quit()
