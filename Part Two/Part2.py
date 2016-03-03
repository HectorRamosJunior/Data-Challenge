"""Hector Ramos
3/2/2016
Enigma Coding Challenge Part 2
"""
import json, urllib
from bs4 import BeautifulSoup

def scrapeData(mainURL):
    """
        Iterates through the pages of the mainurl to get the 
        company url/data
    """
    companyDict = {}
    next = "" # placeholder for iterating through the pages

    while True:
        page = urllib.urlopen(mainURL + next).read()
        soup = BeautifulSoup(page, "html.parser")

        # Parses for all the companies on the webpage and the urls
        companyPageURLs = soup.find("table").findAll("a")

        for a in companyPageURLs:
            name = str(a.text.lstrip()) # Unicode object
            data = getCompanyData(mainURL + a["href"])

            # Updates dictionary with the new company entry
            companyDict[name] = data 

        # Checks if the next page tag doesn't exist.
        if soup.find("li", class_="next disabled"):
            break

        # If the next page exists, move onto the next page
        next = soup.find("li", class_= "next").find("a").get("href")
        print "Moving onto page " + mainURL + next

    json.dump(companyDict, open("solution.json", "w"))


# Returns dictionary of parsed data from the company page
def getCompanyData(companyURL):
    """
        Returns dictionary of parsed data from the company page
    """
    page = urllib.urlopen(companyURL).read()
    soup = BeautifulSoup(page, "html.parser")

    dataDict = {}

    tds = soup.findAll("td")
    for td in tds:
        if td.has_attr("id"):
            dataDict[str(td.get("id"))] = str(td.text) # Unicode objects
    
    return dataDict

scrapeData("http://data-interview.enigmalabs.org")
