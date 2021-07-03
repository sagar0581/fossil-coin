import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_and_add_block(proof = 1, previous_hash = '0')
        self.nodes = set()

    def create_and_add_block(self, proof, previous_hash):
        block = { 'index': len(self.chain) + 1,
          'timestamp': str(datetime.datetime.now()),
          'proof': proof,
          'previous_hash': previous_hash,
          'transactions': self.transactions
        }
        self.chain.append(block)
        self.transactions = []
        return block
    
    def get_previous_block(self):
        return self.chain[-1]

    def get_block_hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def generate_proof_of_work(self, previous_proof):
        proof = 1
        valid_proof = False
        while valid_proof is False:
            hash = self.get_hash_from_proof(proof, previous_proof)
            if hash[:4] == '0000':
                valid_proof = True
            else:
                proof += 1
        return proof

    
    
    def validate_chain(self, chain):
        block_index = 1
        previous_block = chain[0]
        while block_index < len(chain):
            current_block = chain[block_index]
            proof = current_block['proof']
            previous_proof = previous_block['proof']
            hash = self.get_hash_from_proof(proof, previous_proof)
            previous_block_hash = self.get_block_hash(previous_block)
            if hash[:4] != '0000':
                return False
            if previous_block_hash != current_block['previous_hash']:
                return False
            previous_block = current_block
            block_index += 1
        return True

    def get_hash_from_proof(self, proof, previous_proof):
        return hashlib.sha256(str(previous_proof * proof + previous_proof % proof).encode()).hexdigest()

    def add_transactions(self, sender, receiver, amount):
        self.transactions.append({
          'sender': sender,
          'receiver': receiver,
          'amount': amount
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/crypto/chain')
            if response.status_code == 200:
                chain_length = response.json()['length']
                chain = response.json()['chain']
                if chain_length > max_length and self.validate_chain(chain):
                    max_length = chain_length
                    longest_chain = chain
        
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

# App server
app = Flask(__name__)

node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/crypto/mine', methods = ['GET'])
def mine_new_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    new_proof = blockchain.generate_proof_of_work(previous_proof)
    previous_block_hash = blockchain.get_block_hash(previous_block)
    blockchain.add_transactions(sender = node_address, receiver = 'C', amount = 1)
    new_block = blockchain.create_and_add_block(new_proof, previous_block_hash)
    response = {
        'message': 'New block mined',
        'blockIndex': new_block['index'],
        'timestamp': new_block['timestamp'],
        'proof': new_block['proof'],
        'previous_hash': new_block['previous_hash'],
        'transactions': new_block['transactions']
    }
    return jsonify(response), 200

@app.route('/crypto/chain', methods = ['GET'])
def get_block_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/crypto/validate_chain', methods = ['GET'])
def is_chain_valid():
    chain_valid = blockchain.validate_chain(blockchain.chain)
    if chain_valid is False:
        response = {'message': 'Invalid chain'}
    else:
        response = {'message': 'Chain is valid'}
    return jsonify(response), 200

@app.route('/crypto/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'some elements of the transaction are missing', 400
    index = blockchain.add_transactions(sender = json['sender'], receiver = json['receiver'], amount = json['amount'])
    response = {
        'message': f'Transaction will be added to index {index}',
        'index': index
    }
    return response, 201
    
@app.route('/crypto/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': f'All nodes are connected now',
        'total_nodes': list(blockchain.nodes)
    }
    return response, 201

@app.route('/crypto/replace_chain', methods = ['GET'])
def replace_chain():
    replace_chain = blockchain.replace_chain()
    if replace_chain is True:
        response = {
            'message': 'Chain was replaced.',
            'newChain': blockchain.chain
        }
    else:
        response = {
            'message': 'All good',
            'aactual_chain': blockchain.chain
        }
    return jsonify(response), 200

app.run(host = '127.0.0.1', port = 3003)