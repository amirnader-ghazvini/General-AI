import json
import csv

with open("session.json") as memory:
    session = json.load(memory)

def upload_em():
    with open("EM.txt") as memory:
        EM = json.load(memory)
    with open("intent_training_data.json") as memory:
        training = json.load(memory)
    for i in EM:
        b=0
        for j in training:
            if i['WM']['Input']==j['sentence']:
                b=1
                if i['WM']['Intents'][0]['Intent']==j['intent']:
                    j['count']+=1
                break
        if b==0:
            training.append({'sentence': i['WM']['Input'], 'count': 1, 'intent': i['WM']['Intents'][0]['Intent']})

    with open('intent_training_data.json', 'w') as outfile:
        json.dump(training, outfile)

def upload_td():
    td=[]
    with open('train_5_3.csv') as csvfile:
        reader = csv.reader(csvfile, skipinitialspace=True)
        for row in reader:
            td.append({'sentence':row[0],"intent":row[1]})
    return td



print upload_td()