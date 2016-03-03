"""Hector Ramos
3/2/2016
Enigma Coding Challenge Part 2
"""
import json
import urllib
from bs4 import BeautifulSoup


def scrape_company_data(base_url, output_file_name):
    """Scrapes the data of each company page from the given website and 
    stores it into a json file with the desired output file name.

    This assumes the webpage data is structured like the data set at 
    http://data-interview.enigmalabs.org. 
    
    Prints the current page it's scraping from.

    Args:
        base_url: The base website url to scape data from
        output_file_name: The filename for the desired output json file

    Returns:
        None
    """
    company_dict = {}
    page_index = "" # First page index is the base url
    next_page = True

    while next_page:
        full_page_url = base_url + page_index
        print "Scraping data from page %s" % (full_page_url)

        page = urllib.urlopen(base_url + page_index).read()
        soup = BeautifulSoup(page, "html.parser")

        # Parses for all the companies a tags in the table on the page
        company_urls = soup.find("table").findAll("a")

        # Scrapes the data from each company page, adds to company_dict
        for a in company_urls:
            company_name = str(a.text.lstrip())
            company_data = get_company_data(base_url + a["href"])

            # Enter new company data into dictionary
            company_dict[company_name] = company_data 

        # Ends the loop if the next page doesn't exist
        if soup.find("li", class_="next disabled"):
            next_page = False

        # Get next page index
        page_index = soup.find("li", class_= "next").find("a").get("href")

    # Export company dictionary data into a json file
    json.dump(company_dict, open(output_file_name, "w"))


def get_company_data(company_url):
    """Scrapes the data of the given company page and returns a dict
    of the data in the table tag.

    Assumes the the desired data in the table has id tags.

    Args:
        company_url: The company webpage url location

    Returns:
        Dictionary of the company data on the given webpage
    """
    page = urllib.urlopen(company_url).read()
    soup = BeautifulSoup(page, "html.parser")

    data_dict = {}

    # Assumes desired information in the html table has an id attr
    tds = soup.findAll("td")
    for td in tds:
        if td.has_attr("id"):
            data_dict[str(td.get("id"))] = str(td.text)
    
    return data_dict


scrape_company_data("http://data-interview.enigmalabs.org", "solution.json")
