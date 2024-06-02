# class Industry:
#     def __init__(self, name, sector, historical_emissions, production_output, emission_reduction_measures,
#                  future_expansion_plans, technological_infrastructure, carbon_intensity, compliance_history):
#         self.name = name
#         self.sector = sector
#         self.historical_emissions = historical_emissions
#         self.production_output = production_output
#         self.emission_reduction_measures = emission_reduction_measures
#         self.future_expansion_plans = future_expansion_plans
#         self.technological_infrastructure = technological_infrastructure
#         self.carbon_intensity = carbon_intensity
#         self.compliance_history = compliance_history
#
#     def calculate_current_emissions(self):
#         return self.historical_emissions + (self.production_output * self.carbon_intensity)
#
#     def alert_if_crossing_limit(self, emission_limit):
#         current_emissions = self.calculate_current_emissions()
#         if current_emissions > emission_limit:
#             return f"Alert: {self.name} has crossed emission limit. Current emissions: {current_emissions} tons."
#         else:
#             return f"{self.name} is within emission limits. Current emissions: {current_emissions} tons."
#
#
# # Example Usage:
# industry1 = Industry(name="Industry 1",
#                      sector="Manufacturing",
#                      historical_emissions=10000,  # tons
#                      production_output=5000,  # units
#                      emission_reduction_measures=["Installation of scrubbers", "Energy efficiency improvements"],
#                      future_expansion_plans="Expansion of production facilities",
#                      technological_infrastructure="Advanced",
#                      carbon_intensity=2,  # tons per unit
#                      compliance_history="Good")
#
# industry2 = Industry(name="Industry 2",
#                      sector="Energy",
#                      historical_emissions=15000,  # tons
#                      production_output=8000,  # units
#                      emission_reduction_measures=["Shift to renewable energy sources", "Implementation of carbon capture"],
#                      future_expansion_plans="Investment in solar and wind farms",
#                      technological_infrastructure="Moderate",
#                      carbon_intensity=1.5,  # tons per unit
#                      compliance_history="Average")
#
# # Define emission limits for each industry
# emission_limits = {"Industry 1": 20000, "Industry 2": 25000}
#
# # Check if industries are crossing their emission limits
# for industry in [industry1, industry2]:
#     if industry.name in emission_limits:
#         print(industry.alert_if_crossing_limit(emission_limits[industry.name]))


import csv
import json
import time
import pickle
from hashlib import sha256
from datetime import datetime

# Block class for creating blocks
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    # Method to compute hash of the block
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


# Blockchain class to manage the chain and its operations
class Blockchain:
    # Difficulty of our PoW algorithm
    difficulty = 2  # Using difficulty 2 computation

    # Initializing the blockchain
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    # Method to create the genesis block
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    # Getter method to get the last block in the chain
    @property
    def last_block(self):
        return self.chain[-1]

    # Method to add a block to the chain
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash

        # Checking if the previous hash matches
        if previous_hash != block.previous_hash:
            return False

        # Checking if the proof of work is valid
        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    # Method to validate proof of work
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

    # Method to perform proof of work
    def proof_of_work(self, block):
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    # Method to add a new transaction
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    # Method to mine a block
    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index

    # Method to save blockchain object to file
    def save_object(self, obj, filename):
        with open(filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


# CarbonCreditSystem class to manage carbon credit related operations
class CarbonCreditSystem:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    # Method to read data from CSV file
    def read_data_from_csv(self, filename):
        industries = []
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                industries.append(row)
        return industries

    # Method to add data to blockchain
    def add_blockchain_data(self, data):
        for industry_data in data:
            block = Block(index=len(self.blockchain.chain) + 1,
                          transactions=[industry_data],
                          timestamp=time.time(),
                          previous_hash=self.blockchain.last_block.hash)
            proof = self.blockchain.proof_of_work(block)
            self.blockchain.add_block(block, proof)


# Main execution block
# Main execution block
if __name__ == "__main__":
    # Initialize blockchain and CarbonCreditSystem
    blockchain = Blockchain()
    carbon_credit_system = CarbonCreditSystem(blockchain)

    # Read data from CSV file
    data = carbon_credit_system.read_data_from_csv('carbon_credits_data.csv')

    # Add data to blockchain
    carbon_credit_system.add_blockchain_data(data)

    # Mine the data
    blockchain.mine()

    # Save blockchain object to file
    blockchain.save_object(blockchain, 'blockchain_data.pkl')

    # Load blockchain object from file
    with open('blockchain_data.pkl', 'rb') as file:
        blockchain = pickle.load(file)

    # Display the entire blockchain
    print("Blockchain:")
    for block in blockchain.chain:
        print(f"Block Index: {block.index}")
        print(f"Timestamp: {datetime.fromtimestamp(block.timestamp)}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("Transactions:")
        for transaction in block.transactions:
            print(json.dumps(transaction, indent=4))
        print()


