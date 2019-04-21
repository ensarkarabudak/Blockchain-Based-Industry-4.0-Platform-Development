import hashlib
import json
from time import time
import requests
from flask import Flask, jsonify, request


class Blockchain:
    def __init__(self):
        self.mevcut_transactions = []
        self.chain = []
        self.nodes = set()

        # Genesis bloğu oluşturma
        self.yeni_block(önceki_hash='1', proof=100)

    def yeni_block(self, proof, önceki_hash):
        """

         ### Blockchain içinde bir blok oluşturuyoruz ###
        :param proof:  İspat "İş İspatı" algoritmasıyla verilir
        :param previous_hash: (Opsiyonel)  Önceki bloğun hash değeri
        :return:  Yeni blok

        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.mevcut_transactions,
            'proof': proof,
            'önceki_hash': önceki_hash or self.hash(self.chain[-1]),
        }

        # Transactions'ları temizle
        self.mevcut_transactions = []

        self.chain.append(block)
        return block

    def yeni_transaction(self, Gönderici, Alıcı, Mesaj):
        
        """

        ### Bir sonraki blok için yeni bir işlem oluşturur. ###
        :param Gönderici:  Gönderenin adresi
        :param Alıcı:  Alıcının adresi
        :param Mesaj:  Tutar
        :return:  Bu işlemi gerçekleştirecek blok dizini

        """
        self.mevcut_transactions.append({
            'Gönderici': Gönderici,
            'Alıcı': Alıcı,
            'Mesaj': Mesaj,
        })

        return self.önceki_block['index'] + 1

    @property
    def önceki_block(self):  
        # Last block değeri zincirin son elemanını doner
        return self.chain[-1]

    @staticmethod
    def hash(block):

        """
        ### Bloku hash'ler ###

        Blokun SHA-256 hash değerini oluşturuyoruz
        :param block:  Block
        :return: 

        """
        # Dictionary'nin sıralı olduğundan emin olmalıyız, aksi halde tutarsız hash'ler olur.
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, önceki_block):
        önceki_proof = önceki_block['proof']
        önceki_hash = self.hash(önceki_block)

        proof = 0
        while self.dogrula_proof(önceki_proof, proof, önceki_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def dogrula_proof(önceki_proof, proof, önceki_hash):
        """

        ### İspatı doğrula: hash(last_proof, proof) 4 adet 0 ile başlıyor mu? ###
        
        :param last_proof:  Önceki İspat
        :param proof:  Mevcut İspat
        :return:  True if correct, False if not.

        """
        guess = f'{önceki_proof}{proof}{önceki_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

app = Flask(__name__)

"""
# Ödül için her düğüme benzersiz bir adres oluşturma.(Şuanlık kullanılmayacak)
node_identifier = str(uuid4()).replace('-', '')

"""
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # Sonraki kanıtı almak için iş kanıtı algoritmamızı çalıştırıyoruz...
    önceki_block = blockchain.önceki_block
    proof = blockchain.proof_of_work(önceki_block)

    önceki_hash = blockchain.hash(önceki_block)
    # Yeni bloğu zincire ekleyerek çıkarıyoruz..
    block = blockchain.yeni_block(proof, önceki_hash)

    """
    # Ödül Kısmı(Şuanlık kullanılmayacak)
    blockchain.yeni_transaction(
        Gönderici="root",
        Alıcı=node_identifier,
        Mesaj="Öd",
    )
    """
    response = {
        'message': "Yeni blok oluşturuldu",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'önceki_hash': block['önceki_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def yeni_transaction():
    degerler = request.get_json()

     # Zorunlu alanların POST ile gönderilen verinin içinde olduğunu kontrol ediyoruz..
    gerekli_degerler = ['Gönderici', 'Alıcı', 'Mesaj']
    if not all(k in degerler for k in gerekli_degerler):
        return 'Geçersiz Değer', 400

    # Yeni transaction oluşturma
    index = blockchain.yeni_transaction(degerler['Gönderici'], degerler['Alıcı'], degerler['Mesaj'])

    response = {'Mesaj': f'Transaction {index}.bloğa eklenecek'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def zincir_goster():
    response = {
        'chain': blockchain.chain,
        'uzunluk': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
