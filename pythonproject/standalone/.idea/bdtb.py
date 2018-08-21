import urllib,urllib2,re
from bs4 import BeautifulSoup

class BDTB:
    def __init__(self,baseurl,see_lz):
        self.see_lz='?see_lz='+str(see_lz)
        self.baseurl=baseurl
        self.page1=self.get_page(1)
        self.soup=BeautifulSoup(self.page1,'html.parser')
    def get_page(self,page):
        url=self.baseurl+self.see_lz+'&pn='+str(page)
        req=urllib2 .Request(url)
        res=urllib2 .urlopen(req)
        return res
    def get_title(self):
        print self.soup.title.string
    def get_pagenum(self):
        print self.soup.select('li .red')[1].get_text()

baseurl='http://tieba.baidu.com/p/3138733512'
bdtb=BDTB(baseurl,1)
bdtb.get_title()
bdtb.get_pagenum()
