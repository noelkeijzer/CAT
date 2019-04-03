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
                                "action=eth_blockNumber&apikey=DVVX3Z2GF84D1FSUJY9YSNUVUDBJANPHK9")
        result = json.loads(response.text)
        return result["result"]

    @staticmethod
    def get_transaction_count_for_block(block_number):
        response = requests.get("https://api-ropsten.etherscan.io/api?module=proxy&action="
                                "eth_getBlockTransactionCountByNumber&tag={}&apikey=DVVX3Z2GF84D1FSUJY9YSNUVUDBJANPHK9".format(block_number))
        result = json.loads(response.text)
        return result["result"]

    @staticmethod
    def get_contract_by_block_and_index(block, index):
        response = requests.get("https://api-ropsten.etherscan.io/api?module=proxy&action="
                                "eth_getTransactionByBlockNumberAndIndex&tag={}&index={}&"
                                "apikey=DVVX3Z2GF84D1FSUJY9YSNUVUDBJANPHK9".format(block, index))
        try:
            result = json.loads(response.text)
            return result["result"]["creates"]
        except json.decoder.JSONDecodeError:
            print("Etherscan has blocked you!!!!")
            return {"jsonrpc":"2.0","result":{"blockHash":"0x72399c158fb5ca4b3502af1c3bc4e764cbd78ad2417269506b9a6778629ef36e","blockNumber":"0x515e00","chainId":"0x3","condition":null,"creates":null,"from":"0xe0bb9e342e79e54282fb8ee50510d8cd69850823","gas":"0x186a0","gasPrice":"0x77359400","hash":"0xee94f3922a728bb60e6c58f5b7fa78c89a40a3ea277f599226b124bb6b786eb0","input":"0x","nonce":"0xac1ab","publicKey":"0xa0693e8da772a1b9222203771f5949d4d2063b6b97828a0fa3d9aa94cc2a60ae39742d6cfb2a9d2d3d2fea7e11d9e33ae8cb188d46977d5e6544843d4e170d2f","r":"0x1361a5e7656c07926ea2cbed0f32d0afdd8cd5404c06b061a68cf334927ff6c","raw":"0xf867830ac1ab8477359400830186a094e0bb9e342e79e54282fb8ee50510d8cd6985082301802aa001361a5e7656c07926ea2cbed0f32d0afdd8cd5404c06b061a68cf334927ff6ca02b520e6bba73663b1d6e2a13915db95e9361aa04c30232b2a8e2d00d3c5864ef","s":"0x2b520e6bba73663b1d6e2a13915db95e9361aa04c30232b2a8e2d00d3c5864ef","standardV":"0x1","to":"0xe0bb9e342e79e54282fb8ee50510d8cd69850823","transactionIndex":"0xd","v":"0x2a","value":"0x1"},"id":1}
            pass

    @staticmethod
    def log(message):
        print("[CAT - {}] {}".format(datetime.datetime.now().strftime("%H:%M:%S"), message))


if __name__ == '__main__':
    new_contract_queue = Queue()
    scraper = Scraper(new_contract_queue)
    scraper.run()
