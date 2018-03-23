from stat_parser import Parser
import csv
import json
import speech_recognition as sr
import os,sys
import time
import urllib
from nltk.tag import StanfordNERTagger
from practnlptools.tools import Annotator
from nltk.corpus import wordnet as wn
from operator import itemgetter
import wikipedia
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet as wn
#///////         Building annotator
annotator=Annotator()

#///////        List of tags
tag_list=[
    'S',      # simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a wh-word and that does not exhibit subject-verb inversion.
    'SBAR',   # Clause introduced by a (possibly empty) subordinating conjunction.
    'SBARQ',  # Direct question introduced by a wh-word or a wh-phrase. Indirect questions and relative clauses should be bracketed as SBAR, not SBARQ.
    'SINV',   # Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal.
    'SQ',     # Inverted yes/no question, or main clause of a wh-question, following the wh-phrase in SBARQ.

    'ADJP',   # Adjective Phrase.
    'ADVP',   # Adverb Phrase.
    'CONJP',  # Conjunction Phrase.
    'FRAG',   # Fragment.
    'INTJ',   # Interjection. Corresponds approximately to the part-of-speech tag UH.
    'LST',    # List marker. Includes surrounding punctuation.
    'NAC',    # Not a Constituent; used to show the scope of certain prenominal modifiers within an NP.
    'NP',     # Noun Phrase.
    'NX',     # Used within certain complex NPs to mark the head of the NP. Corresponds very roughly to N-bar level but used quite differently.
    'PP',     # Prepositional Phrase.
    'PRN',    # Parenthetical.
    'PRT',    # Particle. Category for words that should be tagged RP.
    'QP',     # Quantifier Phrase (i.e. complex measure/amount phrase); used within NP.
    'RRC',    # Reduced Relative Clause.
    'UCP',    # Unlike Coordinated Phrase.
    'VP',     # Vereb Phrase.
    'WHADJP', # Wh-adjective Phrase. Adjectival phrase containing a wh-adverb, as in how hot.
    'WHADVP',  # Wh-adverb Phrase. Introduces a clause with an NP gap. May be null (containing the 0 complementizer) or lexical, containing a wh-adverb such as how or why.
    'WHNP',   # Wh-noun Phrase. Introduces a clause with an NP gap. May be null (containing the 0 complementizer) or lexical, containing some wh-word, e.g. who, which book, whose daughter, none of which, or how many leopards.
    'WHPP',   # Wh-prepositional Phrase. Prepositional phrase containing a wh-noun phrase (such as of which or by whose authority) that either introduces a PP gap or is contained by a WHNP

    'CC',     # Coordinating conjunction
    'CD',     # Cardinal number
    'DT',     # Determiner
    'EX',     # Existential there
    'FW',     # Foreign word
    'IN',     # Preposition or subordinating conjunction
    'JJ',     # Adjective
    'JJR',    # Adjective, comparative
    'JJS',    # Adjective, superlative
    'LS',     # List item marker
    'MD',     # Modal
    'NN',     # Noun, singular or mass
    'NNS',    # Noun, plural
    'NNP',    # Proper noun, singular
    'NNPS',   # Proper noun, plural
    'PDT',    # Predeterminer
    'POS',    # Possessive ending
    'PRP',    # Personal pronoun
    'PRP$',   # Possessive pronoun (prolog version PRP-S)
    'RB',     # Adverb
    'RBR',    # Adverb, comparative
    'RBS',    # Adverb, superlative
    'RP',     # Particle
    'SYM',    # Symbol
    'TO',     # to
    'UH',     # Interjection
    'VB',     # Verb, base form
    'VBD',    # Verb, past tense
    'VBG',    # Verb, gerund or present participle
    'VBN',    # Verb, past participle
    'VBP',    # Verb, non-3rd person singular present
    'VBZ',    # Verb, 3rd person singular present
    'WDT',    # Wh-determiner
    'WP',     # Wh-pronoun
    'WP$',    # Possessive wh-pronoun (prolog version WP-S)
    'WRB',    # Wh-adverb

    '.',      # Sentence final puntuation
    ',',      # Comma
    ':',      # Mid sentence punctuation
    '-LRB-',  # Left parenthesis
    '-RRB-',  # Right parenthesis
    '``',     # Start quote
    "''",     # End quote
    '#',      # Pound sign
    '$',      # Dollar sign

    # These will be filtered in the following steps
    '',       # Empty
    '-NONE-', #
    'X'       # Uncertain
]
poiner_words=['any','some','a','an','the','this','that','these','those','my','your','his','her','its','our',
              'ur','their','what','where','when','who','which','hows','how']

no_verb=['please','never','ever','still','yet','now','also','thus','already','sometimes','not',"'t",'must',
         'should',"'d",'shoulnt','shouldn','would','will',"'ll","wouldnt","wouldn't",'wouldn','may','might',
         'shall','can','cannot',"cann't",'could','couldn','has','have',"'ve",'having','had','are',"'r",'be',
         'been','is',"'s",'am',"'m",'was','were','want','wanted','being','likes','like','need','plan','going']

noun_list=[
    'NN',     # Noun, singular or mass
    'NNS',    # Noun, plural
    'NNP',    # Proper noun, singular
    'NNPS'    # Proper noun, plural
]
verb_list=[
    'VB',     # Verb, base form
    'VBD',    # Verb, past tense
    'VBG',    # Verb, gerund or present participle
    'VBN',    # Verb, past participle
    'VBP',    # Verb, non-3rd person singular present
    'VBZ'     # Verb, 3rd person singular present
]
adj_list=[
    'JJ',     # Adjective
    'JJR',    # Adjective, comparative
    'JJS'     # Adjective, superlative
]
adv_list=[
    'RB',     # Adverb
    'RBR',    # Adverb, comparative
    'RBS'     # Adverb, superlative
    ]
not_at_np=[
    'PRP$',   # Possessive pronoun (prolog version PRP-S)
    'TO',     # to
    'IN',     # Preposition or subordinating conjunction
    'CD',     # Cardinal number
    'PRP',    # Personal pronoun
    'DT',     # Determiner
    'WDT',    # Wh-determiner
    'WP',     # Wh-pronoun
    'WP$',    # Possessive wh-pronoun (prolog version WP-S)
    'WRB',    # Wh-adverb
    'JJ',     # Adjective
    'JJR',    # Adjective, comparative
    'JJS'    # Adjective, superlative

]
not_at_vp=[
    'PRP$',   # Possessive pronoun (prolog version PRP-S)
    'TO',     # to
    'IN',     # Preposition or subordinating conjunction
    'CD',     # Cardinal number
    'PRP',    # Personal pronoun
    'DT',     # Determiner
    'WDT',    # Wh-determiner
    'WP',     # Wh-pronoun
    'WP$',    # Possessive wh-pronoun (prolog version WP-S)
    'WRB',    # Wh-adverb
    #'JJ',     # Adjective
    #'JJR',    # Adjective, comparative
    #'JJS'    # Adjective, superlative

]
not_at_adjp=[
    'PRP$',   # Possessive pronoun (prolog version PRP-S)
    'TO',     # to
    'IN',     # Preposition or subordinating conjunction
    'CD',     # Cardinal number
    'PRP',    # Personal pronoun
    'DT',     # Determiner
    'WDT',    # Wh-determiner
    'WP',     # Wh-pronoun
    'WP$',    # Possessive wh-pronoun (prolog version WP-S)
    'WRB',    # Wh-adverb
    #'JJ',     # Adjective
    #'JJR',    # Adjective, comparative
    #'JJS'    # Adjective, superlative

]
not_at_advp=[
    'PRP$',   # Possessive pronoun (prolog version PRP-S)
    'TO',     # to
    'IN',     # Preposition or subordinating conjunction
    'CD',     # Cardinal number
    'PRP',    # Personal pronoun
    'DT',     # Determiner
    'WDT',    # Wh-determiner
    'WP',     # Wh-pronoun
    'WP$',    # Possessive wh-pronoun (prolog version WP-S)
    #'WRB',    # Wh-adverb
    #'JJ',     # Adjective
    #'JJR',    # Adjective, comparative
    #'JJS'    # Adjective, superlative

]


#//////         Classes
class Working_memory:
    def __init__(self, Date):
        self.wm = {'S-A':[],'OBJ':{}}
        self.start = Date
        self.end=''
        self.s = 0
#///////NL Data Input
    def nl_article_input(self,y,source,topic):
        sents = nltk.sent_tokenize(y)
        i=[]
        for sent in sents:
            try:
                A = annotator.getAnnotations(sent, dep_parse=True)
            except:
                continue
            #################################   Group entities Recognition
            h = ''
            v = ''

            i.append({'sentence':sent,'structure':'','phrases':[],'source':source,'topics':[topic]})
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


        self.wm['S-A'].append(i)




                    #///////Add New State


    def add_s_a(self, y):
        self.wm['S-A'].append({'Object': [], 'WME': [], 'Input':y})
        b = len(self.wm['S-A'])
        if b > 1:
            self.wm['S-A'][b - 1]['Object'].extend(self.wm['S-A'][b - 2]['Object'])
            self.wm['S-A'][b - 1]['WME'].extend(self.wm['S-A'][b - 2]['WME'])
        self.s=len(self.wm['S-A'])

#////////Add Object to Working memory
    def add_OBJ(self,object):
        """if object not in self.wm['OBJ'].keys():
            OBJ = {"Object": object, 'N': 1,'WME':0}
            self.wm['OBJ'][object]=OBJ
        else:
            self.wm['OBJ'][object]['N']+=1"""
    def save_wm(self,x):
        with open('state_wm_00%s.json'%x, 'w') as outfile:#state_wm_000
            json.dump(self.wm, outfile)
#////////Add object to a State
    def add_object(self, object):
        if object in self.wm['OBJ'].keys():
            self.wm['OBJ'][object]['N'] += 1
            if object not in self.wm['S-A'][self.s-1]['Object']:
                self.wm['S-A'][self.s - 1]['Object'].append(object)
        else:
            self.add_OBJ(object)
            self.add_object(object)

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


class semantic_memory:
    def __init__(self, x):
        self.LIST_of_semantic_types=['VALUE','ATTRIBUTE','CLASS','ENTITY','FUNCTION','CONDITION']
        try:
            with open('semantic_lib00%s.json'%x) as data_file:
                semantic = json.load(data_file)
        except:
            semantic=[]
        self.sm = semantic
    def get_item(self,name,type):
        out = []
        for i in self.sm:
            if (i['name']==name or name.replace('.',' ') in i['synonyms']) and i['type']==type:
                out.append(i)
        return out
    def guess_type(self,item,phrasetype):
        evidence = [phrasetype]
        if 'wordnet_name' in item.keys():
            if item['wordnet_name'] != 'n/a':
                evidence.append(item['wordnet_name'].split('.')[1])
        decison={}
        for i in self.LIST_of_semantic_types:
            decison[i]=0
        for i in evidence:
            if i in ['np','n']:
                decison['ATTRIBUTE'] += 1
                decison['CLASS'] += 1
                decison['ENTITY'] += 1
                print "DEFENITION: " + item['definition']
                print "WORDNET: " + item['wordnet_name']
                var = raw_input("What is %s type? 1:ATTRIBUTE , 2:ClASS , 3:ENTITY , 4:Other" % (item['name']))
                if var == '1':
                    return 'ATTRIBUTE'
                elif var =='2':
                    return 'CLASS'
                elif var =='3':
                    return 'ENTITY'
                elif var =='4':
                    print 'fuck you!'
                    var = raw_input("What is %s type? 1:Value ,2:class and entity ,3:others" % (item['name']))
                    if var == '1':
                        return 'VALUE'
                    elif var=='2':
                        return 'CLASS'
                    elif var == '3':
                        print 'fuck you!'


            elif i in ['adjp','a']:
                decison['VALUE'] += 1
                return 'VALUE'
            elif i in ['vp','v']:
                decison['FUNCTION'] += 1
                return 'FUNCTION'
            elif i in ['advp','s']:
                decison['CONDITION'] += 1
                return 'CONDITION'

    def put_item(self,item,phrasetype):
        if 'name' in item.keys() and 'type' not in item.keys():
            item['type']=self.guess_type(item,phrasetype)
        if ('name' in item.keys())and ('type' in item.keys()):
            name=item['name']
            typeofword=item['type']
            out = []
            for i in self.sm:
                if (i['name'] == name or name.replace('.', ' ') in i['synonyms']) and i['type'] == typeofword:
                    out.append(i)
                    if 'count' in item.keys():
                        i['count']+=item['count']
                    else:
                        i['count'] +=1
            if len(out)!=0:
                print name+" as a " + typeofword + " is already in the semantic memory"

            else:
                with open('entity_lib09.json') as data_file:
                    semantic = json.load(data_file)
                if typeofword== "ATTRIBUTE" or typeofword== "CLASS" or typeofword== "ENTITY":
                    check=['np']
                elif typeofword== "VALUE":
                    check = ['adjp']
                elif typeofword== "FUNCTION":
                    check = ['vp']
                elif typeofword == "CONDITION":
                    check = ['advp']
                for c in check:
                    for j in semantic[c]:
                        if (j['name'] == name or name.replace('.', ' ') in j['synonyms']):
                            if j['definition']!='':
                                print "DEFENITION: "+j['definition']
                                print "WORDNET: " + j['wordnet_name']
                                if j['wordnet_name'].split('.')[1] in ['a','s'] and typeofword=='VALUE':
                                    var='y'
                                else:
                                    var = raw_input("Is this a good definition for %s as %s? (Y / N) " % (name, typeofword))
                                if var=='y':
                                    x=j
                                    x['type']=typeofword
                                    for kk in item.keys():
                                        if kk not in x.keys():
                                            x[kk]=item[kk]



                                        if kk in ["classes","sub_classes"]:
                                            for xx in item[kk]:
                                                self.put_item({'name':xx[0].lower(),'type':"CLASS"})
                                            if kk in x.keys():
                                                for xx in x[kk]:
                                                    self.put_item({'name': xx[0].lower(), 'type': "CLASS"})
                                        elif kk in ["attributes","sub_attributes"]:
                                            for xx in item[kk]:
                                                self.put_item({'name':xx[0].lower(),'type':"ATTRIBUTE"})
                                            if kk in x.keys():
                                                for xx in x[kk]:
                                                    self.put_item({'name': xx[0].lower(), 'type': "ATTRIBUTE"})
                                        elif kk in ["values","sub_values"]:
                                            for xx in item[kk]:
                                                self.put_item({'name':xx[0].lower(),'type':"VALUE"})
                                            if kk in x.keys():
                                                for xx in x[kk]:
                                                    self.put_item({'name': xx[0].lower(), 'type': "VALUE"})
                                        elif kk in ["entities", "sub_entities"]:
                                            for xx in item[kk]:
                                                self.put_item({'name': xx[0].lower(), 'type': "ENTITY"})
                                            if kk in x.keys():
                                                for xx in x[kk]:
                                                    self.put_item({'name': xx[0].lower(), 'type': "ENTITY"})



                                    self.sm.append(x)
                                    for kk in item.keys():
                                        if kk in x.keys() and type(x[kk])==list:
                                            self.update_detail_sm(name,typeofword,kk,item[kk])
                                    break
    def save_sm(self, x):
        with open('semantic_lib00%s.json'%x, 'w') as outfile:#000
            json.dump(self.sm, outfile)
    def update_detail_sm(self,name,type,key,x):
        out = 0
        for i in self.sm:
            if (i['name'] == name or name.replace('.', ' ') in i['synonyms']) and i['type'] == type:
                out+=1
                if key not in i.keys():
                    i[key]=x
                else:
                    for j in x:
                        o=0
                        for t in i[key]:
                            if t[0]==j[0]:
                                t[1]+=j[1]
                                o+=1
                                break
                        if o==0:
                            i[key].append(j)
                i[key] = sorted(i[key], key=itemgetter(1), reverse=True)
        if out==0:
            print "There is no item like that in memory"
    def import_words_from_entity_lib(self,x,max):
        with open('entity_lib0%s.json'%(x)) as data_file:
            entity_data = json.load(data_file)
        for pkind in entity_data.keys():
            for i in entity_data[pkind]:
                if i['count']>max :
                    if 'name' in i.keys() and 'type' not in i.keys():
                        i['type'] = self.guess_type(i, pkind)
                    if ('name' in i.keys()) and ('type' in i.keys()):
                        name = i['name']
                        typeofword = i['type']
                        out = []
                        for j in self.sm:
                            if (j['name'] == name or name.replace('.', ' ') in j['synonyms']) and j['type'] == typeofword:
                                out.append(i)
                                if 'count' in i.keys():
                                    j['count'] += i['count']
                                else:
                                    j['count'] += 1
                        if len(out) != 0:
                            print name + " as a " + typeofword + " is already in the semantic memory"
                        else:
                            for kk in i.keys():
                                if kk in ["classes", "sub_classes"]:
                                    for xx in i[kk]:
                                        self.put_item({'name': xx[0].lower(), 'type': "CLASS"},'np')
                                elif kk in ["attributes", "sub_attributes"]:
                                    for xx in i[kk]:
                                        self.put_item({'name': xx[0].lower(), 'type': "ATTRIBUTE"},'np')
                                elif kk in ["values", "sub_values"]:
                                    for xx in i[kk]:
                                        self.put_item({'name': xx[0].lower(), 'type': "VALUE"},'adjp')
                                elif kk in ["entities", "sub_entities"]:
                                    for xx in i[kk]:
                                        self.put_item({'name': xx[0].lower(), 'type': "ENTITY"},'np')
                            self.sm.append(i)
                    self.save_sm(1)

#////////// Working memory defining
W=Working_memory(time.strftime("%H:%M:%S - %d:%m:%Y"))
S=semantic_memory(0)

#///////        Functions
def sort_based(filename,key):
    with open(filename+'.json') as data_file:
        entity_data = json.load(data_file)
    for pkind in entity_data.keys():
        entity_data[pkind] = sorted(entity_data[pkind], key=itemgetter(key), reverse=True)
    with open((filename+'.json'), 'w') as outfile:
        json.dump(entity_data, outfile)

def show_stat_of_dif_pkind(filename,tag):
    with open(filename+'.json') as data_file:
        entity_data = json.load(data_file)
    c = {"total": 0, "np": 0, "vp": 0, "adjp": 0, "advp": 0}
    cc = {"total": 0, "np": 0, "vp": 0, "adjp": 0, "advp": 0}
    for j in entity_data.keys():
        for i in entity_data[j]:
            c['total'] += i['count']
            c[j] += i['count']
            if tag in i.keys() and i[tag]!='n/a':
                cc['total'] += 1
                cc[j] += 1


    for i in c.keys():
            print "|////////////////////  %s  ///////////////////////|" % (i)
            print ("|//      %s repeats :  %s - %s percent" % (i, c[i], (c[i] * 100 / c['total'])))

            if i != 'total':
                print("|//      Number of %s:  %s " % (i, len(entity_data[i])))
                print("|//      Number of having %s in %s:  %s " % (tag,i, cc[i]))
                print("|//      Percent of having %s in %s:  %s " % (tag, i, cc[i]*100 / len(entity_data[i])))
                if len(entity_data[i])!=0:
                    print ("|//      Average repeat :  %s " % ((c[i] / len(entity_data[i]))))
                    print ("|//      Mean repeat :  %s   " % ((entity_data[i][len(entity_data[i]) / 2]['count'])))
                    print ("|//      on 1/4 repeat :  %s " % ((entity_data[i][int(len(entity_data[i]) / 1.3)]['count'])))
    print "|////////////////////////////////////////////////////////|"

#//////////       Actions
def read_user(w):
    text=raw_input("Enter something: ")
    y={'source':'user','how':'type','what':text}
    w.add_s_a(y)

def listen_user(w):
    text=''
    x=0
    while text=='' and x < 5:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source, 7, 5)
        text = ''
        print ('wait...')
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = r.recognize_google(audio)
            # print("You said: " + text )
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        if text.split(' ')[0] in wh_words:
            text = text + ' ?'
        print("You said: " + text)
        #return text
        x=x+1
    if text!='':
        y = {'source': 'user', 'how': 'say', 'what': str(text)}
    else:
        y = {'source': 'user', 'how': 'say', 'what': "none"}
    w.add_s_a(y)

def write_for_user(w):
    print w.get_what_action()

def Sentiment_analysis(w):
    data = urllib.urlencode({"text": w.wm['S-A'][w.s - 1]['Input']['what']})
    u = urllib.urlopen("http://text-processing.com/api/sentiment/", data)
    u_str = u.read()
    # print u_str
    u_data = json.loads(u_str)
    #print 'Label:', u_data['label']
    #print 'Probability:', u_data['probability'][u_data['label']]
    w.add_wme('sentiment_lable','be',str(u_data['label']),u_data['probability'][u_data['label']])

def Annotate(w):
    A = annotator.getAnnotations(w.wm['S-A'][w.s - 1]['Input']['what'], dep_parse=False)
    probability=1
    print 'POS:', A['pos']
    for t in A['pos']:
        w.add_wme(t[0],'be',t[1],probability)
    print 'NER:', A['ner']
    for t in A['ner']:
        if t[1]!='O':
            w.add_wme(t[0],'be',t[1],probability)
    print 'Chunk:', A['chunk']

    print 'SRL:', A['srl']
    # for i in A['srl']:
    #   print i['V']

    print 'Syntax1:', A['syntax_tree']
    # print A['dep_parse']



#fun=   'IMPORT-From-Conversational'
#fun=   'IMPORT-From-Wordnet'
#fun=   'IMPORT-From-Wikipedia'
#fun=   'REFINE-Entities-0'
#fun=   'REFINE-Entities-1'
#fun=   'SORT-Entities-count'
#fun=   'SORT-Entities-numOfKeywords'
#fun=   'MAKE-Keywords-dict'
#fun=   'MODIFY-Keywords-dict0'
#fun=   'MODIFY-Keywords-dict1'
#fun = 'Add-Values-TO-noun'
#fun = 'Find-multi-words-in-WORDNET'
#fun = 'ADD-GRAMMAR'
#fun = 'GUESS-Type'
fun='n/a'

if fun=='IMPORT-From-Conversational':
    with open('Data_User_Input3.json') as working_file:
        conv_data = json.load(working_file)

    with open('Entity_lib00.json') as data_file:
        entity_data = json.load(data_file)

    """t={'entities':[],'verbs':[],'entity':{},'verb':{},'Adj':{},'Adv':{}}
    for i in tset:
        t['entities'].extend(i['new_entities'])
        t['verbs'].extend(i['verb_entities'])"""
    for i in conv_data:
        if ('nlp' in i.keys())and('entity_learning_status' not in i.keys())and 'Group_Entities' in i.keys():
            # Group entity (Attributes) recognition
            tags = {}
            for pkind in i['Group_Entities'].keys():
                for j in i['Group_Entities'][pkind]:
                    tags[j] = []
                    v = ''
                    k=''
                    for h in j.split('.'):
                        if len(h.split('--')) > 1 and h!='':
                            if k=='':
                                k = h.split('--')[0]
                            else:
                                k = k + ' ' + h.split('--')[0]

                            if ((h.split('--')[1] not in not_at_np)and(pkind=='np'))\
                                    or((h.split('--')[1] not in not_at_vp)and(pkind=='vp')and(h.split('--')[0].lower() not in no_verb))\
                                    or((h.split('--')[1] not in not_at_adjp)and(pkind=='adjp'))\
                                    or((h.split('--')[1] not in not_at_advp)and(pkind=='advp')):
                                if v == '':
                                    v = h.split('--')[0]
                                else:
                                    v = v + '.' + h.split('--')[0]
                    if v == '':
                        continue
                    c=0
                    for ii in entity_data[pkind]:
                        if k in ii['keywords']:
                            ii['count']+=1
                            #entity_data[pkind][ii]['keywords'].append(k)
                            c = 1
                            #break
                        elif (v.lower() == ii['name']) or (v.lower() in ii['synonyms']):
                            ii['count'] += 1
                            ii['keywords'].append(k)
                            c = 1



                    if c==0:
                        if pkind=='np':
                            x = wn.synsets(v.replace('.',' '), pos=wn.NOUN)
                        elif pkind=='vp':
                            x = wn.synsets(v.replace('.',' '), pos=wn.VERB)
                        elif pkind=='adjp':
                            x = wn.synsets(v.replace('.',' '), pos=wn.ADJ)
                        elif pkind=='advp':
                            x = wn.synsets(v.replace('.',' '), pos=wn.ADV)
                        if len(x)==0:
                            entity_data[pkind].append({'name':v.lower(),'count':1,'keywords':[v.replace('.',' ').lower(),k],'wordnet_name':'n/a','synonyms':[]})
                        else:
                            for ii in entity_data[pkind]:
                                if str(x[0]).split("'")[1] == ii['wordnet_name']:
                                    ii['count'] += 1
                                    ii['keywords'].append(k)
                                    ii['synonyms'].append(v.lower())
                                    c=1
                            if c==0:
                                dlemma={}
                                for lemma in x[0].lemmas():
                                    dlemma[str(lemma).split("'")[1]] = lemma.frame_strings()

                                # if (len(x[0].examples()) > 0): print 'example of ',text, ' is ', (x[0].examples()[0])
                                entity_data[pkind].append(
                                    {'name': v.lower(), 'count': 1, 'keywords': [v.replace('.', ' ').lower(), k],
                                     'wordnet_name': str(x[0]).split("'")[1], 'synonyms': [],'definition':x[0].definition(),'lemmas':dlemma})


                                conv_data.append({'sentence':x[0].definition(),"label":"learning",'source':'wordnet'})
                                for xxx in x[0].examples():
                                    conv_data.append({'sentence': xxx, "label": "learning",'source':'wordnet'})

                print pkind,len(entity_data[pkind])
                entity_data[pkind] = sorted(entity_data[pkind], key=itemgetter('count'), reverse=True)
            i['entity_learning_status']="done"
    #//////Saving on memory
    with open('entity_lib00.json', 'w') as outfile:
        json.dump(entity_data, outfile)
    with open('Data_User_Input3.json', 'w') as outfile:
        json.dump(conv_data, outfile)
    #print len(t['verb'])

elif fun == 'IMPORT-From-Wordnet':
    with open('entity_library00.txt') as data_file:
        tset = json.load(data_file)

    # http://www.nltk.org/howto/wordnet.html
    from nltk.corpus import wordnet as wn

    for i in tset['verbs'].keys():
    # input
        text = i.replace('.',' ')
        tset['verbs'][i]['keywords'].append(text)
        t=len(text.split(' '))
        if t==2 and text.split(' ')[0]=='to':
            text=text.split(' ')[1]
        if t==2 and text.split(' ')[0] in ['should','would','will','may','might','shall','can','could','has','have','had','are','be','is','am','was','were']:
            try: text=text.split(' ')[1]
            except: text=text.split(' ')[0]
        elif t==3 and text.split(' ')[0]+' '+text.split(' ')[1] in ['want to','wanted to','is being','likes to','like to','need to','plan to']:
            text=text.split(' ')[2]

    # Look up a word using synsets(); this function has an optional pos argument which lets you constrain the part of speech of the word:
        #print text,' = ',wn.synsets(text)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    #which = raw_input("Enter an option: ")

    # Parts of speech are VERB, NOUN, ADJ and ADV. A synset is identified with a 3-part name of the form: word.pos.nn:
        tset['verbs'][i]['keywords'].append(text)
        tset['verbs'][i]['name'] = text
        x=wn.synsets(text, pos=wn.VERB)
        t=len(x)
        if t!=0:
            #print text,' = ',wn.synsets(text, pos=wn.VERB)
            tset['verbs'][i]['wordnet_name']=str(x[0]).split("'")[1]
            #print text,' number of meanings ',t
            #print text, ' is ', x[0].definition()
            tset['verbs'][i]['definition'] = x[0].definition()
            #if (len(x[0].examples()) > 0): print 'example of ',text, ' is ', (x[0].examples()[0])
            print (x[0].lemmas())
            #print (x[1].lemmas())
    # Synset: a set of synonyms that share a common meaning.
            #print 'Hypernyms:', x[0].hypernyms()
            #print 'Hyponyms:', x[0].hyponyms()
            print 'Member holonyms', x[0].member_holonyms()
    #print 'Root hypernyms:', wn.synset(which).root_hypernyms()
    #print 'Lowest common hypernyms:', wn.synset(which).lowest_common_hypernyms(wn.synset('cat.n.01'))
    #print 'Antonyms:', wn.synset(which).lemmas()[0].antonyms()
    #print 'Derivationally related forms:', wn.synset(which).lemmas()[0].derivationally_related_forms()
    #print 'Pertainyms:', wn.synset(which).lemmas()[0].pertainyms()
            #print 'Frame IDs:', x[0].frame_ids()
            for lemma in x[0].lemmas():
                #print(lemma, lemma.frame_ids())
                print(" | ".join(lemma.frame_strings()))
                #print lemma.frame_strings()
    with open('entity_library00.txt', 'w') as outfile:
        json.dump(tset, outfile)

elif fun == 'IMPORT-From-Wikipedia':

    #with open('Data_User_Input4.json') as working_file:
    #    conv_data = json.load(working_file)

    with open('Entity_lib08.json') as data_file:
        entity_data = json.load(data_file)

    for j in entity_data.keys():
        for i in entity_data[j]:
            if (i['count']>1)and(i['name']!='')and('wiki_search' not in i.keys()):
                i['wiki_search']=[]
                max=0
                wiki=[]
                for w in wikipedia.search(i["name"].replace('.', ' ')):
                    if max<10:
                        try:
                            wiki.append(str(w))
                            max+=1
                        except:
                            print "Ascii-problem"

                for w in wiki:
                    try:
                        i['wiki_search'].append(str(w))
                    except:
                        print "Ascii-problem"

                    print "THIS IS THE WORD: ",w," . ",i['name'],' . ',j
                    #ny = wikipedia.page(w)
                    #ny.url
                    #print ny.content
                    #print ny.links
                    """try:
                        #print wikipedia.summary(w)
                        for y in wikipedia.summary(w).split('\n'):
                            for x in y.split('.'):
                                try:
                                    if x!= '':
                                        conv_data.append({'sentence': str(x).replace("\"",""), "label": "learning","source":"wikipedia"})
                                    #print x
                                except:
                                    print "Ascii-problem"
                    except:
                        print "no response"""

                #print i["name"]," : ",wikipedia.search(i["name"].replace('.',' '))

    # //////Saving on memory
    with open('entity_lib09.json', 'w') as outfile:
        json.dump(entity_data, outfile)
    #with open('Data_User_Input4.json', 'w') as outfile:
    #    json.dump(conv_data, outfile)

elif fun =='REFINE-Entities-0':
    with open('entity_lib03.json') as data_file:
        entity_data = json.load(data_file)

    pos={'np':'n','vp':'v','adjp':'a','advp':'r'}
    for pkind in entity_data.keys():
        k=0
        counter=0
        for i in entity_data[pkind]:
            a=0
            counter+=1
            #if i['name']!=''and(i["wordnet_name"]!='n/a'):
                #if i["wordnet_name"].split('.')[0]!=i['name'].lower():
                    #A = annotator.getAnnotations(i['name'].replace('.',' '), dep_parse=True)
                    #i['name']=WordNetLemmatizer().lemmatize(i['name'].replace('.',' '),'v').replace(' ','.')
                    #print i["wordnet_name"],i['name'].lower()#,WordNetLemmatizer().lemmatize(i['name'].replace('.',' '),'v')#,A['pos'][0][1]
            if i["wordnet_name"]=='n/a':
                new_name=''
                print counter,"  ",i['name']
                for x in i['name'].split('.'):
                    if (pkind=='vp')and(x not in no_verb)and(x not in ['does','do','did',"doesn't","dont","always","otherwise",'first','second','later','initially',"'n","'p"]):
                        if new_name=='':
                            new_name=x
                        else:
                            new_name=new_name+'.'+x

                    elif (pkind=='np')and(x not in poiner_words)and(x not in ["'s",'not',"'n","'p",'most']):
                        if new_name=='':
                            new_name=x
                        else:
                            new_name=new_name+'.'+x

                    elif (pkind=='adjp')and(x not in ["very",'most',"'n","'p"]):
                        if new_name=='':
                            new_name=x
                        else:
                            new_name=new_name+'.'+x

                    elif (pkind=='advp')and(x not in ["'s",'very']):
                        if new_name=='':
                            new_name=x
                        else:
                            new_name=new_name+'.'+x



                if new_name!='':
                    i['name']=new_name
                    i['name'] = WordNetLemmatizer().lemmatize(i['name'].replace('.', ' '), pos[pkind]).replace(' ', '.')
                for b in['or','and',',','.',')','(','/','"',';',':']:
                    if b in i['name'].split('.'):
                        if b==i['name'].split('.')[0]:
                            i['name']='.'+i['name']
                        elif b==i['name'].split('.')[-1]:
                            i['name']=i['name']+'.'
                        for o in i['name'].split('.'+b+'.'):
                            if o not in ['or','and',',','.',')','(','/','','.or','.and']:
                                x = wn.synsets(o.replace('.', ' '), pos=wn.VERB)
                                if len(x)==0:
                                    if type(i['keywords'])==list:
                                        entity_data[pkind].append(
                                            {'name': o.lower(), 'count': i['count'], 'keywords': [o.replace('.', ' ').lower()].extend(i['keywords']),
                                            'wordnet_name':'n/a', 'synonyms': []})
                                    else: i['keywords']=[]
                                else:
                                    dlemma = {}
                                    for lemma in x[0].lemmas():
                                        dlemma[str(lemma).split("'")[1]] = lemma.frame_strings()
                                    if type(i['keywords'])==list:
                                        entity_data[pkind].append(
                                            {'name': o.lower(), 'count': i['count'], 'keywords': [o.replace('.', ' ').lower()].extend(i['keywords']),
                                             'wordnet_name': str(x[0]).split("'")[1], 'synonyms': [],
                                             'definition': x[0].definition(),
                                             'lemmas': dlemma})
                                    else: i['keywords']=[]
                        i['count']=0
            i['name'] = WordNetLemmatizer().lemmatize(i['name'].replace('.', ' '), pos[pkind]).replace(' ', '.')



        entity_data[pkind] = sorted(entity_data[pkind], key=itemgetter('count'), reverse=True)
        ed=[]
        for i in entity_data[pkind]:
            b=0
            for j in ed:
                if type(i['keywords'])!=list:
                    b=1
                elif j['name']==i['name'] and j['wordnet_name']==i['wordnet_name']:
                    j['count']+=i['count']
                    j['keywords'].extend(i['keywords'])
                    j['keywords'] = list(set(j['keywords']))
                    b=1
                    a+=1
                    break
                elif i['name'].replace('.',' ').lower() in j['keywords']:
                    j['count'] += i['count']
                    j['keywords'].extend(i['keywords'])
                    j['keywords'] = list(set(j['keywords']))
                    b = 1
                    a += 1
                    break
                elif j['wordnet_name']==i['wordnet_name'] and j['wordnet_name']!='n/a':
                    j['count']+=i['count']
                    j['keywords'].extend(i['keywords'])
                    j['keywords'] = list(set(j['keywords']))
                    j['synonyms'].append(i['name'].replace('.',' ').lower())
                    j['synonyms'] = list(set(j['synonyms']))
                    b=1
                    a+=1
                    break
                elif i['count']==0:
                    b=1
            if b==0:
                ed.append(i)

            if a>1:
                k+=1
                print i['name']
            else:
                print "wrong"
        print pkind,"total:",k, len(ed)*100/len(entity_data[pkind])
        entity_data[pkind]=ed
        with open('entity_lib03.json', 'w') as outfile:
            json.dump(entity_data, outfile)

elif fun =='REFINE-Entities-1':
    with open('entity_lib10.json') as data_file:
        entity_data = json.load(data_file)
    for pkind in entity_data.keys():

        ex=[]
        for i in entity_data[pkind]:
            if 'count' in i.keys() and i['count']>0 :
                ex.append(i)
        entity_data[pkind]=ex

    with open('entity_lib10.json', 'w') as outfile:
        json.dump(entity_data, outfile)

elif fun =='SORT-Entities-count':
    with open('entity_lib03.json') as data_file:
        entity_data = json.load(data_file)
    for pkind in entity_data.keys():
        entity_data[pkind] = sorted(entity_data[pkind], key=itemgetter('count'), reverse=True)
    with open('entity_lib03.json', 'w') as outfile:
        json.dump(entity_data, outfile)

elif fun =='SORT-Entities-numOfKeywords':
    with open('entity_lib03.json') as data_file:
        entity_data = json.load(data_file)

    for pkind in entity_data.keys():
        for i in entity_data[pkind]:
            i['number_of_keywords']=len(i['keywords'])
            i['ave_repeat_keywords']=float(i['count'])/i['number_of_keywords']
        entity_data[pkind] = sorted(entity_data[pkind], key=itemgetter('ave_repeat_keywords'), reverse=True)
    with open('entity_lib03.json', 'w') as outfile:
        json.dump(entity_data, outfile)

elif fun =='MAKE-Keywords-dict':
    with open('entity_lib03.json') as data_file:
        entity_data = json.load(data_file)

    try:
        with open('group_entity00.json') as data_file:
            di = json.load(data_file)
    except:
        di={'np':[],'vp':[],'adjp':[],'advp':[]}


    for pkind in entity_data.keys():
        #di[pkind]={}
        counter=0
        for i in entity_data[pkind]:
            counter+=1
            if len(i['name'].split('.'))==1:
                if 'keyword_dict' not in i.keys() and (i['count']>500):# and (i['count']<500):
                    i['keyword_dict']=[]
                    for j in i['keywords']:
                        A = annotator.getAnnotations(j, dep_parse=False)
                        key=''

                        for a in A['pos']:
                            t=1
                            b=['X%s'%(pkind),a[1]]
                            if str(a[0])==i['name'].lower() or str(a[0]).lower() in i['synonyms'] or (WordNetLemmatizer().lemmatize(str(a[0]))).lower()==i['name'].lower():
                               t=0
                            if key=='':
                                key+=b[t]
                            else:
                                key+='+'+b[t]
                        number=(float(i['count']))/len(i['keywords'])
                        t=0
                        for a in di[pkind]:
                            if key==a['structure']:
                                a['examples'].append((j, number))
                                a['count'] += number
                                t=1
                                break
                        o = 0
                        for a in i['keyword_dict']:
                            if key == a['structure']:
                                a['examples'].append((j, number))
                                a['count'] += number
                                o = 1
                                break
                        if key!='' and o==0:
                            i['keyword_dict'].append({'structure':key,'examples':[(j,number)],'count': number})

                        if key!='' and t==0:
                            di[pkind].append({'structure':key,'examples':[(j,number)],'count': number})
                            print counter,key
                        else:
                            print counter


    # //////Saving on memory
    with open('group_entity00.json', 'w') as outfile:
        json.dump(di, outfile)
    with open('entity_lib04.json', 'w') as outfile:
        json.dump(entity_data, outfile)

elif fun =='MODIFY-Keywords-dict0':
    with open('group_entity00.json') as data_file:
        di = json.load(data_file)

    #di = {}
    for pkind in di.keys():
        for i in di[pkind]:
            ex=[]
            for j in i['examples']:
                er=0
                for k in ex:
                    if j[0].lower()==k[0].lower():
                        k[1]+=j[1]
                        er=1
                        break
                if er==0:
                    ex.append(j)

            i['examples']=ex
            i['number_of_examples']=len(i['examples'])
        """di[pkind] = []
        for i in entity_data[pkind].keys():
            num=0.0
            for j in entity_data[pkind][i]:
                num+=j[1]

            di[pkind].append({'structure':i,'examples':entity_data[pkind][i],'count':num})
        """
        di[pkind] = sorted(di[pkind], key=itemgetter('number_of_examples'), reverse=True)


    # //////Saving on memory
    with open('group_entity00.json', 'w') as outfile:
        json.dump(di, outfile)

elif fun =='MODIFY-Keywords-dict1':
    with open('group_entity00.json') as data_file:
        di = json.load(data_file)


    for pkind in di.keys():
        di2 = []
        for i in di[pkind]:
            i['tree']={}
            p=0
            for t in i['structure'].split('+'):
                if t not in i['tree'].keys():
                    i['tree'][t]=[]
                elif t+'1'not in i['tree'].keys():
                    i['tree'][t+'1'] = []
                    t=t+'1'
                elif t+'2'not in i['tree'].keys():
                    i['tree'][t+'2'] = []
                    t=t+'2'
                elif t+'3'not in i['tree'].keys():
                    i['tree'][t+'3'] = []
                    t=t+'3'
                elif t+'4'not in i['tree'].keys():
                    i['tree'][t+'4'] = []
                    t=t+'4'
                for j in i['examples']:
                    b=0
                    for tt in i['tree'][t]:
                        if tt[0]==j[0].split(' ')[p].lower():
                            tt[1]+=j[1]/i['count']
                            b=1
                    if b==0:
                        print i['structure'],t,j[0]
                        i['tree'][t].append([j[0].split(' ')[p].lower(),j[1]/i['count']])
                ex=[]
                for tt in i['tree'][t]:
                    if tt[1]>0.05 :
                        ex.append(tt)
                i['tree'][t]=ex


                p+=1
            i['examples']=[]
            if i['count'] > 10 and i['number_of_examples'] > 3:
                di2.append(i)
        di[pkind]=di2

    # //////Saving on memory
    with open('group_entity02.json', 'w') as outfile:
        json.dump(di, outfile)

elif fun == 'Add-Values-TO-noun':
    with open('entity_lib07.json') as data_file:
        entity_data = json.load(data_file)
    for i in entity_data['np']:
        if "keyword_dict" in i.keys():
            print i['name']
            if 'values' not in i.keys():
                i['values']=[]
            if 'entiti_attrib_class' not in i.keys():
                i['entiti_attrib_class'] = []
            if 'conditions' not in i.keys():
                i['conditions']=[]
            if 'functions' not in i.keys():
                i['functions']=[]

            for j in i["keyword_dict"]:
                key=0
                for pos in j["structure"].split('+'):
                    if pos in ["JJ","JJR","JJS"]:
                        for example in j["examples"]:
                            adj=example[0].split(" ")[key].lower()
                            tt=0
                            for t in i['values']:
                                if t[0]==adj and t[2]==pos:
                                    t[1]+=example[1]
                                    tt=1
                                    break
                            if tt==0:
                                i['values'].append([adj,example[1],pos])
                    elif pos in ["NN","NNS","NNP","NNPS"]:
                        for example in j["examples"]:
                            if len(example[0].split(" "))>key:
                                adj=example[0].split(" ")[key].lower()
                                tt=0
                                for t in i['entiti_attrib_class']:
                                    if t[0]==adj and t[2]==pos:
                                        t[1]+=example[1]
                                        tt=1
                                        break
                                if tt==0:
                                    i['entiti_attrib_class'].append([adj,example[1],pos])
                    key+=1
            i['values'] = sorted(i['values'], key=itemgetter(1), reverse=True)
            i['entiti_attrib_class'] = sorted(i['entiti_attrib_class'], key=itemgetter(1), reverse=True)

    with open('entity_lib08.json', 'w') as outfile:
        json.dump(entity_data, outfile)

elif fun == 'Find-multi-words-in-WORDNET':
    with open('entity_lib10.json') as data_file:
        entity_data = json.load(data_file)
    for pkind in entity_data.keys():
        for i in entity_data[pkind]:
            if i['wordnet_name']=='n/a' and '.' in i['name']:
                print i['name']
                v=i['name']
                if pkind == 'np':
                    x = wn.synsets(v.replace('.', '_'), pos=wn.NOUN)
                elif pkind == 'vp':
                    x = wn.synsets(v.replace('.', '_'), pos=wn.VERB)
                elif pkind == 'adjp':
                    x = wn.synsets(v.replace('.', '_'), pos=wn.ADJ)
                elif pkind == 'advp':
                    x = wn.synsets(v.replace('.', '_'), pos=wn.ADV)
                if len(x) != 0:
                    c=0
                    for ii in entity_data[pkind]:
                        if str(x[0]).split("'")[1] == ii['wordnet_name']:
                            print 'already in dictionary..'
                            ii['count'] += i['count']
                            ii['number_of_keywords'] += i['number_of_keywords']
                            try :
                                ii['keyword_dict'].extend(i['keyword_dict'])
                            except :
                                if 'keyword_dict' not in ii.keys():
                                    try: ii['keyword_dict']=(i['keyword_dict'])
                                    except: ii['keyword_dict']=[]

                            ii['wiki_search'].extend(i['wiki_search'])
                            ii['synonyms'].extend(i['synonyms'])
                            i={}
                            c = 1
                    if c == 0:
                        print "wordnet added..."
                        dlemma = {}
                        for lemma in x[0].lemmas():
                            dlemma[str(lemma).split("'")[1]] = lemma.frame_strings()
                        i['wordnet_name']= str(x[0]).split("'")[1]
                        i['definition']= x[0].definition()
                        i['lemmas']=dlemma

    with open('entity_lib10.json', 'w') as outfile:
        json.dump(entity_data, outfile)

elif fun == 'ADD-GRAMMAR':
    with open('entity_lib10.json') as data_file:
        entity_data = json.load(data_file)
    p={'np':'n','vp':'v','adjp':'adj','advp':'adv'}
    r={'np':{
    'NN':'',     # Noun, singular or mass
    'NNS':'',    # Noun, plural
    'NNP':'',    # Proper noun, singular
    'NNPS':''    # Proper noun, plural
    },
    'vp':{
    'VB':'',     # Verb, base form
    'VBD':'',    # Verb, past tense
    'VBG':'',    # Verb, gerund or present participle
    'VBN':'',    # Verb, past participle
    'VBP':'',    # Verb, non-3rd person singular present
    'VBZ':''     # Verb, 3rd person singular present
},
    'adjp':{
    'JJ':'',     # Adjective
    'JJR':'',    # Adjective, comparative
    'JJS':''     # Adjective, superlative
},
    'advp':{
    'RB':'',     # Adverb
    'RBR':'',    # Adverb, comparative
    'RBS':''     # Adverb, superlative
    }}
    for pkind in entity_data.keys():
        for i in entity_data[pkind]:
            if 'grammar' not in i.keys():
                print i['name']
                i['grammar']={'pos':p[pkind],'related':r[pkind]}
    with open('entity_lib10.json', 'w') as outfile:
        json.dump(entity_data, outfile)

elif fun == 'GUESS-Type':
    with open('entity_lib10.json') as data_file:
        entity_data = json.load(data_file)
    for pkind in entity_data.keys():
        for i in entity_data[pkind]:
            if 'type' in i.keys() and i['type']=='n/a':
                item=i
                evidence = [pkind]
                if 'wordnet_name' in item.keys():
                    if item['wordnet_name'] != 'n/a' and len(item['wordnet_name'].split('.'))==3:
                        try : evidence.append(item['wordnet_name'].split('.')[1])
                        except: print item['wordnet_name']

                        x=wn.synset(item['wordnet_name'])
                        if len(x.attributes())>0:
                            evidence.append("att")
                        if len(x.member_holonyms())>0 or len(x.part_holonyms())>0 or len(x.substance_holonyms())>0 or len(x.member_meronyms())>0 or len(x.part_meronyms())>0 or len(x.substance_meronyms())>0:
                            evidence.append("mps")


                decison = {}
                for j in ['VALUE','ATTRIBUTE','CLASS','ENTITY','FUNCTION','CONDITION']:
                    decison[j] = 0
                for j in evidence:
                    if j in ['np', 'n']:
                        decison['ATTRIBUTE'] += 1
                        decison['CLASS'] += 1
                        decison['ENTITY'] += 1
                        #print "DEFENITION: " + item['definition']
                        #print "WORDNET: " + item['wordnet_name']
                    elif j in ['adjp', 'a','s']:
                        decison['VALUE'] += 1
                    elif j in ['vp', 'v']:
                        decison['FUNCTION'] += 1
                    elif j in ['advp', 'r']:
                        decison['CONDITION'] += 1
                    elif j=='att':
                        decison['ATTRIBUTE'] += 1
                        decison['VALUE'] += 1
                    elif j=='mps':
                        decison['CLASS'] += 1
                        decison['ENTITY'] += 1

                max_value = max(decison.values())  # maximum value
                max_keys = [k for k, v in decison.items() if v == max_value]
                if len(max_keys)==1:
                    i['type']=max_keys[0]
                else:
                    i['type']='n/a'
                print i['name'],' : ',i['type']

    with open('entity_lib11.json', 'w') as outfile:
        json.dump(entity_data, outfile)


#S.put_item({"name":"emotion","type":"ATTRIBUTE","values":[['happy',50,'JJ'],['bad',100,'JJ'],['good',100,'JJ'],['mad',50,'JJ'],['angry',50,'JJ'],['joyful',50,'JJ'],['frightened',50,'JJ'],['scared',50,'JJ'],['excited',50,'JJ'],['sad',50,'JJ']]})
#S.import_words_from_entity_lib(9,1000)

#S.save_sm(0)
#sort_based('entity_lib04','count')
show_stat_of_dif_pkind('entity_lib11',"type")
#A = annotator.getAnnotations("I like to go to my school", dep_parse=True)
#print A['srl']
#print A['chunk']


#wikiyear="A year is the orbital period of the Earth moving in its orbit around the Sun. Due to the Earth's axial tilt, the course of a year sees the passing of the seasons, marked by changes in weather, the hours of daylight, and, consequently, vegetation and soil fertility. In temperate and subpolar regions around the globe, four seasons are generally recognized: spring, summer, autumn and winter. In tropical and subtropical regions several geographical sectors do not present defined seasons; but in the seasonal tropics, the annual wet and dry seasons are recognized and tracked.A calendar year is an approximation of the number of days of the Earth's orbital period as counted in a given calendar. The Gregorian, or modern, calendar, presents its calendar year to be either a common year of 365 days or a leap year of 366 days, as do the Julian calendars; see below. For the Gregorian calendar the average length of the calendar year (the mean year) across the complete leap cycle of 400 years is 365.2425 days. The ISO standard ISO 80000-3, Annex C, supports the symbol 'a' (for Latin annus) to represent a year of either 365 or 366 days. In English, the abbreviations 'y' and 'yr' are commonly used.In astronomy, the Julian year is a unit of time; it is defined as 365.25 days of exactly 86400 seconds (SI base unit), totalling exactly 31557600 seconds in the Julian astronomical year."
#frog6="Frogs are small animals that can live on land and in water. Frogs lay lots of eggs in the water that hatch into tadpoles. Tadpoles look like little fish. After a few weeks, the tadpole starts to grow arms and legs. The back legs grow bigger and the tail gets smaller until the frog is fully grown. Frogs use their long sticky tongues to catch food. Frogs like to eat insects, but some frogs eat other frogs! Frogs call to each other by croaking. Each kind of frog has a different croaking sound. Frogs are good jumpers because of their strong back legs. Frogs come in lots of different colors. Some frogs use their colors to hide. Can you find a frog in this picture? The next time you go outside, see what kinds of frogs you can find!"
#W.nl_article_input(frog6,"freekidsbooks","frog")
#W.save_wm("1")



