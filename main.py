from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
import sys

from browser_tab import BrowserTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # メインウインドウ設定
        self.setWindowTitle("マイブラウザ")
        self.resize(800, 600)

        # タブウィジェット
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # タブを追加
        self.browser_tab = BrowserTab()
        self.tabs.addTab(self.browser_tab, "新しいタブ")

if __name__ == "__main__":
    # メインウインドウの呼び出し
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
