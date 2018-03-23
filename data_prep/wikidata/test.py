import json, urllib
import requests

#url="http://g.co/kg/m/03jmrd"
#response2 = json.loads(urllib.urlopen(url).read())
#print str(response2)
x='formula'
#url2='https://www.wikidata.org/w/api.php?action=wbgetentities&titles='+x+'&sites=enwiki&props=&format=jsonfm&formatversion=2'
#url2='https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&titles='+x+'&format=json'
url2='https://www.wikidata.org/w/api.php?action=wbsearchentities&search='+x+'&language=en&format=json'#&type=property'

search_result = json.loads(urllib.urlopen(url2).read())
print str(search_result)
with open('test0.json', 'w') as outfile:
    json.dump(search_result, outfile)


i='Q976981'
url="https://wikidata.org/wiki/Special:EntityData/%s.json"%(i)
#wb_doc = requests.get(url).json()
wb_doc = json.loads(urllib.urlopen(url).read())


print i,'  ' ,wb_doc["entities"][i]['labels']['en']['value'],'    ',wb_doc['entities'][i]["descriptions"]['en']['value']
if type(wb_doc['entities'][i]['aliases'])==dict:
    if 'en' in wb_doc['entities'][i]['aliases'].keys():
        for j in wb_doc['entities'][i]['aliases']['en']:
            print j['value']
ii=i

for j in wb_doc['entities'][ii]['claims'].keys():

    i = j
    url = "https://wikidata.org/wiki/Special:EntityData/%s.json" % (i)
    test = json.loads(urllib.urlopen(url).read())
    print i, '  ', test["entities"][i]['labels']['en']['value']#, '    ', test['entities'][i]["descriptions"]['en']['value']

    try:
        for p in wb_doc['entities'][ii]['claims'][j]:
            i=p["mainsnak"]["datavalue"]['value']['id']
            url = "https://wikidata.org/wiki/Special:EntityData/%s.json" % (i)
            test = json.loads(urllib.urlopen(url).read())
            print '    ', i, '  ', test["entities"][i]['labels']['en']['value']
    except:
        for p in wb_doc['entities'][ii]['claims'][j]:
            if 'datavalue' in p["mainsnak"].keys():
                i = p["mainsnak"]["datavalue"]['value']
                print '   ',i


with open('test0.json', 'w') as outfile:
    json.dump(wb_doc, outfile)