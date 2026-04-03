import sys
from PyQt6 import QtWidgets
from playfair import Ui_Dialog
from playfair_cipher import PlayfairCipher


class PlayfairApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Playfair Cipher")

        # Kết nối các nút với hàm xử lý
        self.ui.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.handle_decrypt)
        self.ui.btn_clear.clicked.connect(self.handle_clear)

    def handle_encrypt(self):
        plaintext = self.ui.txt_plaintext.toPlainText().strip()
        key = self.ui.txt_key.text().strip()

        if not plaintext:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập Plaintext!")
            return
        if not key:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập Key!")
            return

        cipher = PlayfairCipher(key)
        encrypted = cipher.encrypt(plaintext)
        self.ui.txt_encrypt.setPlainText(encrypted)

    def handle_decrypt(self):
        ciphertext = self.ui.txt_encrypt.toPlainText().strip()
        key = self.ui.txt_key.text().strip()

        if not ciphertext:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập chuỗi cần giải mã!")
            return
        if not key:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập Key!")
            return

        cipher = PlayfairCipher(key)
        decrypted = cipher.decrypt(ciphertext)
        self.ui.txt_decrypt.setPlainText(decrypted)

    def handle_clear(self):
        self.ui.txt_plaintext.clear()
        self.ui.txt_key.clear()
        self.ui.txt_encrypt.clear()
        self.ui.txt_decrypt.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec())