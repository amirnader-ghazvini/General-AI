"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib

api_key = 'AIzaSyDZJzhsKe1B12PbhFg8PeTaEjpx5lcfCV4'
query = 'Beef Tenderloin'
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query,
    'limit': 10,
    'indent': True,
    'key': api_key,
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())

for element in response['itemListElement']:
  print element['result']['name'] + ' (' + str(element['resultScore']) + ')'
  print element['result']['@type']

print str(response)
with open('test.json', 'w') as outfile:  # 000
    json.dump(response, outfile)


feature={
  "extractSyntax": True,
  "extractEntities": True,
  "extractDocumentSentiment": False,
  "extractEntitySentiment": False,
}
