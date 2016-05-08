#!/usr/bin/env python3

import os
import requests
import logging
import yaml
import json

from flask import Flask
from flask import request
from flask import send_from_directory

# Import from the 21 Bitcoin Developer Library
from two1.wallet import Wallet
from two1.bitserv.flask import Payment

# See: github.com/salsa-system/weather21
# Set up logging
log = logging.getLogger('werkzeug')
logging.basicConfig(filename='upc.log', level=logging.DEBUG)
#log.setLevel(logging.ERROR)

# Configure app and wallet
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

SERVER_PORT = '5051'
UPC_URL = 'https://api.upcitemdb.com/prod/trial/lookup'


@app.route('/manifest')
def manifest():
	"""Provide the app manifest to the 21 crawler.
	"""
	with open('./manifest.yaml', 'r') as f:
		manifest = yaml.load(f)
	return json.dumps(manifest)


@app.route('/upc/client')
def client():
	"""Provide an example client script.
	"""
	return send_from_directory('static', 'upc.py')


@app.route('/lookup')
@payment.required(1000)
def upc_lookup():
	"""Charge a fixed fee per request to the UPC endpoint.
	"""
	upc_code = str(request.args.get('upc'))
	userdata = {'upc': upc_code}
	response = requests.get(UPC_URL, params=userdata)
	return(response.text)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=SERVER_PORT)


