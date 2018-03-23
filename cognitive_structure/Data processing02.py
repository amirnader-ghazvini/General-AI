""""""" THIS PROGRAM PRE-PROCESS THE USER INPUT DATA " \
"           AND GENERATE NEW DATA BASE "



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
noun_list=[
    'NN',     # Noun, singular or mass
    'NNS',    # Noun, plural
    'NNP',    # Proper noun, singular
    'NNPS',   # Proper noun, plural
]
verb_list=[
    'VB',     # Verb, base form
    'VBD',    # Verb, past tense
    'VBG',    # Verb, gerund or present participle
    'VBN',    # Verb, past participle
    'VBP',    # Verb, non-3rd person singular present
    'VBZ',    # Verb, 3rd person singular present
]


with open('Data_User_Input3.json') as data_file:
    tset = json.load(data_file)

for i in tset:
    if ('nlp' not in i.keys()) and i['sentence'] != '' and i['sentence'].split(' ')[0] != '':
        #i['new_entities']=[]
        #i['verb_entities']=[]
        #///// NLP adding
        try:
            ascii_check=str(i['sentence'])
        except:
            continue

        try:
            A = annotator.getAnnotations(i['sentence'], dep_parse=True)
        except:
            continue
        i['nlp'] = {}
        p=[]
        for t in range(len(A['pos'])):
           p.append({'token':A['pos'][t][0].lower(),'pos':A['pos'][t][1],'chunk':A['chunk'][t][1],'ner':A['ner'][t][1]})
        i['nlp']['words']=p

        #####################################   Group entities Recognition
        h = ''
        v = ''
        i['Group_Entities'] = {'np': [], 'vp': [], 'adjp': [], 'advp': []}
        for j in range(len(A['chunk'])):
            #   Noun Phrase
            if A['chunk'][j][1] == 'S-NP':
                i['Group_Entities']['np'].append(h + A['chunk'][j][0] + '--' + A['pos'][j][1])
                h = ''

            #elif A['chunk'][j][1] == 'S-PP':
            #    h = A['chunk'][j][0] + '--' + A['pos'][j][1] + '.'

            elif A['chunk'][j][1] == 'B-NP':
                h = h + A['chunk'][j][0] + '--' + A['pos'][j][1] + '.'
            elif A['chunk'][j][1] == 'I-NP':
                h = h + A['chunk'][j][0] + '--' + A['pos'][j][1] + '.'
            elif A['chunk'][j][1] == 'E-NP':
                h = h + A['chunk'][j][0] + '--' + A['pos'][j][1]
                i['Group_Entities']['np'].append(h)
                h = ''
            # Verb Phrase
            elif A['chunk'][j][1] == 'S-VP':
                i['Group_Entities']['vp'].append(A['chunk'][j][0] + '--' + A['pos'][j][1])
                h = ''

            elif A['chunk'][j][1] == 'B-VP':
                v = A['chunk'][j][0] + '--' + A['pos'][j][1] + '.'
                h = ''
            elif A['chunk'][j][1] == 'I-VP':
                v = v + A['chunk'][j][0] + '--' + A['pos'][j][1] + '.'
            elif A['chunk'][j][1] == 'E-VP':
                v = v + A['chunk'][j][0] + '--' + A['pos'][j][1]
                i['Group_Entities']['vp'].append(v)
                v = ''
            # Adjective Phrase
            elif A['chunk'][j][1] == 'S-ADJP':
                i['Group_Entities']['adjp'].append(A['chunk'][j][0] + '--' + A['pos'][j][1])
                h = ''

            elif A['chunk'][j][1] == 'B-ADJP':
                v = A['chunk'][j][0] + '--' + A['pos'][j][1] + '.'
                h = ''
            elif A['chunk'][j][1] == 'I-ADJP':
                v = v + A['chunk'][j][0] + '--' + A['pos'][j][1] + '.'
            elif A['chunk'][j][1] == 'E-ADJP':
                v = v + A['chunk'][j][0] + '--' + A['pos'][j][1]
                i['Group_Entities']['adjp'].append(v)
                v = ''
            # Adverb Phrase
            elif A['chunk'][j][1] == 'S-ADVP':
                i['Group_Entities']['advp'].append(A['chunk'][j][0] + '--' + A['pos'][j][1])
                h = ''

            elif A['chunk'][j][1] == 'B-ADVP':
                v = A['chunk'][j][0] + '--' + A['pos'][j][1] + '.'
                h = ''
            elif A['chunk'][j][1] == 'I-ADVP':
                v = v + A['chunk'][j][0] + '--' + A['pos'][j][1] + '.'
            elif A['chunk'][j][1] == 'E-ADVP':
                v = v + A['chunk'][j][0] + '--' + A['pos'][j][1]
                i['Group_Entities']['advp'].append(v)
                v = ''


        #print 'SRL:', A['srl']
        # for i in A['srl']:
        #   print i['V']
        #////// Vrebs wordnet

        #for j in i['verb_entities']:


        #///// NLP Tree
        sy=A['syntax_tree']
        sy=sy.replace(')(',',')
        sy = sy.replace('(', ':{')
        sy = sy.replace(' ', ':')
        sy = sy.replace(')', '}')
        t=0
        sy=str(sy[1:])
        sy2=sy
        tt=0
        for j in range(len(sy)):
            if (sy[j] in ['{','}',':',',']) and t==0:
                t=1
                sy2 = sy2[:j+tt] + "'" + sy2[j+tt:]
                tt=tt+1
                continue
            elif (sy[j] not in ['{','}',':',',']) and t==1:
                sy2 = sy2[:j+tt] + "'" + sy2[j+tt:]
                tt=tt+1
                t=0
            #elif t==1:
                #sy=sy[:j]+"'"+sy[j:]


        sy2=sy2[1:]
        sy2=sy2.replace("'",'"')
        #print sy2
        sy3={}
        try:
            sy3 = json.loads(sy2)
        except:
            sy3 = {}
        i['nlp']['tree']=sy3
        print i['sentence'] , str(sy3)
        #print 'Syntax1:', A['syntax_tree'] , str(type(A['syntax_tree']))
        #print A['dep_parse']

with open('Data_User_Input3.json', 'w') as outfile:
    json.dump(tset, outfile)
