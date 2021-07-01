import datetime
import hashlib
import json

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

    
    
    def validate_chain(self):
        block_index = 1
        previous_block = self.chain[0]
        while block_index < len(self.chain):
            current_block = self.chain[block_index]
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

           
