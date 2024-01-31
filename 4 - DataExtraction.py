# Data extraction

import pandas as pd
import requests
import csv
import time
import datetime
import os
import sys

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
def FolderPath(directory,pathName):
    path = directory + pathName
    if not os.path.exists(path):
        os.mkdir(path)
    return path
def ExtractionStructure(last,pathName,player,csvFormat):
    if last:
        csvName = f"{pathName}{player}_{csvFormat}_Last.csv"
    else: 
        csvName = f"{pathError}{player}{csvFormat}.csv"
    return csvName

filePathTimestamp = r"Insert here the path to the .csv file where you saved the aimed timestamps"
# In the step 01 example is saved as 'timestampToExtract.csv'
dfTimestamps = pd.read_csv(filePathTimestamp)

last = False
lastAmountOfExtractions = 31
if last:
    filePath = r"Insert here the path to .csv file with the player informations"
    # Use this 'last' structure to continue the extraction of a player that was interrupted because of API limitations
    # (such as the key having expired) or Internet connection issues
else:
    filePath = r"Insert here the path to .csv file with all mapped players informations"
    # In the step 03 example is saved as 'mappedMatchesBR.csv'

df = pd.read_csv(filePath,sep=",",encoding="utf-16")

ApiKey = "Insert here your API key obtained in this site https://developer.riotgames.com"
Directiory = r"Insert here the path to where (Folder) you want to save all extractions"

FileName = "extractedPlayer"
DateFormat = "%Y-%m-%d"
DateTimeFormat = "%Y-%m-%d %H:%M:%S"

requestPlayer = "/lol/summoner/v4/summoners/by-name/"
requestMatchId = "/lol/match/v5/matches/by-puuid/" 
requestMatchInfo = "/lol/match/v5/matches/"

playerActions = ["assists","deaths","kills","win"]

# If you need to extract information from any dictionary inside the player actions main one (such as the Challenge dictionary)
playerActionsChallenge = ["abilityUses","baronTakedowns",
"completeSupportQuestInTime","controlWardsPlaced","deathsByEnemyChamps","wardsGuarded"]

playerInfo = ["region","regionCode","puuid","accountId","matchId","gameCreation","gameDuration","gameStartTimestamp","gameEndTimestamp",
              "gameEndTimestampToDate","gameMode","gameType","platformId"]

extraxtedLimit = 99
limit = 0
count = 100
limitTime = 70
amountPlayers = 0
allMatches = 0

weeks = []
weeksTimeStart = []
weeksTimeEnd = []

timeStart = time.time()
for i in range(len(df)):
    player = df["Player"][i]
    region = df["Region"][i]
    regionCode = df["RegionCode"][i]
    time.sleep(limitTime)
    print("Sleep between players")
    timeStartPlayer = time.time()
    
    amountPlayers += 1
    
    playerPuuid = df["Puuid"][i]
    
    # Create Folders to store data
    pathAllPlayers = FolderPath(Directiory,"Players/")
    pathPlayer = FolderPath(Directiory,f"Players/{player}/")
    pathError = FolderPath(Directiory,"Errors/")
    pathMatches = FolderPath(Directiory,"Matches/")
    
    # CSV Errors
    csvNameError = ExtractionStructure(last,pathError,player,"Error")
    CreateCSV(csvNameError,["player","matchId","error"])

    # CSV No Matches
    csvNameNoMatches = ExtractionStructure(last,pathError,player,"NoMatches")
    CreateCSV(csvNameNoMatches,["player","timestampStart","timestampEnd"])
    
    #CSV Matches
    csvNameMatches = ExtractionStructure(last,pathMatches,player,"Matches")
    CreateCSV(csvNameMatches,["player","timestampStart","timestampEnd","matchesAmount","matches"])
    
    if last: 
        rangeTimestamp = range(lastAmountOfExtractions,len(dfTimestamps),1)
    else:
        rangeTimestamp = range(len(dfTimestamps))
    
    for j in rangeTimestamp:        
        timestampStart = dfTimestamps["TimestampStart"][j]
        timestampEnd = dfTimestamps["TimestampEnd"][j]
        
        csvName = f"{pathPlayer}{timestampStart}_{timestampEnd}.csv"
        CreateCSV(csvName,playerInfo + playerActions + playerActionsChallenge)
        
        responseStatusIdMatch,matchIdData = RequestInfo(region,requestMatchId,playerPuuid + f"/ids?startTime={timestampStart}&endTime={timestampEnd}&start=0&count=" + str(count) + "&",ApiKey)
        if responseStatusIdMatch != 200: 
            print("API Error")
            print("-"*30)
            print(f"Player: {player}")
            print(f"Timestamp: {timestampStart}/{timestampEnd}")
            print("-"*30)
            print("Exiting Application\n")
            
            sys.exit()
            
        if len(matchIdData) > 0: 
            print(f"Matches for this timestamp: {matchIdData}")
            UpdateCSV(csvNameMatches,[player,timestampStart,timestampEnd,len(matchIdData),matchIdData])
            
            for matchId in matchIdData:
                if limit >= extraxtedLimit:
                    print(f"\nCount Match: {limit}\nSleep between matches")
                    time.sleep(limitTime)
                    print("Returning\n")
                    timeStartPlayer = time.time()
                    limit = 0
                 
                actionsHolder = {}
                participantIndex = 0
                
                responseStatusMatch,matchData = RequestInfo(region,requestMatchInfo,matchId + "?",ApiKey)
                if responseStatusMatch != 200: 
                    print("API Error")
                    print("-"*30)
                    print(f"Player: {player}")
                    print(f"Timestamp: {timestampStart}/{timestampEnd}")
                    print("-"*30)
                    print("Exiting Application\n")
                    
                    sys.exit()
                try:
                    for participant in matchData["metadata"]["participants"]:
                        participantIndex += 1
                        if participant == playerPuuid:
                                print("-"*30)
                                print("Match Info")
                                print("-"*30)
                                print("MatchId:" + str(matchId))
                                print("GameCreation:" + str({matchData["info"]["gameCreation"]}))
                                print("GameStartTimestamp:" + str({matchData["info"]["gameDuration"]}))
                                print("GameEndTimestamp:" + str({matchData["info"]["gameStartTimestamp"]}))
                                print("GameCreation:" + str({matchData["info"]["gameEndTimestamp"]}))
                                print("-"*30)
                                print("\n")
                                
                                endTimestamp = matchData["info"]["gameEndTimestamp"] /1000
                                endTimestampToDatetime = datetime.datetime.fromtimestamp(endTimestamp)
                                endTimestampToDate = endTimestampToDatetime.strftime(DateFormat)
                                
                                for index, value in enumerate(matchData["info"]["participants"]):
                                    responseStatus,playerDataMatch = RequestInfo(matchData["info"]["platformId"],requestPlayer,matchData["info"]["participants"][index]["summonerName"]+ "?",ApiKey)
                                    
                                    for action in playerActions:
                                        if action in matchData["info"]["participants"][index].keys():
                                            actionsHolder[action] = matchData["info"]["participants"][index][action]
                                    for action in playerActionsChallenge:
                                        if action in matchData["info"]["participants"][index]["challenges"].keys():
                                            actionsHolder[action] = matchData["info"]["participants"][index]["challenges"][action]
                                            
                                    data = []
                                    
                                    for index,value in actionsHolder.items():
                                        data.append(value)
                                        
                                    with open(csvName, mode="a",encoding="utf-16", newline="") as csvfile:
                                        writer = csv.writer(csvfile) 
                                        
                                        if responseStatus != 200:
                                            playerToWritePuuid = "Player Not Found"
                                            playerToWriteAccount = "Player Not Found"
                                        else:
                                            playerToWritePuuid = playerDataMatch["puuid"]
                                            playerToWriteAccount = playerDataMatch["accountId"]
                                            
                                        
                                        writer.writerow([
                                                            region,
                                                            regionCode,
                                                            playerToWritePuuid,
                                                            playerToWriteAccount,
                                                            matchId,
                                                            matchData["info"]["gameStartTimestamp"],
                                                            matchData["info"]["gameDuration"],
                                                            matchData["info"]["gameStartTimestamp"],
                                                            matchData["info"]["gameEndTimestamp"],
                                                            endTimestampToDate,
                                                            matchData["info"]["gameMode"],
                                                            matchData["info"]["gameType"],
                                                            matchData["info"]["platformId"]] 
                                                        + data)
                                        
                                        allMatches += 1
                                        limit += 1
                                        
                                        print(f"Player: {player}")
                                        print(f"Extracted Matches in Total: {allMatches}")
                                        print(f"Count Match for API Limit: {limit}\n")
                                        
                except KeyError as e: 
                    UpdateCSV(csvNameError,[player,matchId,e])
                        
                    print(f"KeyError: {e} not found")
                    print("Moving to next match\n")
                timeEndPlayer = time.time()
                timeTotalPlayer = timeEndPlayer - timeStartPlayer
                print(f"Total Per Player: {timeTotalPlayer/60} minutes")
        else:
            UpdateCSV(csvNameNoMatches,[player,timestampStart,timestampEnd])
            print(f"No match found in this timestamp: {timestampStart}/{timestampEnd}\n")
    
timeEnd = time.time()
timeTotal = timeEnd - timeStart
print(f"Total Time: {timeTotal/60} minutes")  