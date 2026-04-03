class TranspositionCipher:

    def __init__(self):
        pass

    def encrypt(self, text, key):
        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text

    def decrypt(self, text, key):
        num_cols = key
        num_rows = len(text) // key
        remainder = len(text) % key  # số cột có thêm 1 ký tự ở hàng cuối

        # Tính độ dài từng cột
        col_lengths = []
        for col in range(num_cols):
            if col < remainder:
                col_lengths.append(num_rows + 1)
            else:
                col_lengths.append(num_rows)

        # Chia ciphertext thành các cột
        cols = []
        start = 0
        for length in col_lengths:
            cols.append(list(text[start:start + length]))
            start += length

        # Đọc theo hàng ngang để khôi phục plaintext
        plain_text = ''
        for row in range(num_rows + (1 if remainder > 0 else 0)):
            for col in range(num_cols):
                if row < len(cols[col]):
                    plain_text += cols[col][row]
        return plain_text