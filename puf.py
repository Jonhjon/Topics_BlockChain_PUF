import hashlib
import numpy as np

# Step 1: 随机生成一个数，并进行SHA-256哈希
random_number = np.random.randint(0, 2**32,dtype=np.int64)
hash_object = hashlib.sha512(str(random_number).encode())
hex_hash = hash_object.hexdigest()

# Step 2: 十六进制转二进制
bin_hash = bin(int(hex_hash, 16))[2:].zfill(512)

# Step 3: 生成1024个随机数存入数组
random_array = np.random.randint(10, 100, size=1024)

# Step 4: 分四组
arrays = np.split(random_array, 4)

# Step 5: 比较大小并生成Mux数组
Mux1 = np.where(arrays[0] > arrays[1], 1, 0)
Mux2 = np.where(arrays[2] > arrays[3], 1, 0)

# Step 6: Mux数组和SHA-256结果比较，生成新数组
bin_hash_array = np.array(list(map(int, bin_hash)))
new_array_1 = np.where(Mux1 > bin_hash_array[:256], 1, 0)
new_array_2 = np.where(Mux2 > bin_hash_array[256:], 1, 0)

# Step 7: 比较两个新数组大小
RO_PUF_Temp_Array = np.where(new_array_1 > new_array_2, 1, 0)

# Step 8: 交换位移，前8位转成十进制计算位移量
shift_amount = int(''.join(map(str, RO_PUF_Temp_Array[:8])), 2)

# Step 9: 数组位移
shifted_array = np.roll(RO_PUF_Temp_Array, shift_amount)
overflow_part = shifted_array[:shift_amount]
shifted_array[:shift_amount] = overflow_part

# 打印结果
print("RO PUF Temp Array:", RO_PUF_Temp_Array)
print("Shifted RO PUF Temp Array:", shifted_array)
