## Creates a CSV with the players to be extracted

import os
import csv

csvName = "playersToExtractBR.csv"
directory = r"Insert here the path to where (Folder) you want to save the .csv file"

def CreateCSV(filePath,fieldnames):
    with open(filePath, mode="w",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
def UpdateCSV(csvPath,write):
    with open(csvPath, mode="a",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)
def PlayersDictionary(playersList,regionCode):
    players = {}
    for player in playersList:
        players[player] = [regionCode[0],regionCode[1]]
    return players

regionCodes = {
                    "Brazil":["BR1","AMERICAS"],
                    "EuropeNordicAndEast":["EUN1","EUROPE"],
                    "EuropeWest":["EUW1","EUROPE"],
                    "Japan":["JP1","ASIA"],
                    "RepublicOfKorea":["KR","ASIA"],
                    "LatinAmericaNorth":["LA1","AMERICAS"],
                    "LatinAmericaSouth":["LA2","AMERICAS"],
                    "NorthAmerica":["NA1","AMERICAS"],
                    "Oceania":["OC1","SEA"],
                    "Turkey":["TR1","EUROPE"],
                    "Russia":["RU","EUROPE"],
                    "ThePhilippines":["PH2","SEA"],
                    "SingaporeMalaysiaAndIndonesia":["SG2","SEA"],
                    "TaiwanHongKongAndMacao":["TW2","SEA"],
                    "Thailand":["TH2","SEA"],
                    "Vietnam":["VN2","SEA"]
              }

# Add to the list all summoner names you aim to extract
playersBR = [
              "Robo","Aegis"              
            ]

CreateCSV(os.path.join(directory,csvName),["Players","RegionCode","Region"])

playersDictionaryBR = PlayersDictionary(playersBR,regionCodes["Brazil"])

for key,values in playersDictionaryBR.items():
    UpdateCSV(os.path.join(directory,csvName),[key,values[0],values[1]])