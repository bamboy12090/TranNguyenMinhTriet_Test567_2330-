class PlayfairCipher:
    def __init__(self, key):
        self.key = key
        self.matrix = self.create_playfair_matrix(key)

    def create_playfair_matrix(self, key):
        key = key.upper().replace('J', 'I')
        key_set = set()
        matrix = []

        # Thêm các ký tự từ key vào matrix
        for char in key:
            if char not in key_set and char.isalpha():
                matrix.append(char)
                key_set.add(char)

        # Thêm các ký tự còn lại của bảng chữ cái (loại bỏ J)
        for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
            if char not in key_set:
                matrix.append(char)
                key_set.add(char)

        # Chuyển thành ma trận 5x5
        return [matrix[i:i+5] for i in range(0, 25, 5)]

    def find_letter_coords(self, letter):
        """Tìm tọa độ của ký tự trong ma trận"""
        letter = letter.upper()
        if letter == 'J':
            letter = 'I'
        for i in range(5):
            for j in range(5):
                if self.matrix[i][j] == letter:
                    return i, j
        return None

    def prepare_plaintext(self, plaintext):
        """
        Chuẩn bị plaintext: chèn 'X' vào giữa 2 ký tự liền kề giống nhau,
        thêm 'X' vào cuối nếu độ dài lẻ, sau đó trả về list ký tự.
        """
        text = list(plaintext.upper().replace('J', 'I').replace(' ', ''))

        # Chèn X giữa 2 ký tự liền kề giống nhau
        i = 0
        while i < len(text) - 1:
            if text[i] == text[i + 1]:
                text.insert(i + 1, 'X')
                i += 2
            else:
                i += 2

        # Thêm X vào cuối nếu độ dài lẻ
        if len(text) % 2 != 0:
            text.append('X')

        return text

    def encrypt(self, plaintext):
        """Mã hóa thông điệp"""
        text = self.prepare_plaintext(plaintext)

        ciphertext = ""
        for i in range(0, len(text), 2):
            a, b = text[i], text[i + 1]
            row1, col1 = self.find_letter_coords(a)
            row2, col2 = self.find_letter_coords(b)

            if row1 == row2:
                # Cùng hàng: lấy ký tự bên phải
                ciphertext += self.matrix[row1][(col1 + 1) % 5]
                ciphertext += self.matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                # Cùng cột: lấy ký tự bên dưới
                ciphertext += self.matrix[(row1 + 1) % 5][col1]
                ciphertext += self.matrix[(row2 + 1) % 5][col2]
            else:
                # Hình chữ nhật: đổi cột
                ciphertext += self.matrix[row1][col2]
                ciphertext += self.matrix[row2][col1]

        return ciphertext

    def decrypt(self, ciphertext):
        """Giải mã thông điệp"""
        ciphertext = ciphertext.upper().replace('J', 'I').replace(' ', '')
        raw = ""

        for i in range(0, len(ciphertext), 2):
            pair = ciphertext[i:i + 2]
            row1, col1 = self.find_letter_coords(pair[0])
            row2, col2 = self.find_letter_coords(pair[1])

            if row1 == row2:
                # Cùng hàng: lấy ký tự bên trái
                raw += self.matrix[row1][(col1 - 1) % 5]
                raw += self.matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                # Cùng cột: lấy ký tự bên trên
                raw += self.matrix[(row1 - 1) % 5][col1]
                raw += self.matrix[(row2 - 1) % 5][col2]
            else:
                # Hình chữ nhật: đổi cột
                raw += self.matrix[row1][col2]
                raw += self.matrix[row2][col1]

        # Loại bỏ X padding sau khi giải mã:
        # 1. Bỏ X cuối chuỗi (padding cuối)
        if raw.endswith('X'):
            raw = raw[:-1]

        # 2. Bỏ X nằm giữa 2 ký tự giống nhau (padding chèn giữa cặp trùng)
        plaintext = ""
        i = 0
        while i < len(raw):
            if (raw[i] == 'X'
                    and i > 0
                    and i < len(raw) - 1
                    and raw[i - 1] == raw[i + 1]):
                i += 1  # bỏ X padding
            else:
                plaintext += raw[i]
                i += 1

        return plaintext