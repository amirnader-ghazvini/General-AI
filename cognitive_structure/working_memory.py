from stat_parser import Parser
import csv
import json
import speech_recognition as sr
import os,sys
import time
import urllib
#from nltk.tag import StanfordNERTagger
from practnlptools.tools import Annotator
from nltk.corpus import wordnet as wn
from operator import itemgetter
import wikipedia
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet as wn
#///////         Building annotator
annotator=Annotator()

class rule:
    def __init__(self,iput,oput):
        self.input=iput
        self.output=oput
    def check(self,iput2):
        for i in iput2:
            print i




#//////         Classes
class Working_memory:
    def __init__(self, Date):
        self.wm = {'S-A':[],'OBJ':{'N/AID':[]},'Start':Date,'End':''}
        self.s = 0
        self.agent='GAI-000'
#///////NL Data Input
    def nl_article_input(self,y,source,autor,audience):
        sents = nltk.sent_tokenize(y.lower())
        i=[]
        for sent in sents:
            try:
                A = annotator.getAnnotations(sent, dep_parse=True)
            except:
                continue
            #################################   Group entities Recognition
            h = ''
            v = ''

            i.append({'sentence':sent,'structure':'','phrases':[],'source':source,'autor':autor,'audience':audience})
            for j in range(len(A['chunk'])):
                    #   Noun Phrase
                    if A['chunk'][j][1].split('-')[0] == 'S':
                        i[-1]['phrases'].append({'structure':A['pos'][j][1],'words':[A['chunk'][j][0]],'type':A['chunk'][j][1].split('-')[1],'class':A['ner'][j][1]})
                        if i[-1]['structure']=='':
                            i[-1]['structure']=A['chunk'][j][1].split('-')[1]
                        else:
                            i[-1]['structure']+= '+'+ A['chunk'][j][1].split('-')[1]
                        h = ''
                    elif A['chunk'][j][1].split('-')[0] == 'B':
                        if i[-1]['structure']=='':
                            i[-1]['structure']=A['chunk'][j][1].split('-')[1]
                        else:
                            i[-1]['structure']+= '+'+ A['chunk'][j][1].split('-')[1]

                        i[-1]['phrases'].append({'structure':A['pos'][j][1] + '+' , 'words': [A['chunk'][j][0]],'type':A['chunk'][j][1].split('-')[1],'class':A['ner'][j][1]})
                    elif A['chunk'][j][1].split('-')[0] == 'I':
                        i[-1]['phrases'][-1]['structure']+=A['pos'][j][1] + '+'
                        i[-1]['phrases'][-1]['words'].append(A['chunk'][j][0])
                        if A['ner'][j][1]!='O':
                            i[-1]['phrases'][-1]['class']=A['ner'][j][1]
                    elif A['chunk'][j][1].split('-')[0] == 'E':
                        i[-1]['phrases'][-1]['structure'] += A['pos'][j][1]
                        i[-1]['phrases'][-1]['words'].append(A['chunk'][j][0])
                        if A['ner'][j][1]!='O':
                            i[-1]['phrases'][-1]['class']=A['ner'][j][1]
            #for j in i[-1]['phrases']:


        self.add_s_a(i)
        #self.wm['S-A'].append(i)




                    #///////Add New State
    def input_to_wm(self,numberOfSent):
        obj=self.wm['S-A'][-1]['Object']
        for i in self.wm['S-A'][-1]['Input'][numberOfSent]['phrases']:

            if i['structure']=='PRP':
                a='?'
                if i['words'][0]=='i':
                    a=self.wm['S-A'][-1]['Input'][numberOfSent]['autor']
                elif i['words'][0]=='you':
                    if self.wm['S-A'][-1]['Input'][numberOfSent]['audience'] in ['reader','readers','listeners','listener']:
                        a = self.agent
                    else:
                        a = self.wm['S-A'][-1]['Input'][numberOfSent]['audience']
                self.add_object(i['words'][0],a)
            elif i['type']=='NP':
                words = i['words'][0]
                for word in i['words'][1:]:
                    words += ' ' + word
                s=True
                for j in self.wm['S-A'][-1]['Object']:
                    if words in j:
                        s=False
                        break
                if s:
                    self.add_object('N/AID', words)






    def add_s_a(self, y):
        self.wm['S-A'].append({'Object': {'N/AID':[]}, 'N_WME': [], 'G_WME': [], 'Input':y, 'Actions':{}})
        b = len(self.wm['S-A'])
        if b > 1:
            self.wm['S-A'][b - 1]['Object']=self.wm['S-A'][b - 2]['Object']
            self.wm['S-A'][b - 1]['N_WME']=(self.wm['S-A'][b - 2]['N_WME'])
        self.s=len(self.wm['S-A'])

#///////Save_and_load
    def save_wm(self,Date,x):
        self.wm['End']=Date
        with open('state_wm_0%s.json'%(x), 'w') as outfile:#state_wm_000
            json.dump(self.wm, outfile)
    def load_wm(self,x):
        with open('state_wm_0%s.json'%(x)) as infile:
            self.wm=json.load(infile)

    ##////////Add object to a State
    def add_object(self, id,object):
        if id in self.wm['S-A'][-1]['Object'].keys():
            if object not in self.wm['S-A'][-1]['Object'][id]:
                self.wm['S-A'][-1]['Object'][id].append(object)
        else:
            self.wm['S-A'][-1]['Object'][id]=[object]

#///////Add WME to a State
    def add_wme(self,ob1,op,ob2,probability):
        #Check ob1 and ob2 in state
        self.add_object(ob1)
        self.add_object(ob2)
        self.add_object(op)
        self.wm['OBJ'][ob1]['WME'] += 1
        self.wm['OBJ'][ob2]['WME'] += 1
        self.wm['OBJ'][op]['WME'] += 1
        self.wm['S-A'][self.s - 1]['WME'].append({'id':ob1,'at':op,'va':ob2,'P':probability})
    def get_what_action(self):
        return self.wm['S-A'][self.s-1]['Actions'][self.wm['S-A'][self.s-1]['Action']]['what']



WM=Working_memory('8/11/2017')
text="My name is Ben and I come from Australia. I am 24 years old and I live in a small town near Sydney called Branton. I don't have a job now, but normally I clean shop windows. I am not married but I live with my very beautiful girlfriend, Maria, in a nice house in Branton. We don't have any children...maybe next year. My girlfriend is an actress, but she isn't very famous. She acts in a small theatre in our town. At the weekend, we like to go swimming in a big lake near our house. I normally get up at eight o'clock, but on Thursday I get up at six o'clock because that is the day when I go running in the park."
WM.nl_article_input(text,'web','ben','reader')
for i in range(8):
    WM.input_to_wm(i)

print WM.wm['S-A'][0]['Object']