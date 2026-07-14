import esda

# 示例使用
plaintext = "Hello, World!"
key_matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

# 加密
encrypted_mats, orig_len = esda.encrypt_text(plaintext, key_matrix)

# 解密
decrypted_mats = esda.decrypt_text(encrypted_mats, orig_len, key_matrix)

# 输出解密后的文本
decrypted_text = esda.matrices_to_text(decrypted_mats, orig_len)
print("Encrypted Text:", esda.matrices_to_text(encrypted_mats, orig_len))
print("Decrypted Text:", decrypted_text)