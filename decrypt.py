import json
from eth_account import Account

# 設置 `keystore` 文件路徑和賬戶密碼
keystore_file_path = r'UTC--2024-05-22T08-23-18.599501038Z--2bdf99f7460156211739b275b9a22f983c011e55'
password = '0000'

# 讀取 `keystore` 文件內容
with open(keystore_file_path) as keyfile:
    encrypted_key = keyfile.read()
    private_key = Account.decrypt(encrypted_key, password)
    private_key_hex = private_key.hex()

print("Private Key:", private_key_hex)
