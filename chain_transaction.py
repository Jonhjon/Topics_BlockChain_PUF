import hashlib
import json
from web3 import Web3

def generate_ehr_hash(ehr_summary):
    ehr_summary_json = json.dumps(ehr_summary, sort_keys=True)
    ehr_hash = hashlib.sha256(ehr_summary_json.encode('utf-8')).hexdigest()
    return ehr_hash

def connect_to_eth_node(remote_node_url):
    web3 = Web3(Web3.HTTPProvider(remote_node_url))
    if web3.is_connected():
        print("Connected to remote Ethereum node")
    else:
        print("Failed to connect to Ethereum node")
    return web3

def build_transaction(web3, from_account, to_account, ehr_hash):
    nonce = web3.eth.get_transaction_count(from_account, 'pending')
    transaction = {
        'from': from_account,
        'to': to_account,
        'value': 0,
        'gas': 100000,
        'gasPrice': web3.to_wei('50', 'wei'),
        'nonce': nonce,
        'data': web3.to_hex(text=ehr_hash)
    }
    print(f"ehr_hash_to_hex : {web3.to_hex(text=ehr_hash)}")
    return transaction

def sign_and_send_transaction(web3, transaction, private_key):
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash

def verify_ehr_hash(web3, tx_hash, original_hash):
    tx = web3.eth.get_transaction(tx_hash)
    data = tx['input']
    retrieved_hash = str(data).strip("b'")
    if original_hash == retrieved_hash:
        print("Hash values match, EHR is verified!")
    else:
        print("Hash values do not match!")
    return retrieved_hash

def main():
    # 定義電子病歷摘要
    ehr_summary = {
        "patient_id": "123456",
        "diagnosis": "Hypertension",
        "prescription": "Medication A, Medication B",
        "date": "2024-05-27"
    }

    # 生成 EHR 哈希值
    ehr_hash = generate_ehr_hash(ehr_summary)
    print("EHR Hash:", ehr_hash)

    # 連接到遠程以太坊節點
    remote_node_url = 'http://192.168.1.109:8545'
    web3 = connect_to_eth_node(remote_node_url)

    # 設置賬戶和交易參數
    from_account = '0x2bdf99f7460156211739b275b9a22f983c011e55'
    to_account = '0x465047ba558172c7a8e9999bd2a080e7a0577e91'
    private_key = '0xd7d37d837a297fbe4788cc2ddd52ffe449b1876097737346eed340dfc7e4a54a'

    from_account = Web3.to_checksum_address(from_account)
    to_account = Web3.to_checksum_address(to_account)

    # 構建交易
    transaction = build_transaction(web3, from_account, to_account, ehr_hash)

    # 簽名並發送交易
    tx_hash = sign_and_send_transaction(web3, transaction, private_key)
    print("Transaction hash:", web3.to_hex(tx_hash))

    # 驗證哈希值
    verify_ehr_hash(web3, tx_hash, ehr_hash)

if __name__ == "__main__":
    main()
