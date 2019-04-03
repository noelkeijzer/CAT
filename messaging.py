from web3 import Web3

abi = '''[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"last_msg_index","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_key","type":"string"},{"name":"_type","type":"string"}],"name":"setPublicKey","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_who","type":"address"},{"name":"_index","type":"uint256"}],"name":"newMessage","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_who","type":"address"},{"name":"_index","type":"uint256"}],"name":"getMessageByIndex","outputs":[{"name":"","type":"address"},{"name":"","type":"string"},{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"keys","outputs":[{"name":"key","type":"string"},{"name":"key_type","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_who","type":"address"}],"name":"getPublicKey","outputs":[{"name":"_key","type":"string"},{"name":"_key_type","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"uint256"}],"name":"messages","outputs":[{"name":"from","type":"address"},{"name":"text","type":"string"},{"name":"time","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_text","type":"string"}],"name":"sendMessage","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_who","type":"address"}],"name":"getLastMessage","outputs":[{"name":"","type":"address"},{"name":"","type":"string"},{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"lastIndex","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"message_staling_period","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_sender","type":"address"},{"indexed":true,"name":"_receiver","type":"address"},{"indexed":false,"name":"_time","type":"uint256"},{"indexed":false,"name":"message","type":"string"}],"name":"Message","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_sender","type":"address"},{"indexed":false,"name":"_key","type":"string"},{"indexed":false,"name":"_keytype","type":"string"}],"name":"PublicKeyUpdated","type":"event"}]'''

web3 = Web3(Web3.IPCProvider(testnet=True))

if not web3.isConnected():
    print("No connection established")

print(web3.eth.getBlock('latest'))

messaging = web3.eth.contract(address="0xCdcDD44f7f617B965983a8C1bB0B845A5766FEbA", abi=abi)

transaction = messaging.functions.sendMessage("0xEf65A9c43c93cA0f7bD2Ba2958Ced84992927227", "").buildTransaction({'from': web3.eth.accounts[0]})

web3.personal.unlockAccount(web3.eth.accounts[0], "password")

tx = web3.eth.sendTransaction(transaction)

print(tx)

