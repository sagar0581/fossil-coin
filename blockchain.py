import datetime

from flask import Flask, jsonify


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_and_add_block(proof = 1, previous_hash = '0')

    def create_and_add_block(self, proof, previous_hash):
	    block = { 'index': len(self.chain) + 1,
		    'timestamp': str(datetime.datetime.now()),
		    'proof': proof,
		    'previous_hash': previous_hash
	    }
	    self.chain.append(block)
	    return block

           
