import numpy as np

# กำหนด Modulo ตามจำนวนตัวอักษรภาษาอังกฤษ (A-Z = 26)
MOD = 26

# เมทริกซ์กุญแจสำหรับเข้ารหัส (Key Matrix - ต้องเป็นเมทริกซ์ที่หาตัวผกผันได้)
# ในที่นี้สมมติให้ Key คือ [[3, 3], [2, 5]]
K = np.array([[3, 3], [2, 5]])

# ฟังก์ชันหา Modular Inverse ของเมทริกซ์ 2x2 ภายใต้ Mod 26
def mod_inverse_matrix(matrix, mod):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = -1
    for i in range(mod):
        if (det * i) % mod == 1:
            det_inv = i
            break
    if det_inv == -1:
        raise ValueError("Matrix นี้ไม่สามารถหา Inverse ภายใต้ Mod นี้ได้")

    # คำนวณ Adjugate Matrix และคูณด้วย det_inv หา Modulo
    a, b = matrix[0, 0], matrix[0, 1]
    c, d = matrix[1, 0], matrix[1, 1]

    inv_matrix = np.array([[d, -b], [-c, a]]) * det_inv
    return np.mod(inv_matrix, mod)

# 1. ฟังก์ชันแปลงข้อความ (2 ตัวอักษร) เป็นตัวเลข (0-25)
def text_to_vector(text):
    return np.array([ord(text[0].upper()) - 65, ord(text[1].upper()) - 65])

# 2. ฟังก์ชันแปลงตัวเลขกลับเป็นข้อความ
def vector_to_text(vector):
    return chr(vector[0] + 65) + chr(vector[1] + 65)

# --- ตัวอย่างการใช้งานจริง ---

# สมมติผู้เล่นเลือกพิกัดเป็นข้อความ 2 ตัวอักษร เช่น "B4" (สมมติแทนด้วย "BD")
target_text = "BD"
print(f"พิกัดเดิมที่ต้องการยิง: {target_text}")

# แปลงเป็นเวกเตอร์ตัวเลข
vec = text_to_vector(target_text)

# เข้ารหัส (Encryption) -> ส่งออกไปให้เพื่อน
cipher_vec = np.dot(K, vec) % MOD
cipher_text = vector_to_text(cipher_vec)
print(f"-> ส่งรหัสลับให้ฝ่ายตรงข้าม: {cipher_text}")

# ฝ่ายตรงข้ามได้รับ cipher_text แล้วนำมาถอดรหัส (Decryption)
K_inv = mod_inverse_matrix(K, MOD)
received_vec = text_to_vector(cipher_text)
decrypted_vec = np.dot(K_inv, received_vec) % MOD
final_text = vector_to_text(decrypted_vec)
print(f"-> ฝ่ายรับถอดรหัสออกมาได้พิกัดจริง: {final_text}")