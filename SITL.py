#import csv

def readSITLData(file):
    with open(file, "r") as SITLdata:
        for line in SITLdata:
            line_Str=SITLdata.readline()
            lineList = line_Str.strip().split(",")
            yield lineList
    