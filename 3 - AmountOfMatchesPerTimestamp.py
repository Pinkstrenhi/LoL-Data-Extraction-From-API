# Creates a CSV with the player, puuid and amount of matches per timestamp

import pandas as pd
import requests
import csv
import time

filePathTimestamp = r"Insert here the path to the .csv file where you saved the aimed timestamps"
# In the step 01 example is saved as 'timestampToExtract.csv'

dfTimestamp = pd.read_csv(filePathTimestamp)

filePathPlayer = r"Insert here the path to the .csv file where you saved the aimed players"
# In the step 02 example is saved as 'amountOfMatchesBR.csv'

dfPlayer = pd.read_csv(filePathPlayer,encoding="utf-16")

ApiKey = "Insert here your API key obtained in this site https://developer.riotgames.com"
Directiory = r"Insert here the path to where (Folder) you want to save the .csv file"
FileName = "mappedMatchesBR.csv"

requestPlayer = "/lol/summoner/v4/summoners/by-name/"
requestMatchId = "/lol/match/v5/matches/by-puuid/" 

count = 100
extractionLimit = 0
extractionLimitTotal = 99

def CreateURL(location,requestApi,code,apikey):
    url = "https://" + location + ".api.riotgames.com" + requestApi + code + "api_key=" + apikey
    return url
def RequestInfo(location,requestApi,structure,apikey):
    url = CreateURL(location,requestApi,structure,apikey)
    response = requests.get(url)
    responseStatus = response.status_code
    data = response.json()
    return responseStatus,data
def CreateCSV(filePath,fieldnames):
    with open(filePath, mode="w",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
def UpdateCSV(csvPath,write):
    with open(csvPath, mode="a",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)

weeks = []
        
with open(Directiory + FileName, mode="w",encoding="utf-16", newline="") as csvfile:
    for i in range(1,41):
        weeks.append(f"Week{i}")
    fieldnames = ["Player","Puuid","Region","RegionCode"] + weeks
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    
amountPlayers = 0
for i in range(len(dfPlayer)):
    amountPlayers += 1
    
    if extractionLimit >= extractionLimitTotal:
        print("\nSleep\n")
        time.sleep(extractionLimitTotal)
        extractionLimit = 0
    
    player = dfPlayer["Players"][i]
    region = dfPlayer["Region"][i]
    regionCode = dfPlayer["RegionCode"][i]
    
    responseStatus,playerData = RequestInfo(regionCode,requestPlayer,player + "?",ApiKey)
    
    puuid = playerData["puuid"]
    
    amountOfMatchesPerTimestamp = []
    
    for j in range(len(dfTimestamp)):
        timestampStart = dfTimestamp["TimestampStart"][j]
        timestampEnd = dfTimestamp["TimestampEnd"][j]
        
        responseStatus,matchIdData = RequestInfo(region,requestMatchId,puuid + f"/ids?startTime={timestampStart}&endTime={timestampEnd}&start=0&count=" + str(count) + "&",ApiKey)   
        amountOfMatchesPerTimestamp.append(len(matchIdData))
        extractionLimit += 1
    
    print("-"*60)
    print(f"{amountPlayers}/{len(dfPlayer)}")
    print(f"Player: {player}")
    print(f"Amount: {amountOfMatchesPerTimestamp}")
    print("-"*60)
        
    
    UpdateCSV(Directiory + FileName, [player,puuid,region,regionCode] + amountOfMatchesPerTimestamp)

   
    
    
    
    
    
    
    
    
    
    
    
    