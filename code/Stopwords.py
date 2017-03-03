# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 09:07:11 2016

@author: nausheenfatma
"""

#create stoplist

import os
class Stopwords:
    def createstoplist(self):
        f1=open("stopwords.txt","w")
        stoplist=[]
        for i in os.listdir(os.getcwd()): #all files from current working directory
            if i.endswith(".txt"): 
                f=open(i,"r")
                for line in f:
                    line=line.rstrip()
                    if line not in stoplist:
                        stoplist.append(line)
        stoplist.sort()
        
        for stopword in stoplist:
            f1.write(stopword+"\n")
        f1.close()        
                    
                    
    def loadstoplist(self,filename):
        stoplist={}
        f=open(filename,"r")
        for line in f:
            line=line.rstrip()
            stoplist[line]=""
        return stoplist

