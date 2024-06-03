import hashlib
import json
from web3 import Web3
import requests
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def build_transaction(web3, from_account, to_account, ehr_hash,nonce):
    # nonce = web3.eth.get_transaction_count(from_account, 'latest')
    # nonce=nonce+random.randint(1,10)

    transaction = {
        'from': from_account,
        'to': to_account,
        'value': 0,
        'gas': 100000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': nonce,
        'data': web3.to_hex(text=ehr_hash)
    }
    # transaction['gas'] = web3.eth.estimate_gas(transaction)
    return transaction

def sign_and_send_transaction(web3, transaction, private_key):
    try:
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def verify_ehr_hash(web3, tx_hash, original_hash):
    tx = web3.eth.get_transaction(tx_hash)
    data = tx['input']
    retrieved_hash = str(data).strip("b'")
    if original_hash == retrieved_hash:
        print("Hash values match, EHR is verified!")
    else:
        print("Hash values do not match!")
    return retrieved_hash

# 使用ThreadPoolExecutor进行多线程发送请求
def send_requests_concurrently(web3,ehr_hash):
    from_account = '0x2bdf99f7460156211739b275b9a22f983c011e55'
    to_account = '0x465047ba558172c7a8e9999bd2a080e7a0577e91'
    private_key = '0xd7d37d837a297fbe4788cc2ddd52ffe449b1876097737346eed340dfc7e4a54a'

    from_account = Web3.to_checksum_address(from_account)
    to_account = Web3.to_checksum_address(to_account)

    base_nonce = web3.eth.get_transaction_count(from_account, 'latest')    # 使用ThreadPoolExecutor并发发送多个交易

    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = []
        for i in range(10):  # 假设我们要发送10个交易
            # 每个交易可以基于不同的数据来修改，此处用transaction_template作为基础模板
            nonce = base_nonce + i*10000000
            transaction = build_transaction(web3, from_account, to_account, ehr_hash,nonce) # 复制模板
            # 可以根据实际情况修改transaction中的'data'或其他字段
            futures.append(executor.submit(sign_and_send_transaction, web3, transaction, private_key))
        for future in as_completed(futures):
            tx_hash = future.result()
            if tx_hash:
                print(f"\n交易哈希：{str(tx_hash.hex())}")
                verify_ehr_hash(web3, tx_hash, ehr_hash)
            else:
                print("交易发送失败。")

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
    # transaction = build_transaction(web3, from_account, to_account, ehr_hash,)

    results = send_requests_concurrently(web3,ehr_hash)
    # for data, status_code, response_data in results:
    #     print(f"Request data: {data}")
    #     print(f"Response status code: {status_code}")
    #     print(f"Response data: {response_data}")


    
    # 簽名並發送交易
    # tx_hash = sign_and_send_transaction(web3, transaction, private_key)
    # print("Transaction hash:", web3.to_hex(tx_hash))

    # # 驗證哈希值
    # verify_ehr_hash(web3, tx_hash, ehr_hash)

if __name__ == "__main__":
    main()
