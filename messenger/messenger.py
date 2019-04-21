from web3 import Web3, HTTPProvider
from threading import Thread
from queue import Queue
import binascii

from scraper.scraper import Scraper


class Messenger(Thread):
    def __init__(self, report_q, private_key, testnet):
        Thread.__init__(self)
        self.report_q = report_q
        self.private_key = private_key
        self.testnet = testnet
        Thread.daemon = True

    def run(self):
        # Abi of the messaging smart contract
        # abi = '''[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"last_msg_index","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_key","type":"string"},{"name":"_type","type":"string"}],"name":"setPublicKey","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_who","type":"address"},{"name":"_index","type":"uint256"}],"name":"newMessage","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_who","type":"address"},{"name":"_index","type":"uint256"}],"name":"getMessageByIndex","outputs":[{"name":"","type":"address"},{"name":"","type":"string"},{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"keys","outputs":[{"name":"key","type":"string"},{"name":"key_type","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_who","type":"address"}],"name":"getPublicKey","outputs":[{"name":"_key","type":"string"},{"name":"_key_type","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"uint256"}],"name":"messages","outputs":[{"name":"from","type":"address"},{"name":"text","type":"string"},{"name":"time","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_text","type":"string"}],"name":"sendMessage","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_who","type":"address"}],"name":"getLastMessage","outputs":[{"name":"","type":"address"},{"name":"","type":"string"},{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"lastIndex","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"message_staling_period","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_sender","type":"address"},{"indexed":true,"name":"_receiver","type":"address"},{"indexed":false,"name":"_time","type":"uint256"},{"indexed":false,"name":"message","type":"string"}],"name":"Message","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_sender","type":"address"},{"indexed":false,"name":"_key","type":"string"},{"indexed":false,"name":"_keytype","type":"string"}],"name":"PublicKeyUpdated","type":"event"}]'''

        if self.testnet:
            web3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/29e5c62848414895b549aa4befebe614'))
        else:
            web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/29e5c62848414895b549aa4befebe614'))

        acc = web3.eth.account.privateKeyToAccount(self.private_key)

        if not web3.isConnected():
            Scraper.log("Messaging:\tNo connection established")

        # Messaging smart contract to use if not sending a direct transaction to the contract owner
        # messaging = web3.eth.contract(address="0xCdcDD44f7f617B965983a8C1bB0B845A5766FEbA", abi=abi)

        Scraper.log("Messaging:\tWaiting for messages")

        nonce = 1

        while True:
            (address, message) = self.report_q.get()

            if message is None:
                break

            message = "Hello, We scanned a smart contract you deployed and found a vulnrability in it, here is the report:\n" + message

            transaction = {
                    'to' : web3.toChecksumAddress(address),
                    'from' : acc.address,
                    'value' : 0,
                    'gasPrice' : web3.eth.gasPrice,
                    'nonce' : web3.eth.getTransactionCount(acc.address),
                    'data' : message.encode('utf-8').hex()
            }

            transaction['gas'] = web3.eth.estimateGas(transaction)

#            transaction = messaging.functions.sendMessage(address, message).buildTransaction({'from': acc.address, 'nonce': '0x%02x' % web3.eth.getTransactionCount(address)} # Use this to send the message to a messaging smart contract)

            signed = acc.signTransaction(transaction)

            tx = web3.eth.sendRawTransaction(signed.rawTransaction)

            Scraper.log("Messaging:\tSent message")
        Scraper.log("Messaging:\tReceived terminator, shutting down...")
