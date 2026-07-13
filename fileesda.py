import os
import sys

# ===================== 加密核心函数（esda）=====================
def esda(x, y):
    esdaout = [[0 for _ in range(4)] for _ in range(4)]
    z = [[0 for _ in range(4)] for _ in range(4)]
    dz = [[0 for _ in range(4)] for _ in range(4)]
    ASK = [[y[0][3], y[1][1], y[2][0], y[3][1]],
           [y[0][0], y[2][1], y[0][2], y[2][3]],
           [y[1][0], y[1][3], y[1][2], y[3][3]],
           [y[2][0], y[3][0], y[2][2], y[3][2]]]

    for i in range(4):
        for j in range(4):
            z[i][j] = x[i][j] + y[i][j]

    for i in range(4):
        dz[0][i] = z[3][i]
        for j in range(1, 4):
            dz[j][i] = z[j - 1][i]

    for i in range(4):
        for j in range(4):
            esdaout[i][j] = ASK[i][j] + dz[i][j]

    return esdaout


# ===================== 文本 → 矩阵 工具函数 =====================
def text_to_matrices(text):
    """将字符串转换为 4x4 矩阵列表（元素为字符的 Unicode 码点）"""
    codes = [ord(c) for c in text]
    orig_len = len(codes)

    # 用 0 填充到 16 的倍数
    pad = (16 - orig_len % 16) % 16
    codes.extend([0] * pad)

    matrices = []
    for i in range(0, len(codes), 16):
        block = codes[i:i+16]
        mat = [block[0:4], block[4:8], block[8:12], block[12:16]]
        matrices.append(mat)

    return matrices, orig_len


# ===================== 读取密钥文件 =====================
def read_key_matrix(filename='key'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read(16)
    except FileNotFoundError:
        print(f"错误：密钥文件 '{filename}' 不存在。")
        sys.exit(1)

    # 不足 16 个字符时用空格填充
    if len(content) < 16:
        content = content.ljust(16, ' ')

    codes = [ord(c) for c in content]
    key = [codes[0:4], codes[4:8], codes[8:12], codes[12:16]]
    return key


# ===================== 处理单个 .esda 文件 =====================
def process_file(filepath, key_matrix):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            plaintext = f.read()
    except Exception as e:
        print(f"读取文件 {filepath} 失败：{e}")
        return

    # 原文转为矩阵并加密
    matrices, orig_len = text_to_matrices(plaintext)
    encrypted_mats = [esda(mat, key_matrix) for mat in matrices]

    # 输出文件名：替换 .esda 为 .ae
    if filepath.endswith('.esda'):
        outpath = filepath[:-5] + '.ae'
    else:
        outpath = filepath + '.ae'   # 防御性写法

    # 写入加密结果
    try:
        with open(outpath, 'w', encoding='utf-8') as f:
            # 第一行记录原文长度，方便将来解密时去掉填充
            f.write(str(orig_len) + '\n')
            for mat in encrypted_mats:
                for row in mat:
                    f.write(' '.join(str(val) for val in row) + '\n')
        print(f"已加密: {filepath} -> {outpath}")
    except Exception as e:
        print(f"写入文件 {outpath} 失败：{e}")

# ===================== 解密核心函数（unesda）=====================
def unesda(esdaout, y):
    x = [[0 for _ in range(4)] for _ in range(4)]
    z = [[0 for _ in range(4)] for _ in range(4)]
    dz = [[0 for _ in range(4)] for _ in range(4)]
    ASK = [[y[0][3], y[1][1], y[2][0], y[3][1]],
           [y[0][0], y[2][1], y[0][2], y[2][3]],
           [y[1][0], y[1][3], y[1][2], y[3][3]],
           [y[2][0], y[3][0], y[2][2], y[3][2]]]

    for i in range(4):
        for j in range(4):
            dz[i][j] = esdaout[i][j] - ASK[i][j]

    for i in range(4):
        z[3][i] = dz[0][i]
        for j in range(1, 4):
            z[j - 1][i] = dz[j][i]

    for i in range(4):
        for j in range(4):
            x[i][j] = z[i][j] - y[i][j]

    return x


# ===================== 工具函数 =====================
def read_key_matrix(filename='key'):
    """从 key 文件读取 16 字符生成 4x4 密钥矩阵"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read(16)
    except FileNotFoundError:
        print(f"错误：密钥文件 '{filename}' 不存在。")
        sys.exit(1)

    if len(content) < 16:
        content = content.ljust(16, ' ')

    codes = [ord(c) for c in content]
    key = [codes[0:4], codes[4:8], codes[8:12], codes[12:16]]
    return key


def matrices_to_text(matrices, original_len):
    flat = []
    for mat in matrices:
        for row in mat:
            flat.extend(row)
    codes = flat[:original_len]
    return ''.join(chr(c) for c in codes)


# ===================== 处理单个 .ae 文件 =====================
def process_ae_file(filepath, key_matrix):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"读取文件 {filepath} 失败：{e}")
        return

    if not lines:
        print(f"{filepath} 是空文件，跳过。")
        return

    # 第一行：原始文本长度
    try:
        original_len = int(lines[0].strip())
    except ValueError:
        print(f"{filepath} 第一行不是有效长度，跳过。")
        return

    # 剩余行：加密数据（每 4 行组成一个 4x4 矩阵）
    data_lines = [line.strip() for line in lines[1:] if line.strip() != '']
    if len(data_lines) % 4 != 0:
        print(f"{filepath} 数据行数不是 4 的倍数，可能已损坏，跳过。")
        return

    matrices = []
    for i in range(0, len(data_lines), 4):
        mat = []
        for j in range(4):
            parts = data_lines[i + j].split()
            if len(parts) != 4:
                print(f"{filepath} 行格式错误：{data_lines[i + j]}，跳过。")
                return
            try:
                row = [int(p) for p in parts]
            except ValueError:
                print(f"{filepath} 包含非整数数据，跳过。")
                return
            mat.append(row)
        matrices.append(mat)

    # 解密每个矩阵
    decrypted_mats = [unesda(mat, key_matrix) for mat in matrices]

    # 还原为文本
    plaintext = matrices_to_text(decrypted_mats, original_len)

    # 输出文件：去掉 .ae 后缀
    if filepath.endswith('.ae'):
        outpath = filepath[:-3]
    else:
        outpath = filepath + '.dec'  # 意外情况的安全处理

    try:
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(plaintext)
        print(f"已解密: {filepath} -> {outpath}")
    except Exception as e:
        print(f"写入文件 {outpath} 失败：{e}")


# ===================== 加密函数 =====================
def encrypt_files():
    key_matrix = read_key_matrix('key')

    # 获取当前目录下所有 .esda 文件
    esda_files = [f for f in os.listdir('.') if f.endswith('.esda')]
    if not esda_files:
        print("当前目录下未找到 .esda 文件。")
        return

    for fname in esda_files:
        process_file(fname, key_matrix)


# ===================== 解密函数 =====================
def decrypt_files():
    key_matrix = read_key_matrix('key')

    ae_files = [f for f in os.listdir('.') if f.endswith('.ae')]
    if not ae_files:
        print("当前目录下未找到 .ae 文件。")
        return

    for fname in ae_files:
        process_ae_file(fname, key_matrix)

input_choice = input("请选择操作：1.加密文件 2.解密文件\n输入: ").strip()
if input_choice == '1':
    encrypt_files()
elif input_choice == '2':
    decrypt_files()