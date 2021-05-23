from riotwatcher import LolWatcher, ApiError
from apikey import api_key, watcher
from apikey import my_region as euw
import json
import requests
import datetime
import csv
import pandas as pd
import time
# ChampionID to Names
response = requests.get(
    'http://ddragon.leagueoflegends.com/cdn/11.4.1/data/en_US/champion.json')
cdr = json.loads(response.text)
# Creating Champs Dict{}
champs = {}
for key, champion in cdr['data'].items():
    champs[int(champion['key'])] = champion['name']
while True:
    acct = input('Enter Account Name: ')
    if acct == 'quit' or acct == 'exit':
        quit()
    elif acct == "":
        print("This input can't be empty.")
        continue
    print('Searching for', acct)
    try:
        account_data = watcher.summoner.by_name(euw, acct)
    except ApiError as err:
        if err.response.status_code == 404:
            print(acct, 'Not found!')
            continue
        elif err.response.status_code == 429:
            print('Error 429', 'Tryting to reconnect...')
    print(acct, 'Found!')
    print('Retreivng data from Riot API........')
    print('Name:', account_data['name'])
    print('Level:', account_data['summonerLevel'])
    account_id = account_data['accountId']
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
    try:
        match_list = watcher.match.matchlist_by_account(
            euw, account_id, set([400]), None, None, 0, end_index)
    except ApiError as err:
        if err.response.status_code == 429:
            print('Error 429 Too many requests\nRetrying...')
    # list for csv_file
    game_stats_list = [[
        "GameNo", "Date", "MatchResult", "ChampionName",
        "Lane", "Kills", "Deaths", "Assists", "Damage", "CS", "Gold"
    ]]
    print('Retreivng Last', end_index, 'matches', 'for', acct)
    print('=================================================')
    # Games counter Game1 Game2 Game .... so on
    count = 0
    for match in match_list['matches']:
        count = count + 1
        game_id = match['gameId']
        lane = match['lane']
        timestamp = str(match['timestamp'])
        m_time = int(timestamp[:10])
        exact_time = datetime.datetime.fromtimestamp(m_time)
    # to exchange champ_id to name
    # Where champs is created dict{} that has k ,v for each champ_id and name
        champ_id = match['champion']
        if champ_id in champs:
            champ_name = champs[champ_id]
    # Match Deatils API(kills,deaths,etc) matchdetails.json
        try:
            match_detail = watcher.match.by_id(euw, game_id)
        except ApiError as err:
            if err.response.status_code == 429:
                print('Error 429 Too many requests\nRetrying...')
    # Fetching specific participant's details algorithm
    # For more details check "json-files/match_detail.json"
        for row in match_detail['participants']:
            for k, v in row.items():
                if champ_id is v:
                    kills = row['stats']['kills']
                    deaths = row['stats']['deaths']
                    assists = row['stats']['assists']
                    damageDealt = row['stats']['totalDamageDealtToChampions']
                    minions1 = row['stats']['totalMinionsKilled']
                    minions4 = row['stats']['neutralMinionsKilled']
                    minions = minions1 + minions4
                    goldEarned = row['stats']['goldEarned']
                    win = row['stats']['win']
                    if win is True:
                        win = 'Won'
                    else:
                        win = 'Lost'
    # Creating list for the fetched data
                    fetched_data_row = [
                        str(count), exact_time, win, champ_name, lane, kills,
                        deaths, assists, damageDealt, minions, goldEarned
                    ]
                    game_stats_list.append(fetched_data_row)
        print('Game' + str(count), 'Retrieved')
    break
# Make csv_file using game_stats_list
csv_file = acct + '.csv'
with open(csv_file, 'w') as f:
    writer = csv.writer(f)
    try:
        writer.writerows(game_stats_list)
    except:
        quit()
print('Generating Report.....')
time.sleep(0.4)
# Calculating average using pandas lib
df = pd.read_csv(csv_file)
print(df)
print('==============================================')
# Creating win counter that will be used for win percentage.
win_count = 0
match_count = end_index
for match_result in df['MatchResult']:
    if match_result == 'Won':
        win_count += 1
percentage = win_count / match_count * 100
average_damage = df['Damage'].mean()
average_kills = df['Kills'].mean()
average_deaths = df['Deaths'].mean()
average_assists = df['Assists'].mean()
average_gold = df['Gold'].mean()
average_cs = df['CS'].mean()
print('Win Percentage:', str(percentage) + '%')
print("Average Damage Dealt:", average_damage)
print('KDA:', str(average_kills) + '/' +
      str(average_deaths) + '/' + str(average_assists))
print("Average Gold Earned:", average_gold)
print("Average CS:", average_cs)
print("Saving data to csv file.......")
print('Data has been saved to', csv_file)
