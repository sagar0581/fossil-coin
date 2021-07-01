from blockchain import Blockchain
from flask import Flask, jsonify

# App server
app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine', methods = ['GET'])
def mine_new_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    new_proof = blockchain.generate_proof_of_work(previous_proof)
    previous_block_hash = blockchain.get_block_hash(previous_block)
    new_block = blockchain.create_and_add_block(new_proof, previous_block_hash)
    response = {
        'message': 'New block mined',
        'blockIndex': new_block['index'],
        'timestamp': new_block['timestamp'],
        'proof': new_block['proof'],
        'previous_hash': new_block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/chain', methods = ['GET'])
def get_block_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/validate_chain', methods = ['GET'])
def is_chain_valid():
    chain_valid = blockchain.validate_chain()
    if chain_valid is False:
        response = {'message': 'Invalid chain'}
    else:
        response = {'message': 'Chain is valid'}
    return jsonify(response), 200

app.run(host = '127.0.0.1', port = 3000)