import json

with open("Action_list.json") as memory:
    s1 = json.load(memory)
with open("Verb_list.json") as memory:
    s2 = json.load(memory)


dic=[]
for i in s2:
    if i['name'] not in i['synonyms']:
        i['synonyms'].append(i['name'])
    if 'lemmas' in i.keys():
        for j in i['lemmas'].keys():
            if j.split('.')[-1] not in i['synonyms']:
                i['synonyms'].append(j.split('.')[-1])



for j in s1:
    h=0
    for i in s2:
        if j['name'].lower() in i["synonyms"]:
            h=+1
            #i['action:id']=j['id']
            j['syntax']=i
            j['semantic']=[]
    print j['name'],h




#print len(dic)

with open('Verb_list.json', 'w') as outfile:
    json.dump(s2, outfile)
with open('Action_list.json', 'w') as outfile:
    json.dump(s1, outfile)