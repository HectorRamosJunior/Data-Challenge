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

    # Get dictionary of state abbrevation full names
    state_dict = get_state_dict("state_abbreviations.csv")

    # List initialized above date_offset() scope for slight efficiency
    # a set could have been used instead, however the list is small
    # and the list holds the order of the months by index
    month_list = ["January", "February", "March", "April", "May", 
                  "June", "July", "August", "September", "October", 
                  "November", "December"]

    # Write the rows from the input to the new file, while 
    # modifying the bio, state and start date fields along the way
    for row in reader:
        fixed_row = row 

        # Fixes the bio field, changes state abrev to full name
        fixed_row["bio"] = " ".join(fixed_row["bio"].split())
        if fixed_row["state"] in state_dict:
            fixed_row["state"] = state_dict[fixed_row["state"]]

        # Gets normalized date string    
        date = date_offset(fixed_row["start_date"], month_list)

        # Handle invalid normalized date
        if not date:
            fixed_row["start_date_description"] = fixed_row["start_date"]
            fixed_row["start_date"] = "Invalid" 
        else:
            fixed_row["start_date"] = date 
            fixed_row["start_date_description"] = ""

        # Write the modified row as a newest row to the output csv
        writer.writerow(fixed_row)


def get_state_dict(file_name):
    """Reads the csv file for the list of state abbreviations and 
    returns a dictionary of the abbrevations and full names of states. 

    Assumes the first column is the abbreviation, second is the name.
    Also assumes there is more than one row in the state csv file.

    Args:
        file_name: The csv file name for the state abbreviations

    Returns:
        Dictionary of state abbreviations as keys, full names as values
    """
    reader = csv.reader(open(file_name, "rb"))
    state_dict = {}

    # To skip the first row (headers)
    reader.next()

    for row in reader:
        state_dict[row[0]] = row[1]

    return state_dict


def date_offset(date, month_list):
    """Normalizes a date string to YYYY-MM-DD. If the date string
    input is invalid, a tuple is returned where the first value
    is set to "Invalid" and the second value holds the original.

    Assumes valid date entries are in the format "<Month> DD, YYYY"
    or in the format "MM/DD/YYYY".

    Args:
        date: The original start_date field from the input csv
        month_list: A list of the months in a year

    Returns:
        Normalized string if valid, None if not valid
    """
    split_by_space = date.split(" ")
    split_by_slash = date.split("/")

    normalized = "" 

    # Detects the format "<Month> DD, YYYY"
    if len(split_by_space) == 3:
        month, day, year = split_by_space
 
        # Handle year
        if year.isdigit():
            normalized += year + "-"
        
        # Handle month
        for i in xrange(len(month_list)):
            if month == month_list[i]:
                #If match is in the first 9 months
                if i + 1 < 10:
                    normalized += "0"
                normalized += str(i+1) + "-"    

        # Handle day
        day = day.replace(",", "")
        if day.isdigit():
            normalized += day

    # Detects the format: "MM/DD/YYYY"
    if len(split_by_slash) == 3:
        month, day, year = split_by_slash
        
        # Handle year
        if year.isdigit():
            normalized += year + "-"
        
        # Handle month
        if month.isdigit():
            normalized += month + "-"   

        # Handle day
        if day.isdigit():
            normalized += day


    # Checks if date was properly normalized
    if len(normalized) != 10:
        return None
    return normalized


make_solution("test.csv", "solution.csv")