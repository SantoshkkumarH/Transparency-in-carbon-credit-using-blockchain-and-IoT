from Block import Block


class Blockchain:
    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []
        self.genesis_block()

    def genesis_block(self):
        transactions = []
        genesis_block = Block(transactions, "0")
        genesis_block.generate_hash()
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        previous_hash = (self.chain[len(self.chain) - 1]).hash
        new_block = Block(transactions, previous_hash)
        new_block.generate_hash()
        # proof = proof_of_work(block)
        self.chain.append(new_block)

    def print_blocks(self):
        for i in range(len(self.chain)):
            current_block = self.chain[i]
            print("Block {} {}".format(i, current_block))
            current_block.print_contents()

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if (current.hash != current.generate_hash()):
                print("Current hash does not equal generated hash")
                return False
            if (current.previous_hash != previous.generate_hash()):
                print("Previous block's hash got changed")
                return False
        return True

    def proof_of_work(self, block, difficulty=2):
        proof = block.generate_hash()
        while proof[:2] != "0" * difficulty:
            block.nonce += 1
            proof = block.generate_hash()
        block.nonce = 0
        return proof
