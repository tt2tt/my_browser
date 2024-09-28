# 標準ライブラリ
import os
import sys

# 外部ライブラリ
import PySide6
from PySide6.QtWidgets import QApplication,QWidget,QVBoxLayout,QMainWindow
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

# デフォルトのウインドウ
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # 親クラスの初期化
        QMainWindow.__init__(self)
        self.setWindowTitle("My Browser")
        self.widget = QWidget(self)

        # Webページの読み込み
        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://www.python.org/"))

        # レイアウトの作成
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.webview)

        # メインレイアウトの指定
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

# メイン処理
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
