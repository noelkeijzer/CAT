from queue import Queue

import requests
import time
import datetime
import json
from threading import Thread


class Scraper(Thread):
    def __init__(self, contract_queue):
        Thread.__init__(self)
        self.new_contract_queue = contract_queue
        Thread.daemon = True

    def run(self):
        last_contracts = [None]
        last_block = None
        while True:
            block = self.get_newest_block()
            if last_block != block:
                last_contracts = [None]
            last_block = block
            count = int(self.get_transaction_count_for_block(block), 16)

            for i in range(0, count):
                contract = self.get_contract_by_block_and_index(block, hex(i))
                if contract not in last_contracts:
                    self.log("Checking {}@{}: {}".format(i, block, self.get_contract_by_block_and_index(block, hex(i))))
                    new_contract_queue.put(contract)
                time.sleep(0.2)

    @staticmethod
    def get_newest_block():
        response = requests.get("https://api-ropsten.etherscan.io/api?module=proxy&"
                                "action=eth_blockNumber&apikey=SECRET")
        result = json.loads(response.text)
        return result["result"]

    @staticmethod
    def get_transaction_count_for_block(block_number):
        response = requests.get("https://api-ropsten.etherscan.io/api?module=proxy&action="
                                "eth_getBlockTransactionCountByNumber&tag={}&apikey=SECRET".format(block_number))
        result = json.loads(response.text)
        return result["result"]

    @staticmethod
    def get_contract_by_block_and_index(block, index):
        response = requests.get("https://api-ropsten.etherscan.io/api?module=proxy&action="
                                "eth_getTransactionByBlockNumberAndIndex&tag={}&index={}&"
                                "apikey=SECRET".format(block, index))
        result = json.loads(response.text)
        return result["result"]["creates"]

    @staticmethod
    def log(message):
        print("[CAT - {}] {}".format(datetime.datetime.now().strftime("%H:%M:%S"), message))


if __name__ == '__main__':
    new_contract_queue = Queue()
    scraper = Scraper(new_contract_queue)
    scraper.run()
