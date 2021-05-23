import requests
import json
response = requests.get('http://ddragon.leagueoflegends.com/cdn/11.4.1/data/en_US/champion.json')
cdr = json.loads(response.text)

championIdtoName = {}
for key,champion in cdr['data'].items():
    championIdtoName[int(champion['key'])] = champion['name']
