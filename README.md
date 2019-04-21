# CAT
Contract Analysis Tool

Scans the ethereum blockchain for vulnerable smart contracts and lets their creator know about them.

Dependencies:
crypto
mythril
web3

After installing the correct packages, an EtherScan API key is needed. This API key can be retrieved from https://etherscan.io/myapikey after creating an account. The last step to perform, before running the program, is to have a private account key at the Ethereum Ropsten network. For the program to work, some ETH has to be in the account that is linked to the private key. After completing the steps mentioned above, CAT can be run by issuing the following command: python3 main.py [your etherscan api key] [your private ropsten account key].
