# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:24:44 2016

@author: nausheenfatma
"""
import glob
import heapq
import os
from itertools import imap
from operator import itemgetter

class MergeIndices():


    def extract_key(self,line):
        """Extract key and convert to a form that gives the
        expected result in a comparison
        """
        return line.split(":",1)[0] 
    
        
    def batch_sort(self,batch_size):
        
        filenames=glob.glob("temp_folder/"+"/*")
    #    print "len filenames",len(filenames)
    #    if(len(filenames)==1):
    #        exit()
        k=batch_size
        no_of_batches=len(filenames)/float(k)
      #  print "no_of_batches",no_of_batches
        i=0
        m=0
        while(len(filenames)>1):
            i=0
            while(i<len(filenames)):
                    m=m+1
                    #print i
                    #f=open("indexfiles2/index_"+str(m), 'w')
                    files=[]
                    for j in range(i,i+k):
                        if j < len(filenames):
                            files.append(open(filenames[j]))
                            
                    with open("temp_folder/index_"+str(m), 'w') as dest:
                            decorated = [
                                ((self.extract_key(line), line) for line in f)
                                for f in files]
                            merged = heapq.merge(*decorated)
                            undecorated = imap(itemgetter(-1), merged)
                            dest.writelines(undecorated)                        
                            
                            
                            
                    f.close()
                    for j in range(i,i+k):
                        if j < len(filenames):
                            os.remove(filenames[j])
                    i=i+k
                    #print "i",i
            filenames=glob.glob("temp_folder/"+"/*")
       
        
        
    def mergelines_after_sort(self,indexfilepath):
        filenames=glob.glob("temp_folder/"+"*")
        #print filenames
        #final_index_file=open(indexfilepath,"w")
        final_index_file=indexfilepath
        f=None
        if len(filenames)==1:
            f=open(filenames[0])
            
        line=f.readline()
        if line :
            line=line.rstrip()
            prev_key=line.split(":",1)[0]
            final_index_file.write(line)
        while True:
            line=f.readline()
            if not line:
                break
            line=line.rstrip()
            line_tokens=line.split(":",1)
            new_key=line_tokens[0]
            value=line_tokens[1]
            if(prev_key==new_key):
                final_index_file.write("|"+value)
            else :
                final_index_file.write("\n"+line)
            prev_key=new_key
            
#
#start=time.time()    
#batch_sort(75)
#mergelines_after_sort()    
#print "merge taken",  str(time.time()-start) 