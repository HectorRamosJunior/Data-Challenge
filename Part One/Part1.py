""" Hector Ramos
3/1/2016
Enigma Coding Challenge Part 1
"""
import csv, os

def makeSolution(inputFileName, outputFileName):
    # If solution file already exists, remove it
    if os.path.exists(outputFileName):
        os.remove(outputFileName)

    # Dict reader/writer for flexibility with possible column changes
    reader = csv.DictReader(open(inputFileName))

    writerHeader = reader.fieldnames
    writerHeader.append("start_date_description")
    writer = csv.DictWriter(open(outputFileName,'wb'), 
                            fieldnames = writerHeader)
    writer.writeheader()


    # O(1) readtime instead of reading from the csv file each time
    stateDict = getStateDict("state_abbreviations.csv")

    # List initiatilized above dateOffset() scope for slight efficiency
    # A set could have been used instead, however the scope is small
    # And the list holds the order of the months by index
    monthList = ["January", "February", "March", "April", "May", 
                "June", "July", "August", "September", "October", 
                "November", "December"]


    # Write the rows to the new file, fixing them along the way
    for row in reader:
        fixedRow = row 
		
		# Fixes the bio field, changes state abrev to full name using dict
        fixedRow["bio"] = " ".join(fixedRow["bio"].split())
        if fixedRow["state"] in stateDict:
            fixedRow["state"] = stateDict[fixedRow["state"]]

        # Sets the start date fields from the tuple in the function    
        date, date_description = dateOffset(fixedRow["start_date"], 
                                            monthList)

        fixedRow["start_date"] = date 
        fixedRow["start_date_description"] = date_description

		# Write the modified dictionary as a new row to the output csv
        writer.writerow(fixedRow)


# Returns a dictionary of the state abbreviations for O(1) runtime
def getStateDict(fileName):
    reader = csv.reader(open(fileName, "rb"))
    stateDict = {}

    # bool to skip the first row(headers)
    header = True 

    for row in reader:
        if header:
            header = False
            continue

        stateDict[row[0]] = row[1]

    return stateDict

# Returns a tuple for the start date fields, catches errors in start date
def dateOffset(date, monthList):
    spaced = date.split()
    slashed = date.split("/")

    # To be normalized to "YYYY-MM-DD"
    normalized = "" 

    if len(spaced) == 3:
        # Valid Dates to be normalized: "June 26, 1977"  
        
        # YYYY-
        if spaced[2].isdigit():
            normalized += spaced[2] + "-"
        
        # MM-
        for i in xrange(len(monthList)):
            if spaced[0] == monthList[i]:
                if i+1 < 10:
                    normalized += "0"
                normalized += str(i+1) + "-"    

        # DD
        spaced[1] = spaced[1].replace(",", "")
        if spaced[1].isdigit():
            normalized += spaced[1]

    if len(slashed) == 3:
        # Valid Dates to be normalized: "10/27/1998"
        
        # YYYY-
        if slashed[2].isdigit():
            normalized += slashed[2] + "-"
        
        # MM-
        if slashed[0].isdigit():
            normalized += slashed[0] + "-"   

        # DD
        if slashed[1].isdigit():
            normalized += slashed[1]


    # Checks if date was properly normalized
    if len(normalized) != 10:
        return "Invalid", date
    return normalized, ""


makeSolution("test.csv", "solution.csv")