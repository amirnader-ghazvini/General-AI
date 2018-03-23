import json, simplejson
import urllib2,urllib, time
import math

#l1 is a list or dict and l2 is a dict
def keyword_extraction(l1,l2):
    if type(l1) is list:
        for i in l1:
            if type(i) is dict:
                for p in i.keys():
                    if (type(i[p]) is dict) or (type(i[p]) is list):
                        if p in l2.keys():
                            keyword_extraction(i[p],l2[p])
                        else:
                            l2[p]={}
                            keyword_extraction(i[p], l2[p])
                    else:
                        if p in l2.keys():
                            l2[p].append(i[p])
                            l2[p] = list(set(l2[p]))
                        else:
                            l2[p] = []
                            l2[p].append(i[p])
    else:
        for p in l1.keys():
            if (type(l1[p]) is dict) or (type(l1[p]) is list):
                if p in l2.keys():
                    keyword_extraction(l1[p], l2[p])
                else:
                    l2[p] = {}
                    keyword_extraction(l1[p], l2[p])
            else:
                if p in l2.keys():
                    l2[p].append(l1[p])
                    l2[p] = list(set(l2[p]))
                else:
                    l2[p] = []
                    l2[p].append(l1[p])

#Keywords refine // l2 is a dict and a is a list of not important labels
def keyword_refine(l2,x):
    for i in x:
        l2.pop(i, None)
    for i in l2.keys():
        if type(l2[i]) is dict:
            keyword_refine(l2[i],x)
        else:
            a=0
            for s in l2[i]:
                if (type(s) is not int) and (type(s) is not float):
                    a=1
            if a==0:# and len(l2[i])>10:
                l2[i]={"max":max(l2[i]),"min":min(l2[i])}

#fix json file
def fix_json(l):
    l3=[]
    for i in l:
        l2 = {}
        for j in i.keys():
            if '.' in j:
                if j.split('.')[0] not in l2.keys():
                    l2[j.split('.')[0]]={}
                    l2[j.split('.')[0]][j.split('.')[1]]=i[j]
                else:
                    l2[j.split('.')[0]][j.split('.')[1]] = i[j]
            else:
                l2[j]=i[j]
        l3.append(l2)
    return l3


#x is dict and keydict is key and root is a string that shows root key value and key is a string that shows last key value
def keyword_making(x,keydict,root,key):
    if len(x.keys())==2 and 'max' in x.keys() and 'min' in x.keys() :
        keydict[root]=["# "+key]
    else:
        for i in x.keys():
            if type(x[i]) is list:
                for j in x[i]:
                    keydict[root + "." + str(i) + ":" + str(j)] = [str(j).lower()]
                    if ',' in str(j):
                        for xx in str(j).split(','):
                            keydict[root + "." + str(i) + ":" + str(j)].append(xx.lower())
                    if type(j) is str:
                        keydict[root + "." + str(i) + ":" + str(j)].append([j.lower()])
                        if ' ' in j:
                            #keydict[root + "//" + str(i) + "//" + str(j)].extend(j.lower().split(' '))
                            keydict[root + "." + str(i) + ":" + str(j)].append(j.lower().replace(' ', '-'))
                        if '-' in j:
                            #keydict[root + "//" + str(i) + "//" + str(j)].extend(j.lower().split('-'))
                            keydict[root + "." + str(i) + ":" + str(j)].append(j.lower().replace('-',' '))
                        if '_' in j:
                            #keydict[root + "//" + str(i) + "//" + str(j)].extend(j.lower().split('_'))
                            keydict[root + "." + str(i) + ":" + str(j)].append(j.lower().replace('_',' '))
                        if '/' in j:
                            keydict[root + "." + str(i) + ":" + str(j)].extend(j.lower().split('/'))
            else:
                keyword_making(x[i],keydict,root + "." + str(i),i)


#//////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////// Open info data base
with open("Beef-info.json") as car_list:
    list3 = json.load(car_list)

#//////////////////////// Make All in one database
list2={}
keyword_extraction(list3,list2)
#with open('Party-keywords.json', 'w') as outfile:
#    json.dump(list2, outfile)

# /////////////////////// Refine All in one database
#for cars
#a=['id','code','manufacturerCode','squishVins','estimateTmv','hex','manufactureOptionCode','manufactureOptionName','equipmentType']
#for baby
#a=['description','picUrl','details','productId']
# for party
a=['productName','picUrl','productId','description']
keyword_refine(list2 , a)


#with open('Party-keywords.json', 'w') as outfile:
#    json.dump(list2, outfile)

# /////////////////////// Make keyword style db for entity
list3={}
keyword_making(list2,list3,'party','')


with open('test.json', 'w') as outfile:
    json.dump(list3, outfile)
#l2=fix_json(list3)


