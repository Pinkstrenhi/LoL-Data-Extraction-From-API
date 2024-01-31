## Creates CSV with timestamps to extract

import os
import csv
import datetime

timestamps = {
    "week01" : ["1672628460","1673233199"],
    "week02" : ["1673233260","1673837999"],
    "week03" : ["1673838060","1674442799"],
    "week04" : ["1674442860","1675047599"],
    "week05" : ["1675047660","1675652399"]
}

csvName = "timestampToExtract.csv"
directory = r"Insert here the path to where (Folder) you want to save the .csv file"
DateFormat = "%Y-%m-%d"

def CreateCSV(filePath,fieldnames):
    with open(filePath, mode="w",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
def UpdateCSV(csvPath,write):
    with open(csvPath, mode="a",encoding="utf-16", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)
def TimestampToDate(timestamp):
    timestampToDate = int(timestamp)
    timestampToDatetime = datetime.datetime.fromtimestamp(timestampToDate)
    timestampToDate = timestampToDatetime.strftime(DateFormat)
    
    return timestampToDate
        
CreateCSV(os.path.join(directory,csvName),["Week","TimestampStart","TimestampEnd","DateStart","DateEnd"])

for key,values in timestamps.items():
    timestampStart = values[0]
    timestampEnd   = values[1]
    
    timestampToDateStart = TimestampToDate(timestampStart)
    timestampToDateEnd = TimestampToDate(timestampEnd)
    
    UpdateCSV(os.path.join(directory,csvName),[
                                                key,
                                                timestampStart,
                                                timestampEnd,
                                                timestampToDateStart,
                                                timestampToDateEnd
                                              ])