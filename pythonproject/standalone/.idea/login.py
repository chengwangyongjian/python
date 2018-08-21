import urllib,urllib2,requests,re
from bs4 import BeautifulSoup

headers={
    'Connection':'Keep-Alive',
    'Accept-Language':'zh-CN',
    'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
   # 'Accept-Encoding':'gzip,deflate',
    'Host':'bbs.ladyboy.com.cn',
    'Content-Type':'application/x-www-form-urlencoded',
    'Referer':'http://bbs.ladyboy.com.cn/home.php?mod=space&do=home'
}
s=requests.session()
loginurl='http://bbs.ladyboy.com.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
afterurl='http://bbs.ladyboy.com.cn/home.php?mod=space&do=home'
data={'username':'794277368@qq.com','password':'CHENG794277368','quickforward':'yes','handlekey':'ls'}
login=s.post(loginurl,data,headers)
response=s.get(afterurl,cookies=login.cookies,headers=headers)
#print response.content.decode('gbk')
soup = BeautifulSoup(response.content,"html.parser")
#list=soup.find_all('img',{'class':'tn'})
list=soup.find_all('img',class_='tn')
r2=re.compile('\d{6}\w+.jpg')
for item in list:
    purl='http://bbs.ladyboy.com.cn/'+item.attrs['src']
    filename=r'E:\\'+r2.findall(purl)[0]
    f=open(filename,'wb')
    content=requests.get(purl).content
    f.write(content)
    f.close()
