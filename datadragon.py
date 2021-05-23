import urllib.request
import urllib.parse
import urllib.error
import ssl
import json
import sys
import csv

url = 'http://ddragon.leagueoflegends.com/cdn/11.4.1/data/en_US/champion.json'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

connection = urllib.request.urlopen(url, context=ctx)
data = connection.read().decode()
championRawData = json.loads(data)
#print(json.dumps(js, indent=4))
#headers = dict(connection.getheaders())
# for k,v in headers.items():
# print(k,':',v)
crd = championRawData['data']
allchamps = list()
allchamps = [["champName", "champID",
              "ADbase", "FMS", "ASPL", "ASOS", "Title"]]
for champ in crd:
    name = crd[champ]['id']
    champID = crd[champ]['key']
    ADbase = crd[champ]['stats']['attackdamage']
    ADpl = crd[champ]['stats']['attackdamageperlevel']
    FMS = crd[champ]['stats']['movespeed']
    ASPL = crd[champ]['stats']['attackspeedperlevel']
    ASOS = crd[champ]['stats']['attackspeed']
    Title = crd[champ]['title']
    row = [name, champID, ADbase, FMS, ASPL, ASOS, Title]
    allchamps.append(row)
with open('champs2.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(allchamps)
print('Done, open champs.csv')
