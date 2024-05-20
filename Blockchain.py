# Программа на Python для создания блокчейна
# Для временной метки
import datetime
# Вычисление хэша для добавления цифровой подписи к блокам
import hashlib
# Для хранения данных в блокчейне
import json
# Flask предназначен для создания веб-приложения, а jsonify - для
# отображения блокчейнаn
from flask import Flask, jsonify
# подключение к бд
import psycopg2
import pandas as pd
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, hashed_data='0')

# Импорт базы данных
def connect_db():
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='1111', host='localhost')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "blockchain"')
    df = cursor.fetchall()
    df = pd.DataFrame(df)

    return df
database = connect_db()
database[0].iloc[0] = 'Zavalnuk Dmitrii'
database[2].iloc[0] = 'Zavalnuk123'
database[0].iloc[1] = 'Shabashov Vyacheslav'
database[2].iloc[1] = 'Shabashov1234'
database[0].iloc[2] = 'Sintyalev Alexandr'
database[2].iloc[2] = 'Sintyalev12345'
database[0].iloc[3] = 'Azizov Dzhumahon'
database[2].iloc[3] = 'Azizov123456'
database[0].iloc[4] = 'Ivanov Ivan'
database[2].iloc[4] = 'Ivanov1234567'
print(database)
class Blockchain:
# Эта функция ниже создана для создания самого первого блока и установки его хэша равным "0"
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, hashed_data='0')
# Эта функция ниже создана для добавления дополнительных блоков в цепочку
    def create_block(self, proof, hashed_data):
        block = {
            'index': len(self.chain) + 1,
            'name': str(database[0].iloc[len(self.chain)]),
            'email': str(database[1].iloc[len(self.chain)]),
            'phone': str(database[2].iloc[len(self.chain)]),
            'hashed_data': str(database[3].iloc[len(self.chain)]),
            'proof': proof  # добавлено
        }

        self.chain.append(block)
        return block
# Эта функция ниже создана для отображения предыдущего блока
    def print_previous_block(self):
        return self.chain[-1]
# Это функция для проверки работы и используется для успешного майнинга блока
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


def chain_valid(self, chain):
    previous_block = chain[0]
    block_index = 1
    while block_index < len(chain):
        block = chain[block_index]
        if block['hashed_data'] != self.hash(previous_block):
            return False
        previous_proof = previous_block['proof']
        proof = block['proof']
        hash_operation = hashlib.sha256(
            str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
        if hash_operation[:5] != '00000':
            return False
        previous_block = block
        block_index += 1
    return True

# Создание веб-приложения с использованием flask
app = Flask(__name__)
# Создаем объект класса blockchain
blockchain = Blockchain()
# Страница с подсказками
@app.route('/')
def index():
    return "Майнинг нового блока: /mine_block  " \
           "Отобразить блокчейн в формате json: /display_chain  " \
           "Проверка валидности блокчейна: /valid  "

# Майнинг нового блока
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_block['proof'])  # изменено
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'A block is MINED',
                'index': block['index'],
                'name': block['name'],
                'email': block['email'],
                'phone': block['phone'],
                'hashed_data': block['hashed_data']}
    return jsonify(response), 200
# Отобразить блокчейн в формате json
@app.route('/display_chain', methods=['GET'])
def display_chain():
    chain = []
    for block in blockchain.chain:
        data = {
            'index': block['index'],
            'name': block['name'],
            'email': block['email'],
            'phone': block['phone'],
            'hashed_data': block['hashed_data']
        }
        chain.append(data)
    response = {'chain': chain, 'length': len(chain)}
    return jsonify(response), 200
# Проверка валидности блокчейна
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
# Запустите сервер flask локально
app.run(debug = True)

