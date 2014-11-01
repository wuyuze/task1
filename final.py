# -*- coding: utf-8 -*-
import urllib
import re
import os
from sgmllib import SGMLParser
class Getcontent(SGMLParser):
    def __init__(self):
        self.content=[]
        self.ti = False
        self.div = False
        self.getti = False
        self.gettext = False
        self.getimage =False
        self.h1=False
        self.h2=False
        self.h3=False
        self.h4=False
        self.h5=False
        self.h6=False
        self.title=''
        self.layer = 0
        self.mark=0
        SGMLParser.reset(self)

    def start_div(self,attrs):                      #一级div标签#
        if self.div == True:
            self.layer +=1
            return
        for k,v in attrs:
            if k=='class' and v =='show-content':
                self.div = True
            if k=='class' and v =='article-info':
                self.div = True
        for k,v in attrs:
            if k=='class' and v=='image-package imagebubble' :
                self.getimage = True
                return
    def end_div(self):                              
        if self.layer == 0:
            self.div = False
            return
        if self.div == True:
            self.layer -=1
            return
    def start_p(self, attrs):                      #若<p>外存在div标签，则提取内容
        if self.div == False:
           return
        self.gettext = True
    def end_p(self):
        if self.gettext==True:
            self.gettext = False
    def start_title(self,attrs):                   #遇到title标签，则提取内容             
        self.getti = True
    def end_title(self):
        self.getti = False
    def start_h2(self,attrs):                   #遇到h2标签，则提取内容             
        self.h2 = True
    def end_h2(self):
        self.h2 = False
    def start_h3(self,attrs):                   #遇到h3标签，则提取内容             
        self.h3 = True
    def end_h3(self):
        self.h3 = False
    def start_h4(self,attrs):                   #遇到h4标签，则提取内容             
        self.h4 = True
    def end_h4(self):
        self.h4 = False
    def start_h5(self,attrs):                   #遇到h5标签，则提取内容             
        self.h5 = True
    def end_h5(self):
        self.h5 = False
    def start_h6(self,attrs):                   #遇到h6标签，则提取内容             
        self.h6 = True
    def end_h6(self):
        self.h6 = False

    def handle_data(self,text):                    #将提取到的内容加入表格
        if self.gettext == True:
            self.content.append('        '+str(text).strip('\n').replace(' ','' )+'\n')
        if self.getti == True:
            self.title=text
            self.content.append('                       '+text+'\n')
            self.content.append('================================================================================'+'\n')
        if self.h2==True:
            self.content.append(text+'\n')
            self.content.append('--------------------------------------------------------------------------------'+'\n')
        if self.h3==True:
            self.content.append('###'+text)
        if self.h4==True:
            self.content.append('####'+text)
        if self.h5==True:
            self.content.append('#####'+text)
        if self.h6==True:
            self.content.append('######'+text)

    def start_img(self,attrs):
        if self.div ==False:
            return
        alt=[v for k,v in attrs if k=='alt']
        if alt:
            self.content.append('['+str(alt)[1:-1]+']')
        src=[v for k,v in attrs if k=='src']
        if src:
            self.content.append('[id:'+str(src)[1:-1]+']'+'\n')
    def savetomarkdown(self):
        f=open(str(self.title)+'.md','w')
        for i in self.content:
            print i
            f.write(str(i))
def geturl1(url):                              #获取专题页面的文章url
    html = urllib.urlopen(url).read()
    reu=re.compile(r'a href=.*?target')
    html=re.findall(reu,html)
    for i in html:
        url1.append('http://www.jianshu.com'+str(i)[8:-8])  
def geturl2(url):                              #得到文章内部的跳转链接，更多的url
    html = urllib.urlopen(url).read()
    reu=re.compile(r'slug=.*?data-pjax')
    reurl=re.findall(reu,html)
    global j
    for i in reurl:
        url2.append('http://www.jianshu.com/p/'+str(i)[6:-11])

print 'Loading..........'            #start
url1=[]
url2=[]
url=('http://www.jianshu.com/collection/fcd7a62be697/top','http://www.jianshu.com/collection/GUwFza/top','http://www.jianshu.com/collection/723de9bac3cd')
j=0
for n in range(3):              #一重循环
    geturl1(url[n])            
    url11=list(set(url1))       #将重复的url剔除
    for m in url11:
        geturl2(str(m))
    url22= list(set(url2))        #将重复的url剔除
    os.mkdir('/home/wuyuze/python_1/theme'+str(n+1))        #创建文件夹
    os.chdir('/home/wuyuze/python_1/theme'+str(n+1))        #进入文件夹 
    for m in range(100):
        print url22[m]
        content=Getcontent()
        content.mark=m+1
        htmlcontent=urllib.urlopen(str(url22[m])).read()
        content.feed(htmlcontent)
        content.savetomarkdown()
print "All work is finished!"           
