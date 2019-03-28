import requests
import urllib.request
import time
from threading import Thread
from bs4 import BeautifulSoup


def scrape(interval):
    # To download the whole data set, let's do a for loop through all a tags
    lastContracts = []

    while True:
        # Set the URL you want to webscrape from
        url = 'https://ropsten.etherscan.io/contractsVerified'

        # Connect to the URL
        response = requests.get(url)

        contracts = []

        # Parse HTML and save to BeautifulSoup object¶
        soup = BeautifulSoup(response.text, "html.parser")
        for i in range(35, len(soup.findAll('a')) - 7):  # 'a' tags are for links
            one_a_tag = soup.findAll('a')[i]
            link = one_a_tag['href']
            link = link.split("/")[2].split("#")[0]
            print("link: " + link)
            contracts.append(link)

            if link not in lastContracts:
                print("Contract has not been scanned: send to analyzer")
                # TODO Send contract to analyzer

        print("-------------------------------------------------------------")
        lastContracts = contracts
        time.sleep(interval)


try:
    Thread.start(scrape(5))
except:
    print("Error: unable to start thread")
