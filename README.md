# LoL-Data-Extraction-From-API

The code in this repository is divided in 04 steps that make it possible to extract data from League of Legends (LoL) API, according to determined timestamps. 

Step 01 - Timestamps.py

This code returns a .csv file with all the timestamps you aim to extract data, to be used in further steps and avoid repetitions. 

What must be changed: 
* In the dictionary (timestamps) you will set the keys to correspond to the timestamp, in the example is divided per week of the year. The attributed values will correspond to when you want to start and end the extraction, the date must be converted in epoch/unix timestamp as seconds. 
Example: 
* "week01" : ["1672628460","1673233199"]
* It is the first week of the analyzed year (2023), and the extraction of this week will start on January 2nd (1672628460) and end on January 8th (1673233199), according to Brazilian time.  
* You will have to provide a folder (directory) where the .csv file will be saved in your computer. 

Step 02 - PlayersUsersAndRegions.py

This code will take your imputed players, using its Summoner’s Names, and save their regions name and code, to be used in further steps and avoid repetitions. 

What must be changed: 
* After naming your players list as you want, “playersBR” in the example, you will fill it with all the players you aim to extract, using their LoL usernames (Summoner’s Names). This list only supports players from a single region. If you are dealing with a multi-region situation, other lists should be created, and then merged after mapped. 
* You will have to provide a folder (directory) where the .csv file will be saved in your computer. 

Step 03 - AmountOfMatchesPerTimestamp.py

This code will map the amount of matches all the provided players (step 02) played in the determined timestamps (step 01). Which is useful to analyze how often a player plays and to know how many matches will be extracted per player and timestamp. 

What must be changed: 
* It is necessary to provide the path where you saved the .csv file with all aimed timestamps (filePathTimestamp), defined in step 01. And the path for the .csv file with all aimed players (filePathPlayer), defined in step 02. 
* You will have to provide a folder (directory) where the .csv file will be saved in your computer. 
* In “ApiKey”, you will insert your developer key, which can be obtained in the Riot Games Developer Website (https://developer.riotgames.com), by creating a developer account for free. 

Step 04 - DataExtraction.py

This code will extract data from players and matches, considering the provided timestamps (step 01). It will save data from the provided player and his/hers teammates, totalizing 10 data per match, in Summoner’s Rift mode. 

What must be changed: 
* It is necessary to provide the path where you saved the .csv file with all aimed timestamps (filePathTimestamp), defined in step 01.
Provide the path to where you saved the .csv file with player amount of matches information (filePath), defined in step 03.
* In “ApiKey”, you will insert your developer key, which can be obtained in the Riot Games Developer Website (https://developer.riotgames.com), by creating a developer account for free. 
* You will have to provide a folder (directory) where the .csv file will be saved in your computer. 
* In “playerActions”, insert all player in-game actions you want to extract, such as Kills, Deaths and Assists. If an action belongs to a directory inside the main one, you can use a structure like in “playerActionsChallange”. 
* “playerInfo” will extract data from a dictionary associated with the player, inside the API, and can be modified to extract more or less information. 

Attention Points: 
* All “request” variables, such as “requestPlayer” and “requestMatchId”, follow the API structure of request. They are set to work with the structure of 2023. It is important to check the API (https://developer.riotgames.com/apis) to make sure they are the same, and if they are not, to do the proper changes for the API version you are using. 
* If there are less than 10 data per match, it belongs to another game mode. Like 5 players in a Summoner’s Rift - Coop vs AI.   
* Variable “last” can be used if the code breaks during an extraction, because of the key expiration or a connection (Internet) issue. 
* * In this case, it is necessary to change the variable to True. Change “lastAmountOfExtractions” to the last timestamp it was being extracted, considering the code counting that starts at 0. 
* * Example: Break in week 22, you will change “lastAmountOfExtractions” to 21
* Variables named “limit” are used to fulfill API limitations, such as amount of requests per time. They will make the code sleep per a few seconds (70 seconds in the example) before continuing the extraction. 
