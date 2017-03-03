# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 22:33:42 2016

@author: nausheenfatma
"""
from math import log
from nltk import PorterStemmer
import ast
import time



M=5311 #total no. of documents 
avdl=1715 #average document length
k=1
index_file="/media/nausheenfatma/01CFC8995ADC9230/4thsemester/ire/miniprojphase1/201407541_Nausheen_phase1/index_2"
stemmer = PorterStemmer()

class d:
    def __init__(self):
        self.Y=[]
        self.candidate_D=[]
        self.candidates_dict={}
        self.D_rank_score={}
        self.X={}
        
        
    def find_doc_frequencies(self,doc_freq_term):
            frequencies={"t":0,"i":0,"c":0,"b":0,"r":0,"e":0,"net_total":0}
            term_tokens=doc_freq_term.split("-")
            doc_term=term_tokens[0]
            frequency_terms=term_tokens[1]
            freq_field=""
            freq_str=[]
            count=0
            total=[]
            for t in frequency_terms:
                #print t
                try:
                    int(t)
                    freq_str.append(t) #freq_field=num
                except:
                    num_str="".join(freq_str)
                    try :
                        count=int(num_str)
                        total.append(count)
                    except:
                        pass
                    if (len(freq_field)>0):
                        #y[freq_field]=sum(total)
                        frequencies[freq_field]=count
                    freq_field=t
                    freq_str=[]
                    count=0 
            #for last term
            num_str="".join(freq_str)
            count=int(num_str)
            total.append(count)
            if (len(freq_field)>0):
                        frequencies[freq_field]=count       
            net_total=sum(total)
            frequencies["net_total"]=net_total        
            #print frequencies   
            
            return (doc_term,frequencies)
            
    def find_query_word(self,q_term):
        indexfile=open("/media/nausheenfatma/01CFC8995ADC9230/4thsemester/ire/miniprojphase1/201407541_Nausheen_phase1/index_file","r")
        for line in indexfile:
            line=line.rstrip()
            #print line
            tokens=line.split(":")
            word=tokens[0]
            if(q_term==word):
                return tokens[1]
                break
        

    def parse_query_terms(self,query_terms):
        
        for q in query_terms:
            print q
            
            #find entry from index here.
            #update x entry,find idf term
            #self.X[q][idf]=
        
            #index_entry="d1-b1|d2-t3b2e6|d3-t4b8r1"
            index_entry=self.find_query_word(q)
            print "index_entry=",index_entry
            
            docs_freq_terms=index_entry.split("|")
            df=len(docs_freq_terms)
            print df
            #self.X[q]={}
            print self.X
            self.X[q]["df"]=df
            
            for doc in docs_freq_terms:
                (doc_id,frequency_dict)=self.find_doc_frequencies(doc)
                #print (doc_id,frequency_dict)
                try :
                    self.candidates_dict[doc_id][q]=frequency_dict
                except:
                    
                    self.candidates_dict[doc_id]={}
                    self.candidates_dict[doc_id][q]=frequency_dict
        
        #print self.candidates_dict
        print "len self.candidates_dict ",len(self.candidates_dict)
        for doc_id in self.candidates_dict.keys():
            self.OkapiBM25rankscore(doc_id)
            #print doc_id+":"+str(self.candidates_dict[doc_id])
                    
                    
    def parse_refine_query(self,query):
        query_terms=query.split()
        print query_terms
        final_query_terms=[]
        for q in query_terms:  
            try:
                a=self.STOPLIST[q]+"" # remove this condition later,to handle cases like "to be or not to be"
            except:
                    #token=stem(token)
                token=stemmer.stem(q)
                final_query_terms.append(token)
            #remove stop words
            #stem
            
            
            #make x entry
            #initially store just the frequencies in X
            
        for q in final_query_terms:
            try :
                self.X[q]["count"]=self.X[q]["count"]+1
            except:
                #self.X={}
                self.X[q]={}
                self.X[q]["count"]=1
        #print "self.X",self.X
        for j in self.X:
            print self.X[j]
            
        self.parse_query_terms(final_query_terms)
        
    def OkapiBM25score(self,q,d,idf): # where q and d are dictionaries containing only matching words
        okapi_doc_score=0
        for w in d : #where w belongs to intersection of q and d 
            count_w_q=q[w]
            count_w_d=d[w]
            idf_w=idf[w]
            k=1
            w_score=count_w_q* ((k+1)*count_w_d/float(count_w_d+k)) * idf_w
            okapi_doc_score=okapi_doc_score+w_score
        return okapi_doc_score   
        
                
                
    
    def OkapiBM25rankscore(self,doc_id):
        
        okapi_tot_score=0
        q={}
        d={}
        idf={}
        
        for matching_query_term_i in self.candidates_dict[doc_id]:
            #print "matching_query_term_i",matching_query_term_i
            w=matching_query_term_i
            
            count_w_q=self.X[matching_query_term_i]["count"]
            
            q[w]=count_w_q             
            
#            count_x_i=self.X[matching_query_term_i]["count"]
#            idf_x_i=log(10/self.X[matching_query_term_i]["df"])#change 10 here
#            x_i=count_x_i*idf_x_i
            
            idf_w=log(M/self.X[matching_query_term_i]["df"])
            idf[w]=idf_w
            
            
            
            
            #print self.candidates_dict[doc_id][matching_query_term_i]['net_total']
            mydict=self.candidates_dict[doc_id][matching_query_term_i]
            
            #print self.candidates_dict[doc_id][matching_query_term_i]
#            print mydict['net_total']
#            count_y_i=mydict['net_total']
#            y_i=((k+1)*count_y_i)/float(k+count_y_i)

            
            count_w_d=mydict['net_total']
            d[w]=count_w_d
            

            
#            ##try document length normalization here
#            term_score_i=x_i*y_i
#            total_doc_score=total_doc_score+term_score_i
#            print "total_doc_score",total_doc_score
        print "doc_id",doc_id    
        print "okapi scores :",self.OkapiBM25score(q,d,idf)
        okapi_tot_score=self.OkapiBM25score(q,d,idf)
        self.D_rank_score[doc_id]=okapi_tot_score
        
    def findtitle(self,docid):
        f1=open("/media/nausheenfatma/01CFC8995ADC9230/4thsemester/ire/miniprojphase1/201407541_Nausheen_phase1/doc_title_page.txt","r")
        title="not found"
        docid=(docid.split("d"))[1]
        
        #print docid
        for line in f1:
            line=line.rstrip()
            mydict=ast.literal_eval(line)
            #print docid
            if str(mydict["id"])==str(docid):
                title=mydict["title"]
                break
                #return mydict['title']
        return title        
            
            
    def sortbyrank(self):
        #ranks1 = dict(map(reversed, enumerate(sorted(self.D_rank_score, key=dict1.get))))
        for key, value in sorted(self.D_rank_score.iteritems(), key=lambda (k,v): (v,k),reverse=True):
                title=self.findtitle(key)
                print "%s: %s " % (key, value)
                print title
                
   

if __name__=="__main__":
    doc=d()
    #doc.find_doc_frequencies("d1520-t1b200e180r1e5")    
    #doc.parse_query_terms("autism")   
    begin= time.time()
    doc.parse_refine_query("anarchism")
    doc.sortbyrank()
    print "total",time.time()-begin
    #print doc.X
    #doc.OkapiBM25rankscore("d25")
                
        
 

#class OkapiBM25:
#    def __init__(self):
#        self.M=None
#        self.k=10
#        self.b=0 # b lies in [0,1]
#        self.avg_dl=10 #to find
#        
    
        
        
        
    