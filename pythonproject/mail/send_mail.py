import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase

'''smtp_host="smtp.163.com"
from_addr="m18992868907@163.com"
password="Qq794277368"
to_addr="chengwangyongjian@xunlei.com"
'''
smtp_host="mail1.xunlei.com"
from_addr=""
password=""
to_addr=""

f=open('C:\Users\\admin\Desktop\\1.png','rb')
msgimg=MIMEImage(f.read())
f.close()
msgimg.add_header('Content-ID','pic')

msgtext=MIMEText('<html><body><h1>Hello</h1>' +
    '<p><img src="cid:pic"></p>' +
    '</body></html>', 'html', 'utf-8')

msg=MIMEMultipart('related')
msg.attach(msgimg)
msg.attach(msgtext)
msg['subject']="python"
msg['From']=from_addr
msg['To']=to_addr

server=smtplib.SMTP()
server.connect(smtp_host,"25")
server.set_debuglevel(1)
server.login(from_addr,password)
server.sendmail(from_addr,to_addr,msg.as_string())
server.quit()
