# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 09:17:57 2016

@author: nausheenfatma
"""
import sys
import logging
from XMLCustomParser import WikiXmlHandler
import xml.sax
import time
#from datetime import datetime
import ast
from nltk import PorterStemmer
import argparse
#from MergeIndices import batch_sort
from MergeIndices import MergeIndices

sno = PorterStemmer()

punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
remove_punctuation_map = dict((ord(char), 32) for char in punctuation)
number='0123456789'
remove_number_map = dict((ord(char), None) for char in number)
doc_page=open("doc_title_page.txt","w")


class Document():
    def __init__(self):
        self.doc_id={}
        self.title={}
        self.body={}
        self.infobox={}
        self.categories={}
        self.external_links={}
        self.references={}

class Driver:
    
    def __init__(self):
        self.title=""
        self.text=""
        self.comment=""
        self.ref=""   
        self.STOPLIST=self.loadstoplist("code/stopwords.txt") 
        self.wikihandler=None
        self.finalindexpath="temp_index"
        self.DUMP=None
        self.INDEXFILE=None
        self.total_doc_length=0
        #self.total_of_body_tokens=0
        
    def loadstoplist(self,filename):
        stoplist={}
        f=open(filename,"r")
        for line in f:
            line=line.rstrip()
            stoplist[line]=""
        return stoplist
        
    def XMLParse(self):
          #sourceFileName="wiki-search-small.xml"
          sourceFileName="code/xml2"
          #source = open(sourceFileName)
          source = self.DUMP
          self.wikihandler=WikiXmlHandler()
          self.wikihandler.f=open(self.wikihandler.pages_file,"w")
          xml.sax.parse(source,self.wikihandler )              #XmlParsing       
          self.wikihandler.f.close()
          
    #def add_to_dict(self,tokens,dict_name):
    def add_to_dict(self,tokens,dict_name):
        for token in tokens:
                    try :         
                        dict_name[token]=dict_name[token]+1
                    except :
                        dict_name[token]=1    

        
    def remove_comments(self,line):
         #print "remove_comments timer start : "
        # start_time=time.time()
         candidate_string=line
         if (line.find("<;!--") !=-1):
             start=line.find("<;!--")+5
             if (line.find("-->") !=-1):
                 end=line.find("-->",start)
                 comment_string=line[start:end]
                 candidate_string=line.replace(comment_string,"")
         #end_time=time.time()
         #exec_time=end_time-start_time    
         #print "remove comments : ",exec_time
         return candidate_string
         
    def remove_refwithintext(self,line):
         #start_time=time.time()
         #print "remove_refwithintext timer start : "
         candidate_string=line
         if (line.find("<ref>") !=-1):
             start=line.find("<ref>")
             if (line.find("-->") !=-1):
                 end=line.find("-->",start)+3
                 comment_string=line[start:end]
                 candidate_string=line.replace(comment_string,"")
         #end_time=time.time()
         #exec_time=end_time-start_time    
         #print "remove_refwithintext: ",exec_time                 
         return candidate_string
         
    def makeindexfordocument(self,doc,pageid):
        #begin=time.time()
        indexfile=open("temp_folder/"+str(pageid),"w")
        index={}
        for key in doc.title:
            try:
                index[key]=index[key]+"t"+str(doc.title[key])
            except :
                index[key]="t"+str(doc.title[key])
                
        for key in doc.body:
            try:
                index[key]=index[key]+"b"+str(doc.body[key])
            except :
                index[key]="b"+str(doc.body[key])
                
        for key in doc.infobox:
            try:
                index[key]=index[key]+"i"+str(doc.infobox[key])
            except :
                index[key]="i"+str(doc.infobox[key])
                
        for key in doc.categories:
            try:
                index[key]=index[key]+"c"+str(doc.categories[key])
            except :
                index[key]="c"+str(doc.categories[key])   
                
        for key in doc.external_links:
            try :
                index[key]=index[key]+"e"+str(doc.external_links[key])
            except :
                index[key]="e"+str(doc.external_links[key]) 
        for key in doc.references:
            try :
                index[key]=index[key]+"r"+str(doc.references[key])
            except :
                index[key]="r"+str(doc.references[key])     
                

        s=sorted(index.keys())
        for k in s:
           v=index[k]
           indexfile.write(k+":"+"d"+str(pageid)+"-"+v+"\n")

        indexfile.close()
        
    def tokenise(self,string1):
        
        string1=string1.translate(remove_punctuation_map)
        string1=string1.translate(remove_number_map)
        #begin=time.time()     
        return string1.split()
        
            
        
    
    def merge_indices(self):
        #print "merging index files,please wait.."
        mi=MergeIndices()
        start=time.time()    
        mi.batch_sort(75)
        mi.mergelines_after_sort(self.INDEXFILE)    
        print "merging time : ",  str(time.time()-start) 
                
    def find_tokens(self,string_text):
        #begin=time.time()
        final_token_list=[]
        body_tokens=self.tokenise(string_text)

        for token in body_tokens:
             if(len(token)>0):
                try:
                    a=self.STOPLIST[token]+""
                except:
                    #token=stem(token)
                    token=sno.stem(token)
                    final_token_list.append(token)
      #  print "tok--",time.time()-begin
      #  body_tokens
        return final_token_list
        
    #old    
    def selectwordsToIndex(self,lines,doc,pageid):
      #begin=time.time()
      i=-1
      len_lines=len(lines)
      no_of_body_tokens=0
      if(len_lines==1):
          #print "1 line ignore "
          return 0
      while(i<len_lines-1):
            i=i+1
            #print i
            line=lines[i]
    
            if line.startswith("\{\{infobox") :   #INFOBOX
                while True :
                    if ((i+1)>=len_lines or lines[i+1].endswith("\}\}")):# re.match("}}",lines[i+1])):
                        break
                    i=i+1
                    line=lines[i]
                    self.add_to_dict(self.find_tokens(line),doc.infobox)
            
            elif line.startswith("\[\[category:") : #CATEGORIES
                  line=line[9:]
                  self.add_to_dict(self.find_tokens(line),doc.categories)
    
            elif line.startswith("=") : #regex to match string like ======XXX=======
                  title_text=line.replace("=","") #removing equal signs from both sides
                  title_text=title_text.strip()
    
                  if title_text=="references":
                      while True :
                          if (i+1)>=len_lines or lines[i+1].startswith("=") : #skip till next title re.match("(=)+([\w\s])+(=)+",lines[i+1]
                              break
                          i=i+1
                          line=lines[i]
                          if line.startswith("<ref"):
    
                                  self.add_to_dict(self.find_tokens(line),doc.references)
                      continue   
                  
                  
                  elif title_text=="see also": #skip inside of this section
                      while True :
                          if (i+1)>=len_lines or lines[i+1].startswith("=") :# re.match("(=)+([\w\s])+(=)+",lines[i+1]): #skip till next title 
                              break
                          i=i+1
                      continue
                  
                  elif title_text=="further reading": #skip skip this section
                      #start_time=time.time()
                      while True :
                          if (i+1)>=len_lines or lines[i+1].startswith("=") :#or re.match("(=)+([\w\s])+(=)+",lines[i+1]): #skip till next title 
                              break
                          i=i+1
                      continue                 
                  
                  elif (title_text=="external links"): #EXTERNAL LINKS
                      while True:
                          if( i+1>=len_lines or (lines[i+1].startswith("\[\[category"))):
                              break
                          i=i+1
                          line=lines[i]
                          
                          if(line.startswith('*')): #saving only bullet points
                              self.add_to_dict(self.find_tokens(line),doc.external_links)
                      continue
                  else :# (title_text=="external links"): #EXTERNAL LINKS
                      self.add_to_dict(self.find_tokens(title_text),doc.title)
                      #pass
    
        
            else :
                tokens_in_line=self.find_tokens(line)
                no_of_body_tokens=no_of_body_tokens+len(tokens_in_line)
                self.add_to_dict(tokens_in_line,doc.body)
                #self.total_doc_length=+len(tokens_in_line)

      self.total_doc_length=self.total_doc_length+no_of_body_tokens  
      return no_of_body_tokens


    
def main():
  parser = argparse.ArgumentParser(prog="indexing driver", 
                                    description="a mini search engine",
                                    formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('--i', metavar='input', dest="INFILE", type=argparse.FileType('r'), default=sys.stdin, help="<input-file>")
  parser.add_argument('--o', metavar='input', dest="OUTFILE", type=argparse.FileType('w'), default=sys.stdin, help="<input-file>")
  args = parser.parse_args()
  #print args.INFILE
  d=Driver()
  d.DUMP=args.INFILE
  d.INDEXFILE=args.OUTFILE
  start_time=time.time()
  d.XMLParse()
  end_time=time.time()
  parse_time=end_time-start_time
  print "xml parsing time : ",parse_time
  
  i=1

  begin=time.time()    
  m=open(d.wikihandler.pages_file,"r")
  for line in m:
      if(i%100==0):
          print str(i)+" files indexed"
          #print str(datetime.now())  
      

      mylist=ast.literal_eval(line)
#      for k in mylist[]:#basically only 1 element in list
#          doc=Document()
#          if d.selectwordsToIndex(mylist[k],doc,k)  :
#              d.makeindexfordocument(doc,k)
              
      doc=Document()
      page_id=mylist["id"]
      page_title=mylist["title"]
      l=d.selectwordsToIndex(mylist["text"],doc,page_id) #the fucntion finds the words to index and give doc length
      if l > 0:
          #print i
          #print "index for,",page_id
          d.makeindexfordocument(doc,page_id)
        # doc_page.write("{'id':"+str(page_id)+"','doc_length':"+str(l)+",'title':"+str(page_title)+"}\n")
          doc_page.write('{"id":'+str(page_id)+',"doc_length":'+str(l)+',"title":'+str(page_title)+'}\n')

      l=0        
      i=i+1      
  print "files indexing time :", time.time()-begin   
  print "total number of documents M:" ,i-1
  print "average document length :",d.total_doc_length/float(i-1)
  d.merge_indices()
    
if __name__ == "__main__":
    #print str(datetime.now())
    reload(sys)
    sys.setdefaultencoding('utf-8')
    logging.basicConfig()
    start_time=time.time()
    main()
    end_time=time.time()
    exec_time=end_time-start_time
    print "\nIndexing COMPLETE !!\n\nTotal execution time (in seconds): ",exec_time