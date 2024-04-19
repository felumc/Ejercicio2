from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
node_address = "http://127.0.0.1:5000"
blockchain = Blockchain()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()
    blockchain.unconfirmed_transactions.append(tx_data)
    return "Success", 201

@app.route('/mine', methods=['GET'])
def mine():
    if not blockchain.unconfirmed_transactions:
        return "No transactions to mine", 404

    last_block = blockchain.chain[-1]
    new_block = Block(index=last_block.index + 1,
                      transactions=blockchain.unconfirmed_transactions,
                      timestamp=time.time(),
                      previous_hash=last_block.hash)
    proof = blockchain.proof_of_work(new_block)
    blockchain.add_block(new_block, proof)
    blockchain.unconfirmed_transactions = []
    announce_new_block(new_block)
    return jsonify(new_block.__dict__), 200

@app.route('/register_node', methods=['POST'])
def register_node():
    node_data = request.get_json()
    blockchain.nodes.add(node_data["node_address"])
    return "Node registered successfully.", 201

def announce_new_block(block):
    for node in blockchain.nodes:
        url = f"{node}/add_block"
        requests.post(url, json=block.__dict__)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
