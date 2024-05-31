import hashlib
import json
import random
from web3 import Web3

# 定義電子病歷摘要
ehr_summary = {
    "patient_id": "123456",
    "diagnosis": "Hypertension",
    "prescription": "Medication A, Medication B",
    "date": "2024-05-27"
}

# 將摘要轉換為 JSON 字符串並計算 SHA-256 哈希值
ehr_summary_json = json.dumps(ehr_summary, sort_keys=True)
ehr_hash = hashlib.sha256(ehr_summary_json.encode('utf-8')).hexdigest()
print("EHR Hash:", ehr_hash)

# 連接到遠程以太坊節點
remote_node_url = 'http://192.168.1.109:8545'
web3 = Web3(Web3.HTTPProvider(remote_node_url))

# 檢查連接狀態
if web3.is_connected():
    print("Connected to remote Ethereum node")

# 設置賬戶和交易參數
from_account = '0x2bdf99f7460156211739b275b9a22f983c011e55'
to_account = '0x465047ba558172c7a8e9999bd2a080e7a0577e91'
private_key = '0xd7d37d837a297fbe4788cc2ddd52ffe449b1876097737346eed340dfc7e4a54a'

from_account = Web3.to_checksum_address(from_account)
to_account = Web3.to_checksum_address(to_account)

nonce = web3.eth.get_transaction_count(from_account, 'pending')
# nonce += random.randint(1, 1000)  # 增加随机性
print("\ndata_hash_toweb3 : ",web3.to_hex(text=ehr_hash))
print("")
# 構建交易
transaction = {
    'from': from_account,
    'to': to_account,
    'value': 0,
    'gas': 100000,
    'gasPrice': web3.to_wei('50', 'wei'),
    'nonce': nonce,
    'data': web3.to_hex(text=ehr_hash)
}

# 簽名交易
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

# 發送交易
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Transaction hash:", web3.to_hex(tx_hash))

# 查詢交易回執
# tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
# print("Transaction receipt:", tx_receipt)

# 查詢交易數據
tx = web3.eth.get_transaction(tx_hash)
data = tx['input']

# 驗證哈希值
# retrieved_hash = web3.to_text(hexstr=data)
retrieved_hash = str(data).strip("b'")
print("Retrieved hash:", retrieved_hash)

# 比較原始哈希值和鏈上存儲的哈希值
if ehr_hash == retrieved_hash:
    print("Hash values match, EHR is verified!")
else:
    print("Hash values do not match!")
