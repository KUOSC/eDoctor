#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import socket,sys
import subprocess
import threading
import time
import re
import math

##Program that implements Bayes Rule for medical expert system
#Simple Naive Bayes implementation for medical expert engine
class BuildBayesModel():
    #Variable defination for bayes model
    def __init__(self,llist):
        self.totalData=0
        self.cat1Data=0
        self.cat2Data=0
        self.data={}
        self.wordsCat={}
        self.llist=llist
        self.totalCntCat={}
        self.wordCnt={}
        self.dicto={}
    #Determine the number of category
    def countCat(self,cat):
        return len(self.data[cat])
    #Determine the total number of words
    def countTotWords(self):
        for cat in self.data.keys():
            count=0
            for lline in self.data[cat]:
                count=count+len(lline)
            self.totalCntCat[cat]=count
        return self.totalCntCat
    #Count words in each category
    def countWord(self,word):
        for cat in self.data.keys():
            count=0
            for lline in self.data[cat]:
                if word in lline:
                    for lwords in lline:
                        self.dicto[lwords]=''
                        if word in lwords:
                            count=count+1
                else:
                    for lwords in lline:
                        self.dicto[lwords]=''
            self.wordCnt[cat]=count
        return self.wordCnt
    #Find the inverse category
    def invCat(self,cat):
        k=self.data.keys()
        if cat in k[0]:
            tac=k[1]
        else:
            tac=k[0]
        return tac
    #Find the prior probability of given category using Lapaceian smoothing
    def priporProbLS(self,cat1):
        tot=0
        k=1
        for cat in self.data.keys():
            tot=tot+self.countCat(cat)
        return (self.countCat(cat1)+k)/float(tot+k*len(self.data.keys()))
    #Find the prior probability of given category
    def priporProb(self,cat1):
        tot=0
        for cat in self.data.keys():
            tot=tot+self.countCat(cat)
        #print tot
        return self.countCat(cat1)/(float(tot))
    #Find the conditional probability of given category
    def mlProb(self,word,cat):
        wordcnt1=self.countWord(word)
        #print wordcnt1
        return wordcnt1[cat]/(float(self.totalCntCat[cat]))
    #Find the conditional probability of given category using lapaceian smoothing
    def lsProb(self,word,cat):
        k=1
        wordcntl=self.countWord(word)
        return (wordcntl[cat]+k)/float(self.totalCntCat[cat]+k*len(self.dicto.keys()))
    #Calculating probability using bayes rule
    def brule(self,cat,words):
        tpobnue=1.0
        tpobden=1.0
        for word in words:
            #print word
            tpobnue=tpobnue*self.lsProb(word,cat)
            tpobden=tpobden*self.lsProb(word,self.invCat(cat))
        calcnume=tpobnue*self.priporProbLS(cat)
        calcdeno=tpobden*self.priporProbLS(self.invCat(cat))
        #print calcdeno
        return calcnume/(calcnume+calcdeno)
    #Extract data given for training
    def extractInfo(self):
        for a in self.llist:
            elist=[]
            text,cat=a.split(':')
            text=text.split()
            if cat in self.data.keys():
                self.data[cat].append(text)
            else:
                self.data[cat]=elist
                self.data[cat].append(text)
        #print self.data
        
#Build list of messages for training

llist=["yellow discoloration of white part of eyes:Jaundice","yellow discoloration of white part of skin:Jaundice",
       "feeling weak:Jaundice","low fever:Jaundice","yellow pigments:Jaundice","yellowish color:Jaundice",
       "high amount of bilirubin:Jaundice","high amount of bilirubin:Jaundice","headache:Typhoid","cough:Typhoid",
       "running nose:Typhoid","abdominal pain:Typhoid","High fever:Typhoid","rose spots appear:Typhoid","headache:CC","loose nose:CC",
       "Frequent loose, watery stools:Diarrhea","Abdominal cramps:Diarrhea","Abdominal pain:Diarrhea","Fever:Diarrhea",
       "Bleeding:Diarrhea","dizziness from dehydration:Diarrhea","Loss of appetite:Diarrhea","chills fever:Viral fever",
       "Headache:Viral fever","Abdominal Pain:Viral fever","Vomiting:Viral fever","Body pain:Viral fever",
       "Throat pain:Viral fever","Loss of appetite:Viral fever","Cough:Viral fever","Shortness of breathing:Viral fever","Running Nose:Viral fever",
       "Abdominal pain in epigastric region:Gastritis","burning abdominal pain:Gastritis","Radiating abdominal pain:Gastritis","pricking abdominal pain:Gastritis",
       "Puking sensation:Gastritis","Production of sour water:Gastritis" ,"Shortness of breathing:Gastritis","Bloated stomach:Gastritis",
       "Fever:Toncilitiz","Chills fever:Toncilitiz","Sweating:Toncilitiz","Joint Pain:Toncilitiz","Body Pain:Toncilitiz",
       "Smelly mouth:Toncilitiz","Loss of appetite:Toncilitiz","Shortness of breathing:Toncilitiz","Difficulty in swallowing the food:Toncilitiz",
       "Fever:Sinocitis","Headache:Sinocitis","eyeball pain:Sinocitis","running nose:Sinocitis","Nose pain:Sinocitis",
       "Thick mucoid purulent nasal discharge:Sinocitis","Vomiting:Sinocitis","Loss of appetite:Sinocitis","Vision Problem:Sinocitis",
       "Fever:UTI","Vomiting:UTI","Burning Micturation:UTI","Frequent Urination:UTI","Abdominal Pain:UTI","Pain during Urination:UTI",
       "Burning sensation during  urination:UTI","Strong-Smelling urine:UTI","Pelvic pain in Women:UTI","Rectal pain in men:UTI"
       ]
b1=BuildBayesModel(llist)
b1.extractInfo()
b1.countTotWords()
diseaselist=["Jaundice","Typhoid","Diarrhea","Viral fever","Gastritis","Toncilitiz","Sinocitis","UTI"]

# Set up the server:
HOST = "192.168.182.226" # Symbolic name meaning the local host
PORT = 4444 # Arbitrary non-privileged port

def expLoop():
    # Accept the connection once (for starter)
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    stored_data = ' '
    while True:
        # RECEIVE DATA
        data = conn.recv(1024)
        # PROCESS DATA
        tokens = data.split(' ',1)            # Split by space at most once
        print tokens
        command = tokens[0]                   # The first token is the command
        #print command
        if command=='HELO':                    # The client requests the data
            reply = '101'               # Return the stored data
            print reply
        #elif command=='FNAME':                # The client want to store data
        #    fname = tokens[1]           # Get the data as second token, save it
        #    reply = '102'                      # Acknowledge that we have stored the data
        #    print reply
        elif command=='DATA':            # Client wants to translate
            stored_data = tokens[1]     # Convert to upper case
            print stored_data
            #mes='yellow discoloration'
            mes=stored_data.split()
            #probdis={}
            maxprob=0.00
            maxprobdis=''
            #curprob=''
            for dis in diseaselist:
                curpob=b1.brule(dis,mes)
                if curpob>maxprob:
                    maxprob=curpob
                    maxprobdis=dis
                #print dis + str(b1.brule(dis,mes))
            per=round(maxprob,2)*100
            reply=maxprobdis+"|"+str(per)
            #reply="Typhoid Prob: "+ str(b1.brule("Typhoid",mes))
            #print "Jaundice Prob: "+ str(b1.brule("Jaundice",mes))
            #print "Common Cold Prob: "+ str(b1.brule("CC",mes))
            #p.wait()
            #reply = '103'               # Reply with the converted data
            print reply
        elif command=='QUIT':                 # Client is done
            conn.send('Quit')                 # Acknowledge
            break                             # Quit the loop
        else:
            reply = 'Unknown command'
            # SEND REPLY
        conn.send(reply)
    conn.close() # When we are out of the loop, we're done, close


#class ClientThread ( threading.Thread ):
#   def run ( self ):
#       expLoop()

       
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error code: ' + str(msg[0]) + 'Error message: ' + msg[1]
    sys.exit()
print 'Socket bind complete'
s.listen(1)
print 'Socket now listening'
(conn, addr) = s.accept()

# Accept the connection once (for starter)
print 'Connected with ' + addr[0] + ':' + str(addr[1])
stored_data = ' '
expLoop()
## Have the server serve “forever”:
while True:
    (conn, addr) = s.accept()
    threading.Thread(target=expLoop).start()
    #ClientThread.start()
    

