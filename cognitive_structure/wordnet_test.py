# http://www.nltk.org/howto/wordnet.html
from nltk.corpus import wordnet as wn

text='react'
x=wn.synsets(text)
#x.append(wn.synset(text))
print text,' number of meanings ',len(x)
for i in range(len(x)):
    print text, ' is ', x[i].definition()
    print x[i].name()
    if (len(x[i].examples()) > 0): print 'example of ',text, ' is ', (x[i].examples()[0])
    print (x[i].lemmas())
# Synset: a set of synonyms that share a common meaning.
    print 'Hypernyms:', x[i].hypernyms()
    print 'Instance Hypernyms:', x[i].instance_hypernyms()
    print 'Root hypernyms:', wn.synset(x[i].name()).root_hypernyms()

    print 'Hyponyms:', x[i].hyponyms()

    print 'Member holonyms:', x[i].member_holonyms()
    print 'Substance holonyms:', x[i].substance_holonyms()
    print 'Part holonyms:', x[i].part_holonyms()

    print 'Member meronyms:', x[i].member_meronyms()
    print 'Substance meronyms:', x[i].substance_meronyms()
    print 'Part meronyms:', x[i].part_meronyms()

    print 'Topic domains:', x[i].topic_domains()
    print 'Region domains:', x[i].region_domains()
    print 'Usage domains:', x[i].usage_domains()

    print 'attributes:', x[i].attributes()
    print 'entailments:', x[i].entailments()
    print 'causes:', x[i].causes()
    print 'also see:', x[i].also_sees()

    # print 'Lowest common hypernyms:', wn.synset(which).lowest_common_hypernyms(wn.synset('cat.n.01'))
# print 'Antonyms:', wn.synset(which).lemmas()[0].antonyms()
# print 'Derivationally related forms:', wn.synset(which).lemmas()[0].derivationally_related_forms()
# print 'Pertainyms:', wn.synset(which).lemmas()[0].pertainyms()
# print 'Frame IDs:', x[0].frame_ids()
    for lemma in x[i].lemmas():
        print(lemma, lemma.frame_ids(),lemma.key(),lemma.name(),lemma.syntactic_marker())
        #print(" | ".join(lemma.frame_strings()))
        print lemma.frame_strings()
        print lemma.antonyms()
        print lemma.count()
        print lemma.derivationally_related_forms()
        print lemma.pertainyms()