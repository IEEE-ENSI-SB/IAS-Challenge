from django.utils import timezone
import hashlib
import json

class Blockchain_Transactions:
    def __init__(self):
        #create a variable name chain : it's a list of blocks stored in form of dictionnary
        self.chain = []
        transaction = {
            'User_ID' : None,
            'User_username': None,
            'User_email': None,
            'User_phone': None,
            'UserImageUrl': None,

            'Charger_username': None,
            'Charger_email': None,
            'Charger_phone': None,
            'chargerId': None,
            'chargerImageUrl': '../static/images/default_image.jpg',

            'charging_fees': None,
            'Energy_Delivered': None,

            'Vehicle_Type': None,

            'Charger_Type': None,

            'charger_position': None,

            'Transaction_date': None,
        }
        self.create_block(1, '0', transaction ) 

    def create_block(self,nonce,previous_hash,transaction):
        index = len(self.chain) + 1
        block = {
            'index': index,
            'timestamp':str(timezone.now()),
            'nonce': nonce,
            'transaction': transaction,
            'previous_hash': previous_hash
        }
        self.chain.append(block)

    def get_last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while not check_nonce:
            hash_code = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_code[0:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode() #.encode() method is used to convert a string into a sequence of bytes
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_nonce = previous_block['nonce']
            current_nonce = block['nonce']
            hash_code = hashlib.sha256(str(current_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_code[0:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

#-------------------------------------------------------------
BT = Blockchain_Transactions()
BT_scam = Blockchain_Transactions()


def mine_block(BLOCK, transaction):
    previous_block = BLOCK.get_last_block()
    previous_nonce = previous_block['nonce']
    previous_hash = BLOCK.hash(previous_block)
    new_nonce = BLOCK.proof_of_work(previous_nonce)
    BLOCK.create_block(new_nonce, previous_hash, transaction)
