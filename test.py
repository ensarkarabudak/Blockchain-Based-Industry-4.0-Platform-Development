import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        self.mevcut_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.yeni_block(önceki_hash='1', proof=100)

    def yeni_block(self, proof, önceki_hash):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.mevcut_transactions,
            'proof': proof,
            'önceki_hash': önceki_hash,
        }

        # Reset the current list of transactions
        self.mevcut_transactions = []

        self.chain.append(block)
        return block

block=Blockchain()

print(block.chain[-1])