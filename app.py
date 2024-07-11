from flask import Flask, request, jsonify, render_template
from origin_transation import BlockChainProcess

app = Flask(__name__)

# 初始化 BlockChainProcess
block_chain_process = BlockChainProcess(
    '0x2bdf99f7460156211739b275b9a22f983c011e55',
    '0x465047ba558172c7a8e9999bd2a080e7a0577e91',
    'UTC--2024-05-22T08-23-18.599501038Z--2bdf99f7460156211739b275b9a22f983c011e55'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    ehr_summary = request.json
    tx_hash = block_chain_process.send_transaction(ehr_summary)
    return jsonify({'transaction_hash': tx_hash})

@app.route('/search_transaction', methods=['POST'])
def search_transaction():
    tx_hash = request.json['tx_hash']
    transaction_data = block_chain_process.search_transaction(tx_hash)
    return jsonify({'transaction_data': transaction_data})

@app.route('/verify_transaction', methods=['POST'])
def verify_transaction():
    transaction_data = request.json['transaction_data']
    ehr_summary = request.json['ehr_summary']
    is_verified = block_chain_process.verify_transaction(transaction_data, ehr_summary)
    return jsonify({'is_verified': is_verified})

if __name__ == '__main__':
    app.run(debug=True)
