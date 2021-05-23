from riotwatcher import LolWatcher, ApiError
from apikey import api_key, watcher
from apikey import my_region as euw
import json
import requests
import datetime
import sys
import csv

# ChampionID to Names
response = requests.get(
    'http://ddragon.leagueoflegends.com/cdn/11.4.1/data/en_US/champion.json')
cdr = json.loads(response.text)

champs = {}
for key, champion in cdr['data'].items():
    champs[int(champion['key'])] = champion['name']


while True:
    acct = input('Enter Account Name: ')
    if acct == 'quit':
        quit()
    if acct == '':
        acct = 'da3orD'
    print('Searching for', acct)
    print(acct, 'Found!')
    print('Retreivng data from Riot API')
    me = watcher.summoner.by_name(euw, acct)
    # for debugging
    headers1 = json.dumps(me, indent=4)
    # print(headers1)
    print('Retrieved!', len(headers1), 'characters')
    print('Name:', me['name'])
    print('Level:', me['summonerLevel'])
    print('ID:', me['id'])
    AccId = me['accountId']
    print('encryptedID: ', AccId)
    print('=================================================')
    break
while True:
    end_index = input('How Many Matches? ')
    if end_index == 'quit':
        break
    else:
        pass
    try:
        end_index = int(end_index)
        pass
    except:
        print('Error Please Enter Nurmeric Input')
        continue

    match_list = watcher.match.matchlist_by_account(
        euw, AccId, set([400]), None, None, 0, end_index)
    # for debugging match_list.json
    headers = json.dumps(match_list, indent=4)
    # print(headers)

    # List for csv file output
    myList = list()
    print('Retreivng Last', end_index, 'matches', 'for', acct)
    print('Retrieved!', len(headers), "characters")
    print('=================================================')
    count = 0
    for u in match_list['matches']:
        count = count + 1
        GameID2 = u['gameId']
        timestamp = str(u['timestamp'])
        lane = u['lane']

        # Time
        exactTimeHook = int(timestamp[:10])
        exactTime = datetime.datetime.fromtimestamp(exactTimeHook)


        # Match Deatil Json, match_detail.json
        match_detail = watcher.match.by_id(euw, GameID2)

        # Dangerous code stil checking reliability
        for row in match_detail['participants']:
            for k, v in row.items():
                if u['champion'] is v:
                    kills = row['stats']['kills']
                    deaths = row['stats']['deaths']
                    assists = row['stats']['assists']
                    damageDealt = row['stats']['totalDamageDealtToChampions']
                    patriparticipantID = row['participantId']
                    minions1 = row['stats']['totalMinionsKilled']
                    minions4 = row['stats']['neutralMinionsKilled']
                    minions = minions1 + minions4
                    goldEarned = row['stats']['goldEarned']
                    win = row['stats']['win']
                    dataList = list()
                    row1 = [kills,deaths,assists,minions,goldEarned,lane]
                    myList.append(row1)
                    if win is True:
                        win = 'Won'
                    else:
                        win = 'Lost'
        # to exchange champID to name
        champName = u['champion']
        if champName in champs:
            champName1 = champs[champName]
        print('Game' + str(count))
        print(exactTime)
        print(win)
        print('GameID:', u['gameId'])
        print('Champion Name:', champName1)
        print('Lane:',lane)
        print('KDA:', str(kills) + '/' + str(deaths) + '/' + str(assists))
        print('Damage Dealt:', damageDealt)
        print('Creep Score:', minions)
        print('Gold Earned:', goldEarned)
        print('=================================================')
    break
#with open('champs1.csv', 'w') as f:
    #writer = csv.writer(f)
    #writer.writerows(dataList)
#print('Done, open champs1.csv')
print(myList)
