#Hector Ramos
#3/1/2016
#Enigma Coding Challenge Part 1
import csv, os

def makeSolution(inputFileName, outputFileName):
    #If solution file already exists, remove it
    if os.path.exists(outputFileName):
        os.remove(outputFileName)

    #Dict assumes the column names or placement subject to change
    inputReader = csv.DictReader(open(inputFileName))
    writer = csv.DictWriter(open(outputFileName,'wb'), 
                                fieldnames = inputReader.fieldnames)
    writer.writeheader()

    #O(1) readtime instead of reading the csv file each time
    stateDict = getStateDict("state_abbreviations.csv")

    #Write the rows to the new file, fixing them along the way
    for row in inputReader:
        fixedRow = row 
        fixedRow["bio"] = getCleanString(fixedRow["bio"])
        
        if fixedRow["state"] in stateDict:
            fixedRow["state"] = stateDict[fixedRow["state"]]

        writer.writerow(fixedRow)


def getCleanString(string):
    return "test"

def getStateDict(fileName):
    reader = csv.reader(open(fileName, "rb"))
    stateDict = {}

    header = True #bool to skip the first row(headers)

    for row in reader:
        if header:
            header = False
            continue

        stateDict[row[0]] = row[1]

    return stateDict



makeSolution("test.csv", "solution.csv")




