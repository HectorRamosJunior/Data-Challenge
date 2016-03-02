#Hector Ramos
#3/1/2016
#Enigma Coding Challenge Part 1
import csv, os

def makeSolution(inputFileName, outputFileName):
    #If solution file already exists, remove it
    if os.path.exists(outputFileName):
        os.remove(outputFileName)

    #Dict reader/writer for flexibility with possible column changes
    reader = csv.DictReader(open(inputFileName))
    writer = csv.DictWriter(open(outputFileName,'wb'), 
                                fieldnames = reader.fieldnames)
    writer.writeheader()

    #O(1) readtime instead of reading from the csv file each time
    stateDict = getStateDict("state_abbreviations.csv")

    #Write the rows to the new file, fixing them along the way
    for row in reader:
        fixedRow = row 
		
		#Fix the dictionary fields as desired
        fixedRow["bio"] = " ".join(fixedRow["bio"].split())
        if fixedRow["state"] in stateDict:
            fixedRow["state"] = stateDict[fixedRow["state"]]

		#Write the modified dictionary as a new row to the output csv
        writer.writerow(fixedRow)


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