"""Hector Ramos
3/1/2016
Enigma Coding Challenge Part 1
"""
import csv
import os

def make_solution(input_file_name, output_file_name):
    """Creates a new csv file which if a modified version of the input. 
    The bio field's padding is removed, the state abbreviation is 
    changed to its full name and the start date is normalized.

    Deletes the old output file if it exists and creates a new one.

    Args:
        input_file_name: The filename for the input csv file
        output_file_name: The filename for the desired output csv file

    Returns:
        None
    """
    # If solution file already exists, remove it
    if os.path.exists(output_file_name):
        os.remove(output_file_name)

    # Dict reader/writer for flexibility with possible column changes
    reader = csv.DictReader(open(input_file_name))

    writer_header = reader.fieldnames
    writer_header.append("start_date_description")
    writer = csv.DictWriter(open(output_file_name, "wb"), 
                            fieldnames = writer_header)
    writer.writeheader()

    # O(1) readtime instead of reading from the csv file each time
    state_dict = get_state_dict("state_abbreviations.csv")

    # List initialized above date_offset() scope for slight efficiency
    # a set could have been used instead, however the list is small
    # and the list holds the order of the months by index
    month_List = ["January", "February", "March", "April", "May", 
                "June", "July", "August", "September", "October", 
                "November", "December"]

    # Write the rows from the input to the new file, while 
    # modifying the bio, state and start date fields along the way
    for row in reader:
        fixed_row = row 
		# Fixes the bio field, changes state abrev to full name using dict
        fixed_row["bio"] = " ".join(fixed_row["bio"].split())
        if fixed_row["state"] in state_dict:
            fixed_row["state"] = state_dict[fixed_row["state"]]

        # Sets the start date fields from the tuple in the function    
        date, date_description = date_offset(fixed_row["start_date"], 
                                            month_List)

        fixed_row["start_date"] = date 
        fixed_row["start_date_description"] = date_description

		# Write the modified row as a newest row to the output csv
        writer.writerow(fixed_row)


# Returns a dictionary of the state abbreviations for O(1) runtime
def get_state_dict(file_name):
    """Reads the csv file for the list of state abbreviations and 
    returns a dictionary of the abbrevations and full names of states. 

    Args:
        file_name: The csv file name for the state abbreviations.

    Returns:
        Dictionary of state abbreviations as keys, full names as values.
    """
    reader = csv.reader(open(file_name, "rb"))
    state_dict = {}

    # bool to skip the first row(headers)
    header = True 

    for row in reader:
        if header:
            header = False
            continue

        state_dict[row[0]] = row[1]

    return state_dict

# Returns a tuple for the start date fields, catches errors in start date
def date_offset(date, month_list):
    """Reads the csv file for the list of state abbreviations and 
    returns a dictionary of the abbrevations and full names of states. 

    Args:
        date: The csv file name for the state abbreviations.

    Returns:
        Dictionary of state abbreviations as keys, full names as values.
    """
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