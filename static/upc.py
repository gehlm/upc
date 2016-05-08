#!/usr/bin/env python3

import sys
import json

# Import methods from the 21 Bitcoin Library
from two1.commands.config import Config
from two1.wallet import Wallet
from two1.bitrequests import BitTransferRequests

SERVER_IP_ADDRESS='10.244.250.224'
SERVER_PORT = '5051'

# Configure your Bitcoin Wallet
username = Config().username
wallet = Wallet()
requests = BitTransferRequests(wallet, username)


def get_upc(upc_code):	
	upc_url = 'http://%s:%s/lookup?upc=%s' % (SERVER_IP_ADDRESS, SERVER_PORT, upc_code)
	response = requests.get(url=upc_url)
	print(response.text)


if __name__ == '__main__':

	if len(sys.argv) != 2:
		print('Usage: python3 upc.py [UPC_CODE]')
		sys.exit(1)

	upc = sys.argv[1]
	get_upc(upc)
