# 標準ライブラリ
import os
import sys

# 外部ライブラリ
import PySide6
from PySide6.QtWidgets import QApplication,QWidget

# デフォルトのウインドウ
class MainWindow(QWidget):
    def __init__(self, parent=None):
        # 親クラスの初期化
        super().__init__(parent)
        self.setWindowTitle("My Browser")

# メイン処理
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
