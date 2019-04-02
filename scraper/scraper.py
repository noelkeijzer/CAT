import requests
import urllib.request
import time
import datetime
import json
from threading import Thread
from bs4 import BeautifulSoup

def scrape_verified(interval):
    """Scrapes the Etherscan website to find new verified contracts

    Parameters:
    interval (int): The amount of seconds to sleep between each scrape
    """

    # Results from the last scraping attempt
    lastContracts = []

    while True:
        # TODO: Should probably be configured through a config file
        url = 'https://ropsten.etherscan.io/contractsVerified'

        # Get the contents of the page
        response = requests.get(url)

        # All contracts found on the page
        contracts = []

        # Parse HTML and save to BeautifulSoup object
        soup = BeautifulSoup(response.text, "html.parser")
        for i in range(35, len(soup.findAll('a')) - 7):  # 'a' tags are for links
            one_a_tag = soup.findAll('a')[i]
            link = one_a_tag['href']
            link = link.split("/")[2].split("#")[0]
            contracts.append(link)

            if link not in lastContracts:
                log("New contract: {}".format(link))
                # TODO Send contract to analyzer

        lastContracts = contracts
        time.sleep(interval)

def get_newest_block():
    response = requests.get("https://api-ropsten.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=SECRET")
    result = json.loads(response.text)
    return result["result"]

def get_transaction_count_for_block(block_number):
    response = requests.get("https://api-ropsten.etherscan.io/api?module=proxy&action=eth_getBlockTransactionCountByNumber&tag={}&apikey=SECRET".format(block_number))
    result = json.loads(response.text)
    return result["result"]

def get_contract_by_block_and_index(block, index):
    response = requests.get("https://api-ropsten.etherscan.io/api?module=proxy&action=eth_getTransactionByBlockNumberAndIndex&tag={}&index={}&apikey=SECRET".format(block, index))
    result = json.loads(response.text)
    return result["result"]["creates"]

def log(message):
    print("[CAT - {}] {}".format(datetime.datetime.now().strftime("%H:%M:%S"), message))

block = get_newest_block()
count = int(get_transaction_count_for_block(block), 16)

for i in range(0, count):
    log("Checking {}@{}: {}".format(i, block, get_contract_by_block_and_index(block, hex(i))))
    time.sleep(1)

try:    
    print()
    #Thread.start(scrape_verified(5))
except:
    log("Error: unable to start thread")
