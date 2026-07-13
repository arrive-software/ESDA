# Copyright (C) 2026 by Jason Lee,silent_wind
# This program is free software:
#  you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

def esda(x = [[15,21,18,-64],[12,5,-64,13],[15,14,4,5],[2,15,14,10]],y = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]):
    esdaout = [[0 for _ in range(4)] for _ in range(4)]
    z = [[0 for _ in range(4)] for _ in range(4)]
    dz = [[0 for _ in range(4)] for _ in range(4)]
    ASK = [[y[0][3],y[1][1],y[2][0],y[3][1]],[y[0][0],y[2][1],y[0][2],y[2][3]],[y[1][0],y[1][3],y[1][2],y[3][3]],[y[2][0],y[3][0],y[2][2],y[3][2]]]
    
    for i in range(4):
        for j in range(4):
            z[i][j] = x[i][j] + y[i][j]
    for i in range(4):
        dz[0][i] = z[3][i]
        for j in range(1,4):
            dz[j][i] = z[j-1][i]
    for i in range(4):
        for j in range(4):
            esdaout[i][j] = ASK[i][j] + dz[i][j]

    return esdaout
def unesda(esdaout = [[2,15,14,10],[15,21,18,-64],[12,5,-64,13],[15,14,4,5]],y = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]):
    x = [[0 for _ in range(4)] for _ in range(4)]
    z = [[0 for _ in range(4)] for _ in range(4)]
    dz = [[0 for _ in range(4)] for _ in range(4)]
    ASK = [[y[0][3],y[1][1],y[2][0],y[3][1]],[y[0][0],y[2][1],y[0][2],y[2][3]],[y[1][0],y[1][3],y[1][2],y[3][3]],[y[2][0],y[3][0],y[2][2],y[3][2]]]
    
    for i in range(4):
        for j in range(4):
            dz[i][j] = esdaout[i][j] - ASK[i][j]
    for i in range(4):
        z[3][i]=dz[0][i]
        for j in range(1,4):
            z[j-1][i]=dz[j][i]
    for i in range(4):
        for j in range(4):
            x[i][j] = z[i][j] - y[i][j]
    
    return x

def text_to_matrices(text):
    
    ascii_list = [ord(c) for c in text]
    original_len = len(ascii_list)
    
    # 计算需要填充的个数（使总长度能被 16 整除）
    pad = (16 - original_len % 16) % 16
    ascii_list.extend([0] * pad)   # 用 0 填充
    
    matrices = []
    for i in range(0, len(ascii_list), 16):
        block = ascii_list[i:i+16]
        # 按行优先组成 4x4 矩阵
        mat = [
            block[0:4],
            block[4:8],
            block[8:12],
            block[12:16]
        ]
        matrices.append(mat)
    
    return matrices, original_len


def matrices_to_text(matrices, original_len):
    flat = []
    for mat in matrices:
        for row in mat:
            flat.extend(row)
    
    # 截断到原始长度，去除填充
    ascii_codes = flat[:original_len]
    return ''.join(chr(c) for c in ascii_codes)

# 加密
def encrypt_text(plaintext, key_matrix):
    mats, orig_len = text_to_matrices(plaintext)
    encrypted_mats = []
    for mat in mats:
        encrypted_mats.append(esda(mat, key_matrix))
    return encrypted_mats, orig_len

# 解密
def decrypt_text(encrypted_mats, orig_len, key_matrix):
    decrypted_mats = []
    for mat in encrypted_mats:
        decrypted_mats.append(unesda(mat, key_matrix))
    return decrypted_mats, orig_len
