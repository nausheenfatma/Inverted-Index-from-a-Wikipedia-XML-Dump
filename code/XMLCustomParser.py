# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 18:43:53 2016

@author: nausheenfatma
"""

import xml.sax
import sys
import logging
from Page import Page
import time
import ast

class WikiXmlHandler(xml.sax.ContentHandler):
  def __init__(self):
      self.current_data=""
      self.Page=""
      self.Pages=[]
      self.page_id=[]
      self.page_id_txt=""
      self.temp_txt=[]
      self.tmp_txt2=[]
      self.all_lines=[]
      self.pages_file="documents.txt"
      self.line_tokens=[]
      self.f=None
      self.word_txt=[]
      self.word_list=[]
      self.page_title_text=""
      self.page_title=[]
      
      
  def startElement(self, tag, attrs):
    self.current_data=tag
    if(tag=="page"):
       # print "-----------New Page--------------"
        self.Page=Page()
#    if(tag=="ref"):
#        print "new ref"
 
  def endElement(self, tag):
        
      if(tag=="page"):
          if(len(self.page_id)>0):
              self.Page.id=self.page_id[0]
          page_title="".join(self.page_title)
          page_title=page_title.rstrip()
          page_title.replace("\"", "")
          mylist=[]
          mylist.append(page_title)
          #print 
          #self.f.write("{'id':"+self.Page.id+",'text':"+str(self.Page.text_lines)+",'title':'"+str(page_title)+"'}"+"\n")
          self.f.write('{"id":'+self.Page.id+',"text":'+str(self.Page.text_lines)+',"title":'+str(mylist)+'}'+'\n')
          self.page_id=[]
          self.page_title=[]
          
          
      if(tag=="id" ):
          self.page_id.append(self.page_id_txt)
          self.page_id_txt=""
          
      #if(tag=="title" ):

 
  def characters(self, content):
      if self.current_data=="title":
          self.page_title.append(content)
          #self.Page.title=self.Page.title+content
          #self.Page.title=self.Page.title+content
      
      if self.current_data=="text":
 
          self.tmp_txt2.append(content.lower()) 

              
          if(content=='\n'):
              line="".join(self.tmp_txt2)
              self.Page.text_lines.append(line)
              self.tmp_txt2=[]

          
      if self.current_data=="id" :
          self.page_id_txt=content

   
def main(sourceFileName):
  source = open(sourceFileName)
  wikihandler=WikiXmlHandler()
  wikihandler.f=open(wikihandler.pages_file,"w")
  xml.sax.parse(source,wikihandler )              #XmlParsing
  
  print "total number of pages",len(wikihandler.Pages)
  wikihandler.f.close()
  i=1
  m=open(wikihandler.pages_file,"r")
  for line in m:
      
      mylist=ast.literal_eval(line)
      for k in mylist:
          print mylist["title"]
#          for el in mylist[k]:
#              print el+"---------"
      i=i+1
 
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    logging.basicConfig()
    start_time=time.time()
    main("../dump.xml")
    end_time=time.time()
    parse_time=end_time-start_time
    print "parsing time : ",parse_time