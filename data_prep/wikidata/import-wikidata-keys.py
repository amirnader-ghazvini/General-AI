import json, urllib

with open('wikidata-keys2.json') as working_file:
    dic = json.load(working_file)

for n in range(1090000,2000000):
    i='Q%s'%(n)
    if i not in dic.keys():
        url="https://wikidata.org/wiki/Special:EntityData/%s.json"%(i)
        #wb_doc = requests.get(url).json()
        try:
            wb_doc = json.loads(urllib.urlopen(url).read())
            dic[i]={'label':wb_doc["entities"][i]['labels']['en']['value'],'wikiid':i,'alias':[]}
            if type(wb_doc['entities'][i]['aliases']) == dict:
                if 'en' in wb_doc['entities'][i]['aliases'].keys():
                    for j in wb_doc['entities'][i]['aliases']['en']:
                        dic[i]['alias'].append(j['value'])

            print i,'  ' ,wb_doc["entities"][i]['labels']['en']['value']
            if (n%100)==0:
                with open('wikidata-keys2.json', 'w') as outfile:
                    json.dump(dic, outfile)
        except:
            print i, '  N/A'
            if (n % 100) == 0:
                with open('wikidata-keys2.json', 'w') as outfile:
                    json.dump(dic, outfile)
            continue