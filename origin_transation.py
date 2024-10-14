import hashlib
import json
import random
from web3 import Web3

from decrypt import decrypt_private_key


class BlockChainProcess:
    def __init__(self, from_account: str, to_account: str, private_key_path: str) -> None:
        self._from_account = Web3.to_checksum_address(from_account)
        self._to_account = Web3.to_checksum_address(to_account)
        self._private_key = decrypt_private_key(private_key_path)

        self._remote_node_address = 'http://192.168.1.109:8545'
        self._web3 = Web3(Web3.HTTPProvider(self._remote_node_address))

    def set_node_address(self, node_address: str) -> None:  #區塊鏈地址的set
        self._remote_node_address = node_address

    def get_node_address(self):#區塊鏈地址的get
        return self._remote_node_address

    def set_from_account(self, from_account: str) -> None:  #轉帳方的set
        self._from_account = Web3.to_checksum_address(from_account)

    def get_from_account(self): #轉帳方的get
        return self._from_account

    def set_to_account(self, to_account: str) -> None:  #接收方的set
        self._to_account = Web3.to_checksum_address(to_account)

    def get_to_account(self):  #接受方的get
        return self._to_account

    def __summary_ehr(self, ehr):
        # 將摘要轉換為 JSON 字符串並計算 SHA-256 哈希值
        ehr_summary_json = json.dumps(ehr, sort_keys=True)
        ehr_hash = hashlib.sha256(ehr_summary_json.encode('utf-8')).hexdigest()
        print("EHR Hash:", ehr_hash)
        return ehr_hash

    def send_transaction(self, ehr) -> str:
        ehr_hash = self.__summary_ehr(ehr)
        nonce = self._web3.eth.get_transaction_count(self._from_account, 'pending')
        # nonce += random.randint(1, 1000)  # 增加随机性
        print("\ndata_hash_toweb3 : ", self._web3.to_hex(text=ehr_hash))
        print("")
        # 構建交易
        transaction = {
            'from': self._from_account,
            'to': self._to_account,
            'value': 0,
            'gas': 100000,
            'gasPrice': self._web3.to_wei('50', 'wei'),
            'nonce': nonce,
            'data': self._web3.to_hex(text=ehr_hash)
        }

        # 簽名交易
        signed_txn = self._web3.eth.account.sign_transaction(transaction, private_key=self._private_key)

        # 發送交易
        tx_hash = self._web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print("Transaction hash:", self._web3.to_hex(tx_hash))
        return self._web3.to_hex(tx_hash)

    def search_transaction(self, tx_hash):
        tx = self._web3.eth.get_transaction(tx_hash)
        transaction_data = tx['input']
        return transaction_data

    def verify_transaction(self, transaction_data, ehr):
        ehr_hash = self.__summary_ehr(ehr)
        retrieved_hash = str(transaction_data).strip("b'")
        print("Retrieved hash:", retrieved_hash)

        # 比較原始哈希值和鏈上存儲的哈希值
        if ehr_hash == retrieved_hash:
            print("Hash values match, EHR is verified!")
            return True
        else:
            print("Hash values do not match!")
            return False


# 下面這段僅用於測試邏輯，不參與flask應用執行
if __name__ == "__main__":
    # # 定義電子病歷摘要
    ehr_summary = {
        "patient_id": "123456",
        "diagnosis": "Hypertension",
        "prescription": "Medication A, Medication B",
        "date": "2024-05-27"
    }
    black_chain_process = BlockChainProcess('0x2bdf99f7460156211739b275b9a22f983c011e55',
                                            '0x465047ba558172c7a8e9999bd2a080e7a0577e91',
                                            'UTC--2024-05-22T08-23-18.599501038Z--2bdf99f7460156211739b275b9a22f983c011e55')
    tx_hash = black_chain_process.send_transaction(ehr_summary)
    transaction_data = black_chain_process.search_transaction(tx_hash)
    black_chain_process.verify_transaction(transaction_data, ehr_summary)
