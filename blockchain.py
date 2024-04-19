# Programa Python para crear una cadena de bloques (Blockchain)

# Importar datetime para generar marcas temporales de los bloques
import datetime

# Importar hashlib para realizar operaciones de hash y así garantizar la integridad de los bloques
import hashlib

# Importar json para facilitar el almacenamiento y la manipulación de la estructura de los bloques
import json

# Importar Flask para crear la aplicación web y jsonify para formatear la respuesta como JSON
from flask import Flask, jsonify

class Blockchain:

    # Constructor para inicializar la cadena de bloques
    # Crea el bloque génesis y establece su hash a "0"
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    # Función para crear un nuevo bloque en la cadena
    # Requiere una prueba de trabajo y el hash del bloque anterior
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    # Función para obtener el último bloque de la cadena
    def print_previous_block(self):
        return self.chain[-1]

    # Función para realizar la prueba de trabajo (Proof of Work)
    # Encuentra un número que resuelva el problema definido y así minar un nuevo bloque
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

    # Función para calcular el hash de un bloque
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # Función para verificar la integridad de la cadena
    # Comprueba que los enlaces entre bloques sean correctos y que las pruebas de trabajo sean válidas
    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1

        return True

# Inicializar Flask
app = Flask(__name__)

# Instancia de la clase Blockchain
blockchain = Blockchain()

# Ruta para minar un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {
        'message': 'Un bloque ha sido MINADO',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

# Ruta para obtener la cadena completa
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

# Ruta para verificar la validez de la cadena de bloques
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)

    if valid:
        response = {'message': 'El Blockchain es válido.'}
    else:
        response = {'message': 'El Blockchain no es válido.'}
    return jsonify(response), 200

# Ejecutar el servidor Flask localmente
app.run(host='127.0.0.1', port=5000)
