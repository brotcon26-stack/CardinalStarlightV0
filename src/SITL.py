#import csv

def readSITLData(file):
    with open(file, "r") as SITLdata:
        #reader = csv.reader(SITLdata)
        #next(reader)
        #for row in reader:
            #yield row
        for line in SITLdata:
            line_Str=SITLdata.readline()
            lineList = line_Str.strip().split(",")
            yield lineList
    