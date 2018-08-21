import requests,insert,re
from bs4 import BeautifulSoup

def send_req(url):
    return requests.get(url)

def get_answ(url):
   html=send_req(url)
   soup=BeautifulSoup(html.content,'html.parser',from_encoding='UTF-8')
   for i in soup.select('span > pre'):
        return i.string

response=send_req('http://iask.sina.com.cn/c/74.html')
#print response.encoding
soup=BeautifulSoup(response.content,'html.parser',from_encoding='UTF-8')
#print soup.original_encoding
for item in soup.find_all('a',href=re.compile('/b/.*\.html'),title=True):
    d={'title':item.string,'addr':'http://iask.sina.com.cn'+item.attrs['href']}
    answer=get_answ(d['addr'])
    if answer:
        d['answer']=answer
    else:d['answer']='none'
  #  print d
    m=insert.mysql()
    m.insert_data('question',d)


